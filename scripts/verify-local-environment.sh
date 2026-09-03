#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
expected_wan_commit="796f5b53cab69a3d48a44233ce21aae889e94a08"
python_bin="$repo_root/.venv/bin/python"

export HF_HOME="$repo_root/.cache/huggingface"
export HF_HUB_CACHE="$HF_HOME/hub"
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export DIFFUSERS_OFFLINE=1

[[ -x "$python_bin" ]] || { printf 'Missing project Python: %s\n' "$python_bin" >&2; exit 1; }

python_arch="$($python_bin -c 'import platform; print(platform.machine())')"
python_version="$($python_bin -c 'import platform; print(platform.python_version())')"
[[ "$python_arch" == "arm64" ]]
[[ "$python_version" == 3.12.* ]]
printf 'python=%s architecture=%s\n' "$python_version" "$python_arch"

$python_bin -c 'from importlib.metadata import version; import mlx.core as mx; assert mx.metal.is_available(); mx.set_default_device(mx.gpu); value = mx.sum(mx.array([1, 2, 3])); mx.eval(value); print("mlx={} metal={} gpu_sum={}".format(version("mlx"), mx.metal.is_available(), value.item()))'
$python_bin -c 'import torch; assert torch.backends.mps.is_built(); assert torch.backends.mps.is_available(); print(f"torch={torch.__version__} mps_built={torch.backends.mps.is_built()} mps_available={torch.backends.mps.is_available()}")'

ffmpeg -version 2>&1 | sed -n '1p'

actual_wan_commit="$(git -C "$repo_root/third_party/mlx-examples" rev-parse HEAD)"
[[ "$actual_wan_commit" == "$expected_wan_commit" ]]
printf 'wan_commit=%s\n' "$actual_wan_commit"

help_output="$(cd "$repo_root/third_party/mlx-examples/video/wan2.1" && "$python_bin" txt2video.py --help)"
grep -q 'Generate videos from text using Wan2.1' <<<"$help_output"
grep -q -- '--model' <<<"$help_output"
printf 'wan_help=pass offline_flags=enabled\n'

while IFS= read -r ignored_path; do
  git -C "$repo_root" check-ignore --quiet "$ignored_path"
done <<'EOF'
.cache/huggingface/hub/models--example/model.safetensors
models/Wan2.1-T2V-1.3B/model.safetensors
outputs/example.mp4
.env.local
EOF
printf 'gitignore_representatives=pass\n'

if git -C "$repo_root" ls-files | grep -E '(^|/)(\.env($|\.)|.*\.(safetensors|ckpt|pt|pth|gguf|onnx|mp4|mov|mkv|webm|wav|mp3|m4a)$)' >/dev/null; then
  printf 'Tracked secret, model, or generated-media candidate found.\n' >&2
  exit 1
fi
printf 'tracked_artifact_scan=pass\n'
