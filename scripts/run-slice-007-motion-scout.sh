#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
project_python="$repo_root/.venv/bin/python"
runtime_root="${LIVING_LITERATURE_RUNTIME_ROOT:-$HOME/models/living-literature/runtimes/mlx-gen-0.33.1}"
runtime_cli="$runtime_root/.venv/bin/mlxgen"
model_store="${LIVING_LITERATURE_MODEL_STORE:-$HOME/models/huggingface/hub}"
model_snapshot="$model_store/models--AbstractFramework--wan2.2-i2v-a14b-diffusers-bf16/snapshots/ef2a0bfe5b4ca7edb84c93f1675edb1a8bfe7d60"
source_still="$repo_root/outputs/slice-006/source-still-candidates/candidate-d-frame-048.png"
output_path="$repo_root/outputs/slice-007/wan2.2-i2v-a14b-motion-scout-seed-42.mp4"
artifact_root="$repo_root/benchmarks/artifacts/slice-007"
run_id="local-files-only-motion-scout-seed-42"
run_root="$artifact_root/$run_id"

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
  local total
  local child_pid
  local child_total
  local rss
  rss="$(ps -o rss= -p "$parent_pid" 2>/dev/null | tr -d ' ' || true)"
  total="${rss:-0}"
  while IFS= read -r child_pid; do
    [[ -n "$child_pid" ]] || continue
    child_total="$(sum_process_tree_rss_kb "$child_pid")"
    total=$((total + child_total))
  done < <(pgrep -P "$parent_pid" 2>/dev/null || true)
  printf '%s\n' "$total"
}

if pgrep -fl 'mlxgen.*generate|mlxgen-generate-wan|mflux.models.wan.cli.wan_generate' >/dev/null 2>&1; then
  printf 'Refusing scout: another Wan or MLX-Gen inference process is running.\n' >&2
  pgrep -fl 'mlxgen.*generate|mlxgen-generate-wan|mflux.models.wan.cli.wan_generate' >&2 || true
  exit 1
fi

for tracked_path in \
  benchmarks/slice-007-wan-2.2-i2v-a14b-motion-scout.json \
  docs/slice-007-wan-2.2-i2v-a14b-motion-scout.md \
  manifests/models/wan2.2-i2v-a14b-bf16.json \
  manifests/runtimes/mlx-gen-0.33.1.json \
  runtimes/mlx-gen-0.33.1/pyproject.toml \
  runtimes/mlx-gen-0.33.1/uv.lock \
  scripts/download-wan2.2-i2v-a14b-bf16.py \
  scripts/prepare-slice-007-runtime.py \
  scripts/run-slice-007-motion-scout.sh \
  scripts/verify-slice-007.py; do
  if ! git -C "$repo_root" diff --quiet HEAD -- "$tracked_path"; then
    printf 'Refusing scout: %s differs from committed HEAD.\n' "$tracked_path" >&2
    exit 1
  fi
done

"$project_python" "$repo_root/scripts/verify-slice-007.py" --preflight

if [[ ! -x "$runtime_cli" ]]; then
  printf 'Refusing scout: missing pinned runtime CLI at %s.\n' "$runtime_cli" >&2
  exit 1
fi
if [[ ! -d "$model_snapshot" ]]; then
  printf 'Refusing scout: missing pinned model snapshot at %s.\n' "$model_snapshot" >&2
  exit 1
fi

free_percentage="$(memory_pressure | awk '/System-wide memory free percentage:/ { gsub("%", "", $5); print $5 }')"
swap_used_mb="$(sysctl -n vm.swapusage | sed -E 's/.*used = ([0-9.]+)M.*/\1/')"
repo_disk_available_kb="$(df -Pk "$repo_root" | awk 'NR == 2 { print $4 }')"
model_disk_available_kb="$(df -Pk "$model_store" | awk 'NR == 2 { print $4 }')"
thermal_status="$(pmset -g therm 2>&1)"

if ((free_percentage < minimum_preflight_memory)); then
  printf 'Refusing scout: only %s%% memory is free; %s%% required.\n' \
    "$free_percentage" "$minimum_preflight_memory" >&2
  exit 1
fi
if [[ "$swap_used_mb" != "0.00" && "$swap_used_mb" != "0" ]]; then
  printf 'Refusing scout: swap is %s MiB; zero required.\n' "$swap_used_mb" >&2
  exit 1
fi
if ((repo_disk_available_kb < minimum_preflight_disk_kb || model_disk_available_kb < minimum_preflight_disk_kb)); then
  printf 'Refusing scout: less than 120 GiB is free on a required volume.\n' >&2
  exit 1
fi
if ! grep -q 'No thermal warning level' <<<"$thermal_status" || \
   ! grep -q 'No performance warning level' <<<"$thermal_status"; then
  printf 'Refusing scout: thermal or performance warning is active.\n%s\n' "$thermal_status" >&2
  exit 1
fi

mkdir -p "$run_root" "$(dirname "$output_path")"
attempt_marker="$run_root/generation-attempt-started.marker"
if [[ -e "$attempt_marker" || -e "$output_path" ]]; then
  printf 'Refusing scout: the one-shot generation attempt was already started.\n' >&2
  exit 1
fi

log_path="$run_root/run.log"
sample_path="$run_root/system-samples.tsv"
summary_path="$run_root/summary.env"
metadata_path="${output_path%.mp4}.metadata.json"

benchmark_command=(
  /usr/bin/env
  HF_HUB_OFFLINE=1
  TRANSFORMERS_OFFLINE=1
  DIFFUSERS_OFFLINE=1
  "$runtime_cli"
  generate
  --model "$model_snapshot"
  --task image-to-video
  --image "$source_still"
  --prompt "Single continuous five-second shot, locked-off wide side view. A Late Bronze Age Aegean galley with a long black hull, curved prow and stern, one mast and one rectangular square sail moves steadily from left to right across a dark wine-colored sea before dawn. The bow always points right; the stern remains left. Moderate wind blows from left to right, naturally filling the sail and raising aligned wavelets. A small bow wave splits outward at the prow; a narrow foamy wake begins only behind the stern and trails leftward. Heavy purple clouds drift slowly. Stable geometry, physically coherent motion, no camera movement, text, or modern objects. Preserve the approved input image’s ship design, palette, atmosphere, framing, and horizon."
  --negative-prompt "reverse playback, backward sailing, wake or foam ahead of the bow, wake extending forward, perfectly still water with a filled sail, deformed sail, changing hull geometry, extra mast, camera dolly, pan, zoom, text, watermark, modern vessel, blurry image, JPEG artifacts"
  --width 448
  --height 256
  --canvas-policy source-aspect
  --resize-mode resize
  --frames 41
  --fps 8
  --steps 15
  --seed 42
  --guidance 4.0
  --guidance-2 3.0
  --flow-shift 3.0
  --solver unipc
  --low-ram
  --no-prompt-cache
  --metadata
  --json-events
  --no-replace
  --output "$output_path"
)

started_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
started_epoch="$(date +%s)"
git_commit="$(git -C "$repo_root" rev-parse HEAD)"
printf '%s\n' "$started_at" >"$attempt_marker"
printf 'timestamp_utc\tmemory_free_percent\tswap_used_mb\trepo_disk_available_kb\tmodel_disk_available_kb\tprocess_tree_rss_kb\tthermal_status\n' >"$sample_path"
printf 'run_id=%s\nmode=local-files-only\nstarted_at_utc=%s\noutput=%s\nmetadata=%s\nmodel_snapshot=%s\nruntime_root=%s\ngit_commit=%s\n' \
  "$run_id" "$started_at" "$output_path" "$metadata_path" "$model_snapshot" "$runtime_root" "$git_commit" >"$summary_path"
printf 'Starting %s; detailed output: %s\n' "$run_id" "$log_path"

set +e
/usr/bin/time -l "${benchmark_command[@]}" >"$log_path" 2>&1 &
run_pid=$!
set -e

safety_stop="none"
denoising_started=0
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

  if ((denoising_started == 0)) && grep -q '"phase": "denoise"' "$log_path" 2>/dev/null; then
    denoising_started=1
  fi
  if ((denoising_started == 1)); then
    log_mtime="$(stat -f %m "$log_path")"
    if ((now_epoch - log_mtime > stop_progress_silence_seconds)); then
      safety_stop="no-denoising-progress-for-20-minutes"
    fi
  fi

  if [[ "$safety_stop" != "none" ]]; then
    printf 'Stopping %s: %s\n' "$run_id" "$safety_stop" | tee -a "$log_path" >&2
    terminate_process_tree "$run_pid"
    break
  fi
  sleep 15
done

set +e
wait "$run_pid"
exit_code=$?
set -e

ended_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
ended_epoch="$(date +%s)"
duration_seconds=$((ended_epoch - started_epoch))
printf 'ended_at_utc=%s\nduration_seconds=%s\ninference_exit_code=%s\nsafety_stop=%s\ndenoising_started=%s\n' \
  "$ended_at" "$duration_seconds" "$exit_code" "$safety_stop" "$denoising_started" >>"$summary_path"

if [[ "$exit_code" -ne 0 || "$safety_stop" != "none" ]]; then
  printf '%s failed with exit code %s and safety stop %s. See %s\n' \
    "$run_id" "$exit_code" "$safety_stop" "$log_path" >&2
  exit 1
fi
if [[ ! -f "$output_path" || ! -f "$metadata_path" ]]; then
  printf '%s completed without the declared output and metadata.\n' "$run_id" >&2
  exit 1
fi

output_sha256="$(shasum -a 256 "$output_path" | awk '{ print $1 }')"
output_size_bytes="$(stat -f %z "$output_path")"
metadata_sha256="$(shasum -a 256 "$metadata_path" | awk '{ print $1 }')"
printf 'output_sha256=%s\noutput_size_bytes=%s\nmetadata_sha256=%s\n' \
  "$output_sha256" "$output_size_bytes" "$metadata_sha256" >>"$summary_path"
ffprobe -v error \
  -show_entries stream=codec_name,pix_fmt,width,height,nb_frames,r_frame_rate,duration \
  -show_entries format=duration,size \
  -of json "$output_path" >"$run_root/ffprobe.json"
ffmpeg -v error -i "$output_path" -f null -
printf 'full_decode=pass\nwrapper_exit_code=0\nwrapper_closeout=normal\n' >>"$summary_path"

printf '%s completed in %s seconds.\n' "$run_id" "$duration_seconds"
printf 'output_sha256=%s\n' "$output_sha256"
