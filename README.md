# Living Literature

Living Literature is a local-first research project for short cinematic entrances into public-domain literature. The work should lead viewers toward reading rather than replace the source text.

The repository now proves the Slice 005 capability boundary: BigBoy ran the exact pinned Wan2.1-T2V-14B model locally and reproduced a byte-identical result under OS-enforced network denial. The 14B result passed image quality, color, atmosphere, resource, and offline gates but failed physical motion hard gates, so it is not an accepted production model.

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

No API key or cloud generation service belongs in the inference path. See `docs/local-video-environment.md` for the environment boundary, `docs/slice-002-wan-1.3b-benchmark.md` for the 1.3B control, and `docs/slice-005-wan-2.1-t2v-14b-benchmark.md` for the measured 14B evidence.

## Reproduce the Slice 002 Benchmark

The model revision, file set, prompt, and parameters are fixed in tracked manifests. The runtime cache and generated videos are intentionally ignored.

```sh
.venv/bin/python scripts/download-wan-1.3b.py
./scripts/run-slice-002-benchmark.sh online
./scripts/run-slice-002-benchmark.sh offline
.venv/bin/python scripts/verify-slice-002.py
```

The offline command uses macOS `sandbox-exec` to deny network access. Do not edit the runner while either long-running command is active.

## Reproduce the Slice 005 Benchmark

The 14B revision, ten-file runtime allowlist, fixed prompt, parameters, safety gates, and external model store are tracked. Expect approximately 3.3–3.7 hours per full run on the measured BigBoy configuration.

```sh
.venv/bin/python scripts/download-wan-14b.py
.venv/bin/python scripts/verify-slice-005.py --model-only
./scripts/run-slice-005-benchmark.sh online
./scripts/run-slice-005-benchmark.sh offline
.venv/bin/python scripts/verify-slice-005.py
```

The measured rejection is intentional evidence, not a request to tune the prompt inside Slice 005. Future prompt and cross-model work must use a new exact slice.

## Model Storage

New model caches are stored outside the checkout under `~/models/huggingface/hub`. The Slice 005 tools accept `LIVING_LITERATURE_MODEL_STORE` or `--model-store` as an explicit override. Ollama is not used for Wan video diffusion because it cannot execute the pinned Apple MLX video pipeline.

The older repository-local Slice 002 cache is retained only because its immutable manifest and verifier reference that exact evidence location. Do not move it during another benchmark slice.

## Project Authority

Repository-local `.project-memory/` is authoritative for active state, constraints, verification commands, and workflow. Obsidian is the durable planning and summary surface.
