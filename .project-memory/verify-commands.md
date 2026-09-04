---
kind: verification-commands
version: 5
---

# Verification Commands

## Setup Reproduction
- `UV_CACHE_DIR=.cache/uv UV_PYTHON_INSTALL_DIR=.python uv python install 3.12`
- `UV_CACHE_DIR=.cache/uv UV_PYTHON_INSTALL_DIR=.python uv sync --frozen`
- `./scripts/bootstrap-wan-source.sh`

## Slice 001 Environment
- `./scripts/inspect-local-environment.sh`
- `./scripts/verify-local-environment.sh`
- `git submodule status third_party/mlx-examples`
- `ffmpeg -version`
- `UV_CACHE_DIR=.cache/uv UV_PYTHON_INSTALL_DIR=.python uv tree --locked --depth 1`

## Slice 002 Wan 1.3B Benchmark
- `.venv/bin/python scripts/download-wan-1.3b.py`
- `./scripts/run-slice-002-benchmark.sh online`
- `./scripts/run-slice-002-benchmark.sh offline`
- `.venv/bin/python scripts/verify-slice-002.py`
- `ffprobe -v error -show_entries stream=codec_name,width,height,nb_frames,r_frame_rate,duration -show_entries format=duration,size -of json outputs/slice-002/wan-1.3b-offline-seed-42.mp4`

## Slice 005 Wan T2V 14B Benchmark
- `.venv/bin/python scripts/download-wan-14b.py`
- `.venv/bin/python scripts/verify-slice-005.py --model-only`
- `./scripts/run-slice-005-benchmark.sh online`
- `./scripts/run-slice-005-benchmark.sh offline`
- `.venv/bin/python scripts/verify-slice-005.py`

## Lockfile Recreation
- `recreate_dir="$(mktemp -d /private/tmp/living-literature-lock.XXXXXX)"; UV_CACHE_DIR=.cache/uv UV_PYTHON_INSTALL_DIR=.python UV_PROJECT_ENVIRONMENT="$recreate_dir/.venv" uv sync --frozen --offline`

## Repository Safety
- `rg --hidden -n '\p{Cyrillic}' -g '!.git/**' -g '!third_party/**' -g '!.venv/**' -g '!.python/**' -g '!.cache/**' .`
- `find . -type f \( -name '*.safetensors' -o -name '*.ckpt' -o -name '*.pt' -o -name '*.pth' -o -name '*.gguf' -o -name '*.mp4' -o -name '*.mov' -o -name '*.mkv' -o -name '*.webm' \) -not -path './.venv/*' -not -path './.cache/*' -print`
- `./.automation/scripts/aira-memory audit --mode project-local --fail-on-drift`

## Notes
- The MLX Metal and PyTorch MPS check must run on the actual host. A sandboxed or headless process may report no Metal device even when the host supports it.
- The Slice 001 verifier enables Hugging Face and related offline flags before the Wan CLI help check. It does not invoke a prompt.
- Slice 002 generation, offline inference, benchmark, and media validation are registered. Generated videos and detailed runtime artifacts remain local and Git-ignored; tracked manifests contain their hashes and measurements.
- Run host inference only after reviewing the fixed benchmark manifest and current safety thresholds. Never edit the runner while it is active.
- Rights-ledger verification is not registered until its owning slice implements it.
- Slice 005 stores new weights under `~/models/huggingface/hub`; `LIVING_LITERATURE_MODEL_STORE` may override that location explicitly.
