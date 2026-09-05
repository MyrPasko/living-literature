#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
project_python="$repo_root/.venv/bin/python"
runtime_root="$HOME/models/living-literature/runtimes/mlx-gen-0.33.1"
runtime_cli="$runtime_root/.venv/bin/mlxgen-generate-wan"
model_store="$HOME/models/huggingface/hub"
model_snapshot="$model_store/models--AbstractFramework--wan2.2-i2v-a14b-diffusers-bf16/snapshots/ef2a0bfe5b4ca7edb84c93f1675edb1a8bfe7d60"
first_image="$repo_root/outputs/next-slice-reference-candidates/right-facing-aegean-galley-start-frame-candidate-v2.png"
last_image="$repo_root/outputs/next-slice-reference-candidates/right-facing-aegean-galley-approved-end-frame-v1.png"
output_path="$repo_root/outputs/slice-009/wan2.2-i2v-a14b-first-last-full-render-seed-42.mp4"
review_root="$repo_root/outputs/slice-009/review"
contact_sheet="$review_root/contact-sheet.png"
run_id="local-files-only-first-last-full-render-seed-42"
run_root="$repo_root/benchmarks/artifacts/slice-009/$run_id"

minimum_preflight_memory=90
minimum_preflight_disk_kb=125829120
stop_memory_percent=10
stop_swap_mb=8192
stop_disk_kb=104857600
stop_progress_silence_seconds=1200
maximum_run_seconds=14400
sample_interval_seconds=15

positive_prompt="One continuous 5.125-second shot from a completely locked camera. Image 1 is the exact first frame; Image 2 is the exact last frame. The Late Bronze Age Aegean galley travels slowly and continuously from LEFT TO RIGHT, bow first. The unmistakable RIGHT-facing curved prow and short massive submerged ram lead the motion in every frame. The LEFT stern and its separate steering oar always trail behind. Movement is smooth and uniform at approximately 3 knots. Across the entire shot, the ship moves only the distance fixed by the two anchor images—approximately one-quarter of its hull length. No sudden acceleration, sliding, sideways drift, or speedboat motion. A steady 8–10-knot following wind blows strictly from LEFT TO RIGHT. The rectangular square sail remains taut and naturally filled. Its cloth belly and loose edges bow gently toward the RIGHT, downwind, throughout the shot. Because the sail is filled, small wind-driven wavelets and short ripples remain clearly visible across the entire sea surface. The water must never become flat, glassy, or motionless. A small bow wave begins precisely at the RIGHT-facing prow and submerged ram. A narrow, low-energy wake begins only behind the LEFT stern and trails leftward. No foam or wake appears ahead of the bow. Preserve the approved ship, ram, steering oar, hull, mast, rigging, sail, purple pre-dawn sky, wine-dark sea, horizon, framing, scale, and lighting. Keep geometry and camera completely stable."
negative_prompt="reverse travel, stern-first movement, backward sailing, bow or ram pointing left, stern leading the ship, rapid movement, acceleration, sliding, sideways drift, speedboat wake, sail bending or bulging left, wind from right to left, limp sail, flat water, glassy sea, motionless water with a filled sail, wake ahead of the bow, foam on the right ahead of the ram, missing steering oar, exposed long ram, deformed hull, changing mast, changing rigging, camera pan, camera tracking, zoom, horizon movement, text, watermark, modern object"

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
  local total child_pid child_total rss
  rss="$(ps -o rss= -p "$parent_pid" 2>/dev/null | tr -d ' ' || true)"
  total="${rss:-0}"
  while IFS= read -r child_pid; do
    [[ -n "$child_pid" ]] || continue
    child_total="$(sum_process_tree_rss_kb "$child_pid")"
    total=$((total + child_total))
  done < <(pgrep -P "$parent_pid" 2>/dev/null || true)
  printf '%s\n' "$total"
}

read_host_state() {
  free_percentage="$(memory_pressure | awk '/System-wide memory free percentage:/ { gsub("%", "", $5); print $5 }')"
  swap_used_mb="$(sysctl -n vm.swapusage | sed -E 's/.*used = ([0-9.]+)M.*/\1/')"
  repo_disk_available_kb="$(df -Pk "$repo_root" | awk 'NR == 2 { print $4 }')"
  model_disk_available_kb="$(df -Pk "$model_store" | awk 'NR == 2 { print $4 }')"
  thermal_status="$(pmset -g therm 2>&1)"
}

if [[ "$(git -C "$repo_root" branch --show-current)" != "feature/slice-009-wan2-2-first-last-full-render" ]]; then
  printf 'Refusing full render: wrong branch.\n' >&2
  exit 1
fi
if [[ -n "$(git -C "$repo_root" status --porcelain=v1)" ]]; then
  printf 'Refusing full render: the tracked working tree is not clean.\n' >&2
  git -C "$repo_root" status --short >&2
  exit 1
fi
if ! git -C "$repo_root" merge-base --is-ancestor 6a3e3381b3190c348697557f60ed05b257c60115 HEAD; then
  printf 'Refusing full render: completed Slice 008 is not an ancestor.\n' >&2
  exit 1
fi
if pgrep -fl 'mlxgen.*generate|mlxgen-generate-wan|mflux.models.wan.cli.wan_generate|ComfyUI|diffusers.*(generate|inference)' >/dev/null 2>&1; then
  printf 'Refusing full render: another model-inference process is running.\n' >&2
  exit 1
fi

for tracked_path in \
  benchmarks/slice-009-wan2.2-first-last-full-render.json \
  docs/slice-009-wan2.2-first-last-full-render.md \
  manifests/models/wan2.2-i2v-a14b-bf16.json \
  manifests/runtimes/mlx-gen-0.33.1.json \
  runtimes/mlx-gen-0.33.1/pyproject.toml \
  runtimes/mlx-gen-0.33.1/uv.lock \
  scripts/run-slice-009-full-render.sh \
  scripts/verify-slice-009.py \
  .project-memory/canon/current-state.md \
  .project-memory/verify-commands.md \
  .project-memory/docs-index.md; do
  if ! git -C "$repo_root" diff --quiet HEAD -- "$tracked_path"; then
    printf 'Refusing full render: %s differs from committed HEAD.\n' "$tracked_path" >&2
    exit 1
  fi
done

"$project_python" "$repo_root/scripts/verify-slice-009.py" --preflight
"$project_python" "$repo_root/scripts/verify-slice-007.py" --preflight

if [[ ! -x "$runtime_cli" || ! -d "$model_snapshot" ]]; then
  printf 'Refusing full render: pinned runtime or model snapshot is missing.\n' >&2
  exit 1
fi
if ! "$runtime_cli" --help | grep -q -- '--last-image'; then
  printf 'Refusing full render: direct Wan CLI does not expose --last-image.\n' >&2
  exit 1
fi

read_host_state
if ((free_percentage < minimum_preflight_memory)); then
  printf 'Refusing full render: only %s%% memory is free; %s%% required.\n' "$free_percentage" "$minimum_preflight_memory" >&2
  exit 1
fi
if [[ "$swap_used_mb" != "0.00" && "$swap_used_mb" != "0" ]]; then
  printf 'Refusing full render: swap is %s MiB; zero required.\n' "$swap_used_mb" >&2
  exit 1
fi
if ((repo_disk_available_kb < minimum_preflight_disk_kb || model_disk_available_kb < minimum_preflight_disk_kb)); then
  printf 'Refusing full render: less than 120 GiB is free on a required volume.\n' >&2
  exit 1
fi
if ! grep -q 'No thermal warning level' <<<"$thermal_status" || ! grep -q 'No performance warning level' <<<"$thermal_status"; then
  printf 'Refusing full render: thermal or performance warning is active.\n' >&2
  exit 1
fi

mkdir -p "$run_root" "$(dirname "$output_path")" "$review_root"
attempt_marker="$run_root/generation-attempt-started.marker"
if [[ -e "$attempt_marker" || -e "$output_path" ]]; then
  printf 'Refusing full render: the one-shot generation attempt was already started.\n' >&2
  exit 1
fi

log_path="$run_root/run.log"
sample_path="$run_root/system-samples.tsv"
summary_path="$run_root/summary.env"
metadata_path="${output_path%.mp4}.metadata.json"
benchmark_command=(
  /usr/bin/env HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 DIFFUSERS_OFFLINE=1
  "$runtime_cli"
  --model "$model_snapshot"
  --image-path "$first_image"
  --last-image "$last_image"
  --prompt "$positive_prompt"
  --negative-prompt "$negative_prompt"
  --width 832
  --height 480
  --canvas-policy source-aspect
  --resize-mode resize
  --frames 81
  --fps 16
  --steps 50
  --seed 42
  --guidance 5.0
  --guidance-2 5.0
  --flow-shift 5.0
  --solver unipc
  --low-ram
  --no-prompt-cache
  --release-inactive-denoiser
  --metadata
  --json-events
  --no-replace
  --output "$output_path"
)

started_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
started_epoch="$(date +%s)"
git_commit="$(git -C "$repo_root" rev-parse HEAD)"
if ! (set -o noclobber; printf 'started_at_utc=%s\ngit_commit=%s\n' "$started_at" "$git_commit" >"$attempt_marker"); then
  printf 'Refusing full render: could not atomically create the one-attempt marker.\n' >&2
  exit 1
fi
printf 'timestamp_utc\tmemory_free_percent\tswap_used_mb\trepo_disk_available_kb\tmodel_disk_available_kb\tprocess_tree_rss_kb\tthermal_status\n' >"$sample_path"
printf 'run_id=%s\nmode=local-files-only\nstarted_at_utc=%s\noutput=%s\nmetadata=%s\nfirst_image=%s\nlast_image=%s\nmodel_snapshot=%s\nruntime_root=%s\ngit_commit=%s\n' \
  "$run_id" "$started_at" "$output_path" "$metadata_path" "$first_image" "$last_image" "$model_snapshot" "$runtime_root" "$git_commit" >"$summary_path"
printf 'Starting %s; detailed output: %s\n' "$run_id" "$log_path"

run_pid=""
cleanup_running_process() {
  local status=$?
  trap - EXIT
  if [[ -n "${run_pid:-}" ]] && kill -0 "$run_pid" 2>/dev/null; then
    terminate_process_tree "$run_pid"
  fi
  exit "$status"
}
trap cleanup_running_process EXIT

set +e
/usr/bin/time -l "${benchmark_command[@]}" >"$log_path" 2>&1 &
run_pid=$!
set -e
safety_stop="none"
denoising_started=0
denoise_event_count=0
last_progress_epoch="$started_epoch"

while kill -0 "$run_pid" 2>/dev/null; do
  timestamp="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  now_epoch="$(date +%s)"
  read_host_state
  process_tree_rss_kb="$(sum_process_tree_rss_kb "$run_pid")"
  thermal_flat="$(tr '\n\t' '| ' <<<"$thermal_status" | sed -E 's/[[:space:]]+/ /g')"
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$timestamp" "$free_percentage" "$swap_used_mb" "$repo_disk_available_kb" "$model_disk_available_kb" "$process_tree_rss_kb" "$thermal_flat" >>"$sample_path"

  current_denoise_count="$(grep -c '"phase": "denoise"' "$log_path" 2>/dev/null || true)"
  if ((current_denoise_count > denoise_event_count)); then
    denoising_started=1
    denoise_event_count="$current_denoise_count"
    last_progress_epoch="$now_epoch"
    printf 'runtime-progress %s\n' "$(grep '"phase": "denoise"' "$log_path" | tail -n 1)"
  fi

  if ((free_percentage <= stop_memory_percent)); then
    safety_stop="memory-free-at-or-below-10-percent"
  elif (( ${swap_used_mb%.*} > stop_swap_mb )); then
    safety_stop="swap-above-8-gib"
  elif ((repo_disk_available_kb < stop_disk_kb || model_disk_available_kb < stop_disk_kb)); then
    safety_stop="disk-below-100-gib"
  elif ! grep -q 'No thermal warning level' <<<"$thermal_status" || ! grep -q 'No performance warning level' <<<"$thermal_status"; then
    safety_stop="thermal-or-performance-warning"
  elif ((denoising_started == 1 && now_epoch - last_progress_epoch >= stop_progress_silence_seconds)); then
    safety_stop="no-denoising-progress-for-20-minutes"
  elif ((now_epoch - started_epoch > maximum_run_seconds)); then
    safety_stop="run-exceeded-4-hours"
  fi

  if [[ "$safety_stop" != "none" ]]; then
    printf 'Stopping %s: %s\n' "$run_id" "$safety_stop" | tee -a "$log_path" >&2
    terminate_process_tree "$run_pid"
    break
  fi
  sleep "$sample_interval_seconds"
done

set +e
wait "$run_pid"
exit_code=$?
set -e
run_pid=""
if [[ "$exit_code" -ne 0 && "$safety_stop" == "none" ]]; then
  safety_stop="process-exited-unexpectedly"
elif [[ "$exit_code" -eq 0 && ( ! -f "$output_path" || ! -f "$metadata_path" ) ]]; then
  safety_stop="process-completed-without-required-output"
fi

ended_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
ended_epoch="$(date +%s)"
duration_seconds=$((ended_epoch - started_epoch))
printf 'ended_at_utc=%s\nduration_seconds=%s\ninference_exit_code=%s\nsafety_stop=%s\ndenoising_started=%s\ndenoise_event_count=%s\n' "$ended_at" "$duration_seconds" "$exit_code" "$safety_stop" "$denoising_started" "$denoise_event_count" >>"$summary_path"
if [[ "$exit_code" -ne 0 || "$safety_stop" != "none" ]]; then
  printf '%s failed with exit code %s and safety stop %s. See %s\n' "$run_id" "$exit_code" "$safety_stop" "$log_path" >&2
  exit 1
fi

output_sha256="$(shasum -a 256 "$output_path" | awk '{ print $1 }')"
output_size_bytes="$(stat -f %z "$output_path")"
metadata_sha256="$(shasum -a 256 "$metadata_path" | awk '{ print $1 }')"
printf 'output_sha256=%s\noutput_size_bytes=%s\nmetadata_sha256=%s\n' "$output_sha256" "$output_size_bytes" "$metadata_sha256" >>"$summary_path"
ffprobe -v error -show_entries stream=codec_name,pix_fmt,width,height,nb_frames,r_frame_rate,duration -show_entries format=duration,size -of json "$output_path" >"$run_root/ffprobe.json"
ffmpeg -v error -i "$output_path" -f null -
ffmpeg -v error -n -i "$output_path" -vf "select='eq(n,0)+eq(n,16)+eq(n,32)+eq(n,48)+eq(n,64)+eq(n,80)',scale=416:240,tile=3x2:padding=8:margin=8" -frames:v 1 -fps_mode vfr "$contact_sheet"
contact_sheet_sha256="$(shasum -a 256 "$contact_sheet" | awk '{ print $1 }')"
printf 'full_decode=pass\ncontact_sheet=%s\ncontact_sheet_sha256=%s\nwrapper_exit_code=0\nwrapper_closeout=normal\n' "$contact_sheet" "$contact_sheet_sha256" >>"$summary_path"

printf '%s completed in %s seconds.\n' "$run_id" "$duration_seconds"
printf 'output_sha256=%s\ncontact_sheet_sha256=%s\n' "$output_sha256" "$contact_sheet_sha256"
