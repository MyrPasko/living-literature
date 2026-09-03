---
kind: verification-commands
version: 4
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

## Lockfile Recreation
- `recreate_dir="$(mktemp -d /private/tmp/living-literature-lock.XXXXXX)"; UV_CACHE_DIR=.cache/uv UV_PYTHON_INSTALL_DIR=.python UV_PROJECT_ENVIRONMENT="$recreate_dir/.venv" uv sync --frozen --offline`

## Repository Safety
- `rg --hidden -n '\p{Cyrillic}' -g '!.git/**' -g '!third_party/**' -g '!.venv/**' -g '!.python/**' -g '!.cache/**' .`
- `find . -type f \( -name '*.safetensors' -o -name '*.ckpt' -o -name '*.pt' -o -name '*.pth' -o -name '*.gguf' -o -name '*.mp4' -o -name '*.mov' -o -name '*.mkv' -o -name '*.webm' \) -not -path './.venv/*' -not -path './.cache/*' -print`
- `./.automation/scripts/aira-memory audit --mode project-local --fail-on-drift`

## Notes
- The MLX Metal and PyTorch MPS check must run on the actual host. A sandboxed or headless process may report no Metal device even when the host supports it.
- The Slice 001 verifier enables Hugging Face and related offline flags before the Wan CLI help check. It does not invoke a prompt.
- Generation, offline inference, benchmark, media validation, and rights-ledger verification are not registered until their owning slices implement them.
