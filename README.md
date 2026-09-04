# Living Literature

Living Literature is a local-first research project for short cinematic entrances into public-domain literature. The work should lead viewers toward reading rather than replace the source text.

The repository now proves the Slice 002 feasibility boundary: the exact pinned Wan2.1-T2V-1.3B candidate generated the fixed benchmark locally and reproduced a byte-identical result under OS-enforced network denial. `Wan2.1-T2V-1.3B` remains a feasibility candidate, not an accepted production model.

## Recreate the Environment

Requirements:

- Apple Silicon with macOS 14 or newer;
- `uv`;
- Git;
- FFmpeg on `PATH`;
- Xcode Command Line Tools.

```sh
UV_CACHE_DIR=.cache/uv UV_PYTHON_INSTALL_DIR=.python uv python install 3.12
UV_CACHE_DIR=.cache/uv UV_PYTHON_INSTALL_DIR=.python uv sync --frozen
./scripts/bootstrap-wan-source.sh
./scripts/verify-local-environment.sh
```

The exact Python dependency graph is stored in `uv.lock`. The Apple example is a Git submodule pinned by the parent repository and independently checked by `manifests/upstream-wan.json` and the bootstrap script.

## Network Boundary

Three operations must remain distinct:

1. Dependency and source download is allowed during controlled environment setup.
2. Model-weight download is a separate, explicit operation with exact revision and file manifests.
3. Model inference is local-only. The Slice 002 offline repeat combined library offline flags, local-only cache resolution, and macOS network denial.

No API key or cloud generation service belongs in the inference path. See `docs/local-video-environment.md` for the environment boundary and `docs/slice-002-wan-1.3b-benchmark.md` for the measured inference evidence.

## Reproduce the Slice 002 Benchmark

The model revision, file set, prompt, and parameters are fixed in tracked manifests. The runtime cache and generated videos are intentionally ignored.

```sh
.venv/bin/python scripts/download-wan-1.3b.py
./scripts/run-slice-002-benchmark.sh online
./scripts/run-slice-002-benchmark.sh offline
.venv/bin/python scripts/verify-slice-002.py
```

The offline command uses macOS `sandbox-exec` to deny network access. Do not edit the runner while either long-running command is active.

## Model Storage

New model caches are stored outside the checkout under `~/models/huggingface/hub`. The Slice 005 tools accept `LIVING_LITERATURE_MODEL_STORE` or `--model-store` as an explicit override. Ollama is not used for Wan video diffusion because it cannot execute the pinned Apple MLX video pipeline.

The older repository-local Slice 002 cache is retained only because its immutable manifest and verifier reference that exact evidence location. Do not move it during another benchmark slice.

## Project Authority

Repository-local `.project-memory/` is authoritative for active state, constraints, verification commands, and workflow. Obsidian is the durable planning and summary surface.
