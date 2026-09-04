#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
run_mode="${1:?usage: run-slice-005-benchmark.sh online|offline}"
python_bin="$repo_root/.venv/bin/python"
model_store="${LIVING_LITERATURE_MODEL_STORE:-$HOME/models/huggingface/hub}"
artifact_root="$repo_root/benchmarks/artifacts/slice-005"
network_profile='(version 1) (allow default) (deny network*)'

minimum_preflight_memory=90
minimum_preflight_disk_kb=125829120
stop_memory_percent=10
stop_swap_mb=8192
stop_disk_kb=104857600
stop_progress_silence_seconds=1200
maximum_run_seconds=14400

terminate_process_tree() {
  local parent_pid="$1"
  local child_pid
  while IFS= read -r child_pid; do
    [[ -n "$child_pid" ]] || continue
    terminate_process_tree "$child_pid"
  done < <(pgrep -P "$parent_pid" 2>/dev/null || true)
  kill -TERM "$parent_pid" 2>/dev/null || true
}

sum_process_tree_rss_kb() {
  local parent_pid="$1"
  local total=0
  local process_pid
  local rss
  local -a queue=("$parent_pid")
  local -a next_queue=()
  while ((${#queue[@]} > 0)); do
    next_queue=()
    for process_pid in "${queue[@]}"; do
      rss="$(ps -o rss= -p "$process_pid" 2>/dev/null | tr -d ' ' || true)"
      if [[ -n "$rss" ]]; then
        total=$((total + rss))
      fi
      while IFS= read -r child_pid; do
        [[ -n "$child_pid" ]] && next_queue+=("$child_pid")
      done < <(pgrep -P "$process_pid" 2>/dev/null || true)
    done
    queue=("${next_queue[@]}")
  done
  printf '%s\n' "$total"
}

case "$run_mode" in
  online)
    run_id="online-pinned-14b"
    output_path="$repo_root/outputs/slice-005/wan-14b-online-seed-42.mp4"
    ;;
  offline)
    run_id="offline-network-denied-14b"
    output_path="$repo_root/outputs/slice-005/wan-14b-offline-seed-42.mp4"
    ;;
  *)
    printf 'Unsupported run mode: %s\n' "$run_mode" >&2
    exit 2
    ;;
esac

if pgrep -fl 'run-pinned-wan-14b-benchmark.py|txt2video.py' >/dev/null 2>&1; then
  printf 'Refusing benchmark: another Wan inference process is running.\n' >&2
  pgrep -fl 'run-pinned-wan-14b-benchmark.py|txt2video.py' >&2 || true
  exit 1
fi

for tracked_path in \
  benchmarks/slice-005-wan-2.1-t2v-14b.json \
  manifests/models/wan2.1-t2v-14b.json \
  scripts/run-pinned-wan-14b-benchmark.py \
  scripts/run-slice-005-benchmark.sh \
  scripts/verify-slice-005.py; do
  if ! git -C "$repo_root" diff --quiet HEAD -- "$tracked_path"; then
    printf 'Refusing benchmark: %s differs from committed HEAD.\n' "$tracked_path" >&2
    exit 1
  fi
done

"$python_bin" "$repo_root/scripts/verify-slice-005.py" \
  --model-only \
  --model-store "$model_store"

free_percentage="$(memory_pressure | awk '/System-wide memory free percentage:/ { gsub("%", "", $5); print $5 }')"
swap_used_mb="$(sysctl -n vm.swapusage | sed -E 's/.*used = ([0-9.]+)M.*/\1/')"
repo_disk_available_kb="$(df -Pk "$repo_root" | awk 'NR == 2 { print $4 }')"
model_disk_available_kb="$(df -Pk "$model_store" | awk 'NR == 2 { print $4 }')"
thermal_status="$(pmset -g therm 2>&1)"

if ((free_percentage < minimum_preflight_memory)); then
  printf 'Refusing benchmark: only %s%% memory is free; %s%% required.\n' \
    "$free_percentage" "$minimum_preflight_memory" >&2
  exit 1
fi
if [[ "$swap_used_mb" != "0.00" && "$swap_used_mb" != "0" ]]; then
  printf 'Refusing benchmark: swap is %s MiB; zero required.\n' "$swap_used_mb" >&2
  exit 1
fi
if ((repo_disk_available_kb < minimum_preflight_disk_kb || model_disk_available_kb < minimum_preflight_disk_kb)); then
  printf 'Refusing benchmark: less than 120 GiB is free on a required volume.\n' >&2
  exit 1
fi
if ! grep -q 'No thermal warning level' <<<"$thermal_status" || \
   ! grep -q 'No performance warning level' <<<"$thermal_status"; then
  printf 'Refusing benchmark: thermal or performance warning is active.\n%s\n' "$thermal_status" >&2
  exit 1
fi

run_root="$artifact_root/$run_id"
mkdir -p "$run_root" "$(dirname "$output_path")"
log_path="$run_root/run.log"
sample_path="$run_root/system-samples.tsv"
summary_path="$run_root/summary.env"

benchmark_command=(
  "$python_bin"
  "$repo_root/scripts/run-pinned-wan-14b-benchmark.py"
  --network-mode "$run_mode"
  --model-store "$model_store"
  --output "$output_path"
)

network_denial_preflight="not-applicable"
if [[ "$run_mode" == "offline" ]]; then
  if /usr/bin/sandbox-exec -p "$network_profile" "$python_bin" -c \
    'import socket; socket.socket().bind(("127.0.0.1", 0))' >/dev/null 2>&1; then
    printf 'Network-denial preflight failed: loopback binding was allowed.\n' >&2
    exit 1
  fi
  benchmark_command=(/usr/bin/sandbox-exec -p "$network_profile" "${benchmark_command[@]}")
  network_denial_preflight="pass"
  printf 'network_denial_preflight=pass\n'
fi

started_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
started_epoch="$(date +%s)"
git_commit="$(git -C "$repo_root" rev-parse HEAD)"
printf 'timestamp_utc\tmemory_free_percent\tswap_used_mb\trepo_disk_available_kb\tmodel_disk_available_kb\tprocess_tree_rss_kb\tthermal_status\n' >"$sample_path"
printf 'run_id=%s\nmode=%s\nstarted_at_utc=%s\noutput=%s\nmodel_store=%s\ngit_commit=%s\nnetwork_denial_preflight=%s\n' \
  "$run_id" "$run_mode" "$started_at" "$output_path" "$model_store" "$git_commit" "$network_denial_preflight" >"$summary_path"
printf 'Starting %s; detailed output: %s\n' "$run_id" "$log_path"

set +e
/usr/bin/time -l "${benchmark_command[@]}" >"$log_path" 2>&1 &
run_pid=$!
set -e

safety_stop="none"
progress_started=0
while kill -0 "$run_pid" 2>/dev/null; do
  timestamp="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  now_epoch="$(date +%s)"
  free_percentage="$(memory_pressure | awk '/System-wide memory free percentage:/ { gsub("%", "", $5); print $5 }')"
  swap_used_mb="$(sysctl -n vm.swapusage | sed -E 's/.*used = ([0-9.]+)M.*/\1/')"
  repo_disk_available_kb="$(df -Pk "$repo_root" | awk 'NR == 2 { print $4 }')"
  model_disk_available_kb="$(df -Pk "$model_store" | awk 'NR == 2 { print $4 }')"
  process_tree_rss_kb="$(sum_process_tree_rss_kb "$run_pid")"
  thermal_status="$(pmset -g therm 2>&1)"
  thermal_flat="$(tr '\n\t' '| ' <<<"$thermal_status" | sed -E 's/[[:space:]]+/ /g')"
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$timestamp" "$free_percentage" "$swap_used_mb" "$repo_disk_available_kb" \
    "$model_disk_available_kb" "$process_tree_rss_kb" "$thermal_flat" >>"$sample_path"

  if ((free_percentage <= stop_memory_percent)); then
    safety_stop="memory-free-at-or-below-10-percent"
  elif (( ${swap_used_mb%.*} > stop_swap_mb )); then
    safety_stop="swap-above-8-gib"
  elif ((repo_disk_available_kb < stop_disk_kb || model_disk_available_kb < stop_disk_kb)); then
    safety_stop="disk-below-100-gib"
  elif ! grep -q 'No thermal warning level' <<<"$thermal_status" || \
       ! grep -q 'No performance warning level' <<<"$thermal_status"; then
    safety_stop="thermal-or-performance-warning"
  elif ((now_epoch - started_epoch > maximum_run_seconds)); then
    safety_stop="run-exceeded-4-hours"
  fi

  if ((progress_started == 0)) && grep -qE '[0-9]+%\|' "$log_path" 2>/dev/null; then
    progress_started=1
  fi
  if ((progress_started == 1)); then
    log_mtime="$(stat -f %m "$log_path")"
    if ((now_epoch - log_mtime > stop_progress_silence_seconds)); then
      safety_stop="no-progress-for-20-minutes"
    fi
  fi

  if [[ "$safety_stop" != "none" ]]; then
    printf 'Stopping %s: %s\n' "$run_id" "$safety_stop" | tee -a "$log_path" >&2
    terminate_process_tree "$run_pid"
    break
  fi
  sleep 30
done

set +e
wait "$run_pid"
exit_code=$?
set -e

ended_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
ended_epoch="$(date +%s)"
duration_seconds=$((ended_epoch - started_epoch))
printf 'ended_at_utc=%s\nduration_seconds=%s\ninference_exit_code=%s\nsafety_stop=%s\n' \
  "$ended_at" "$duration_seconds" "$exit_code" "$safety_stop" >>"$summary_path"

if [[ "$exit_code" -ne 0 || "$safety_stop" != "none" ]]; then
  printf '%s failed with exit code %s and safety stop %s. See %s\n' \
    "$run_id" "$exit_code" "$safety_stop" "$log_path" >&2
  exit 1
fi
if [[ ! -f "$output_path" ]]; then
  printf '%s completed without the declared output.\n' "$run_id" >&2
  exit 1
fi

output_sha256="$(shasum -a 256 "$output_path" | awk '{ print $1 }')"
output_size_bytes="$(stat -f %z "$output_path")"
printf 'output_sha256=%s\noutput_size_bytes=%s\n' "$output_sha256" "$output_size_bytes" >>"$summary_path"
ffprobe -v error \
  -show_entries stream=codec_name,width,height,nb_frames,r_frame_rate,duration \
  -show_entries format=duration,size \
  -of json "$output_path" >"$run_root/ffprobe.json"
ffmpeg -v error -i "$output_path" -f null -
printf 'full_decode=pass\nwrapper_exit_code=0\nwrapper_closeout=normal\n' >>"$summary_path"

printf '%s completed in %s seconds.\n' "$run_id" "$duration_seconds"
printf 'output_sha256=%s\n' "$output_sha256"
