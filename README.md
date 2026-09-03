# Living Literature

Living Literature is a local-first research project for short cinematic entrances into public-domain literature. The work should lead viewers toward reading rather than replace the source text.

The repository currently proves only the Slice 001 environment boundary: a native Apple Silicon Python environment can load MLX and reach the help surface of Apple's Wan2.1 text-to-video example. `Wan2.1-T2V-1.3B` remains a feasibility candidate, not an accepted production model.

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
2. Model-weight download is a separate, explicit Slice 002 operation.
3. Model inference is local-only and is not executed in Slice 001.

No API key or cloud generation service belongs in the inference path. See `docs/local-video-environment.md` for the offline flags and the evidence boundary.

## Project Authority

Repository-local `.project-memory/` is authoritative for active state, constraints, verification commands, and workflow. Obsidian is the durable planning and summary surface.
