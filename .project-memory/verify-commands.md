---
kind: verification-commands
version: 10
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

## Slice 006 Wan2.2 I2V-A14B Decision Gate
- `.venv/bin/python scripts/verify-slice-006.py --allow-pending-still` while the owner source-still selection is pending
- `.venv/bin/python scripts/verify-slice-006.py` after the selected still is pinned

## Slice 007 Wan2.2 I2V-A14B Motion Scout
- `.venv/bin/python scripts/verify-slice-007.py --configuration-only` before installing the isolated runtime or model package
- `.venv/bin/python scripts/prepare-slice-007-runtime.py` to install and verify the pinned MLX-Gen 0.33.1 runtime below `~/models`
- `.venv/bin/python scripts/download-wan2.2-i2v-a14b-bf16.py` to download and hash the exact pinned 44-file package below `~/models`
- `.venv/bin/python scripts/verify-slice-007.py --preflight` before the one authorized generation attempt
- `./scripts/run-slice-007-motion-scout.sh` exactly once; the runner refuses a second attempt after denoising starts
- `.venv/bin/python scripts/verify-slice-007.py --allow-pending-review` after technical completion and before owner motion review
- `.venv/bin/python scripts/verify-slice-007.py` after owner review; a failed review may leave unnecessary gates as `not_assessed` but must record at least one explicit failure

## Slice 008 Corrected First/Last Motion Scout
- `.venv/bin/python scripts/verify-slice-008.py --preflight` before the one authorized attempt; this checks both anchors, frozen configuration, exact runtime/model inventories, direct Wan CLI `--last-image` support, and live host safety
- `.venv/bin/python scripts/verify-slice-007.py --preflight` immediately before launch to reuse the proven model/runtime inventory check
- `./scripts/run-slice-008-motion-scout.sh` exactly once; the runner creates a durable marker before launch and refuses an existing marker or output
- `.venv/bin/python scripts/verify-slice-008.py --allow-pending-review` after technical completion and before owner motion review
- `.venv/bin/python scripts/verify-slice-008.py` after all twelve owner motion verdicts are recorded

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
- Slice 006 is documentation and benchmark design only. Its verifier reads the existing ignored Slice 005 videos and ignored Slice 006 candidate stills; it performs no download or inference.
- Slice 007 permits one local-files-only scout after the exact runtime, model inventory, source still, host safety gates, and committed configuration pass. It does not permit a duplicate, tuning, or full render.
- Slice 008’s two-anchor route must use the direct `mlxgen-generate-wan` executable because the generic wrapper does not expose `--last-image`.
- Slice 008 execution permits exactly one local-files-only first/last-frame scout after renewed checks. It authorizes no retry, tuning, duplicate, full render, parallel inference, publication, or automatic Memory Core promotion.
