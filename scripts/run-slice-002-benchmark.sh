#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
run_mode="${1:?usage: run-slice-002-benchmark.sh online|offline}"
python_bin="$repo_root/.venv/bin/python"
artifact_root="$repo_root/benchmarks/artifacts/slice-002"
network_profile='(version 1) (allow default) (deny network*)'

terminate_process_tree() {
  local parent_pid="$1"
  local child_pid
  while IFS= read -r child_pid; do
    [[ -n "$child_pid" ]] || continue
    terminate_process_tree "$child_pid"
  done < <(pgrep -P "$parent_pid" 2>/dev/null || true)
  kill -TERM "$parent_pid" 2>/dev/null || true
}

case "$run_mode" in
  online)
    run_id="online-pinned-baseline"
    output_path="$repo_root/outputs/slice-002/wan-1.3b-online-seed-42.mp4"
    ;;
  offline)
    run_id="offline-network-denied-repeat"
    output_path="$repo_root/outputs/slice-002/wan-1.3b-offline-seed-42.mp4"
    ;;
  *)
    printf 'Unsupported run mode: %s\n' "$run_mode" >&2
    exit 2
    ;;
esac

run_root="$artifact_root/$run_id"
mkdir -p "$run_root" "$(dirname "$output_path")"
log_path="$run_root/run.log"
sample_path="$run_root/system-samples.tsv"
summary_path="$run_root/summary.env"

free_percentage="$(memory_pressure | awk '/System-wide memory free percentage:/ { gsub("%", "", $5); print $5 }')"
swap_used_mb="$(sysctl -n vm.swapusage | sed -E 's/.*used = ([0-9.]+)M.*/\1/')"
disk_available_kb="$(df -Pk "$repo_root" | awk 'NR == 2 { print $4 }')"

if (( free_percentage < 20 )); then
  printf 'Refusing benchmark: only %s%% memory is free.\n' "$free_percentage" >&2
  exit 1
fi
if (( disk_available_kb < 104857600 )); then
  printf 'Refusing benchmark: less than 100 GiB is free.\n' >&2
  exit 1
fi

benchmark_command=(
  "$python_bin"
  "$repo_root/scripts/run-pinned-wan-benchmark.py"
  --network-mode "$run_mode"
  --output "$output_path"
)

network_denial_preflight="not-applicable"
if [[ "$run_mode" == "offline" ]]; then
  if /usr/bin/sandbox-exec -p "$network_profile" "$python_bin" -c 'import socket; socket.socket().bind(("127.0.0.1", 0))' >/dev/null 2>&1; then
    printf 'Network-denial preflight failed: loopback binding was allowed.\n' >&2
    exit 1
  fi
  benchmark_command=(/usr/bin/sandbox-exec -p "$network_profile" "${benchmark_command[@]}")
  network_denial_preflight="pass"
  printf 'network_denial_preflight=pass\n'
fi

started_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
started_epoch="$(date +%s)"
printf 'timestamp_utc\tmemory_free_percent\tswap_used_mb\tdisk_available_kb\tprocess_rss_kb\tthermal_status\n' >"$sample_path"
printf 'run_id=%s\nmode=%s\nstarted_at_utc=%s\noutput=%s\nnetwork_denial_preflight=%s\n' \
  "$run_id" "$run_mode" "$started_at" "$output_path" "$network_denial_preflight" >"$summary_path"
printf 'Starting %s; detailed output: %s\n' "$run_id" "$log_path"

set +e
/usr/bin/time -l "${benchmark_command[@]}" >"$log_path" 2>&1 &
run_pid=$!
set -e

safety_stop="none"
while kill -0 "$run_pid" 2>/dev/null; do
  timestamp="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  free_percentage="$(memory_pressure | awk '/System-wide memory free percentage:/ { gsub("%", "", $5); print $5 }')"
  swap_used_mb="$(sysctl -n vm.swapusage | sed -E 's/.*used = ([0-9.]+)M.*/\1/')"
  disk_available_kb="$(df -Pk "$repo_root" | awk 'NR == 2 { print $4 }')"
  process_rss_kb="$(ps -o rss= -p "$run_pid" | tr -d ' ' || true)"
  thermal_status="$(pmset -g therm 2>&1 | tr '\n\t' '| ' | sed -E 's/[[:space:]]+/ /g')"
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$timestamp" "$free_percentage" "$swap_used_mb" "$disk_available_kb" "${process_rss_kb:-0}" "$thermal_status" >>"$sample_path"

  free_integer="${free_percentage%.*}"
  swap_integer="${swap_used_mb%.*}"
  if (( free_integer <= 10 )); then
    safety_stop="memory-free-at-or-below-10-percent"
  elif (( swap_integer >= 32768 )); then
    safety_stop="swap-at-or-above-32-gib"
  elif (( disk_available_kb < 104857600 )); then
    safety_stop="disk-below-100-gib"
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

if [[ "$exit_code" -ne 0 ]]; then
  printf '%s failed with exit code %s. See %s\n' "$run_id" "$exit_code" "$log_path" >&2
  exit "$exit_code"
fi

output_sha256="$(shasum -a 256 "$output_path" | awk '{ print $1 }')"
output_size_bytes="$(stat -f %z "$output_path")"
printf 'output_sha256=%s\noutput_size_bytes=%s\n' "$output_sha256" "$output_size_bytes" >>"$summary_path"
ffprobe -v error -show_entries stream=codec_name,width,height,nb_frames,r_frame_rate,duration -show_entries format=duration,size -of json "$output_path" >"$run_root/ffprobe.json"
printf 'wrapper_exit_code=0\nwrapper_closeout=normal\n' >>"$summary_path"

printf '%s completed in %s seconds.\n' "$run_id" "$duration_seconds"
printf 'output_sha256=%s\n' "$output_sha256"
