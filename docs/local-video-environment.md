---
project: Living Literature
document: local-video-environment
status: verified
verified: 2026-09-03
slice: slice-001-local-video-lab
---

# Local Video Environment

## Slice Boundary

Slice 001 establishes a reproducible local environment and reaches the command-line help surface of Apple's official MLX Wan2.1 implementation. It does not download model weights, run inference, generate media, benchmark performance, or accept a production model.

`Wan2.1-T2V-1.3B` remains a feasibility candidate. Video generation and convincing offline-inference evidence belong to Slice 002.

## Verified Hardware and System Baseline

Verified on 2026-09-03 with identifier-safe commands that do not emit serial numbers, hardware UUIDs, or provisioning identifiers:

- Mac model: MacBook Pro (`Mac17,6`);
- chip: Apple M5 Max;
- architecture: `arm64`;
- CPU: 18 physical and 18 logical cores, reported as 6 performance and 12 efficiency cores;
- GPU: 40 cores;
- unified memory: 128 GB;
- graphics runtime: Metal 4 supported;
- macOS: 26.6.2, build 25G83;
- available project-volume disk space: approximately 7.0 TiB;
- memory pressure at inspection: 96% system-wide memory free;
- swap at inspection: 0 bytes configured and 0 bytes used;
- `uv`: 0.11.29 at `/Users/myroslavpasko/.local/bin/uv`;
- Xcode Command Line Tools: 26.6.0.0.1781586589 at `/Library/Developer/CommandLineTools`;
- standalone `metal` compiler lookup: not present in the Command Line Tools package;
- runtime Metal and PyTorch MPS availability: verified separately inside the locked environment.

Hardware, free disk, memory pressure, and swap are drift-prone. Re-run `./scripts/inspect-local-environment.sh` immediately before model-weight download or inference.

## Python Environment

The project uses a uv-managed CPython 3.12 installation under `.python/` and an isolated `.venv/`. Both are local-only and Git-ignored. The macOS system Python 3.9 is not used.

The direct dependency list mirrors the pinned Apple example's `video/wan2.1/requirements.txt`. Exact direct and transitive versions are locked in `uv.lock`.

Installed direct versions:

- Python 3.12.13;
- MLX 0.32.2 and MLX Metal 0.32.2;
- PyTorch 2.14.0;
- einops 0.8.2;
- huggingface-hub 1.30.0;
- NumPy 2.5.2;
- Pillow 12.3.0;
- tokenizers 0.23.2;
- tqdm 4.70.0.

```sh
UV_CACHE_DIR=.cache/uv UV_PYTHON_INSTALL_DIR=.python uv python install 3.12
UV_CACHE_DIR=.cache/uv UV_PYTHON_INSTALL_DIR=.python uv sync --frozen
```

## Apple MLX Wan2.1 Source

- upstream: `https://github.com/ml-explore/mlx-examples.git`;
- pinned commit: `796f5b53cab69a3d48a44233ce21aae889e94a08`;
- relevant source: `video/wan2.1`;
- upstream source license: MIT, preserved at `third_party/mlx-examples/LICENSE`;
- verification date: 2026-09-03;
- integration: Git submodule pinned by the parent repository, with a sparse working tree limited to `/LICENSE` and `/video/wan2.1/`;
- rationale: the submodule preserves exact upstream history and license provenance without copying or modifying Apple's source, while sparse checkout keeps the active working tree bounded.

The candidate model weights are a separate artifact hosted under `Wan-AI/Wan2.1-T2V-1.3B`. No weight revision is selected or downloaded in this slice. The model repository currently presents an Apache-2.0 license file, but model acceptance and exact weight revision pinning remain Slice 002 gates.

Bootstrap or repair the source checkout with:

```sh
./scripts/bootstrap-wan-source.sh
```

To update in a future explicitly approved slice:

1. inspect the new upstream commit, Wan files, requirements, and root license;
2. check out the approved exact commit inside `third_party/mlx-examples`;
3. update `manifests/upstream-wan.json` and both verification scripts;
4. refresh `pyproject.toml` and `uv.lock` if upstream requirements changed;
5. rerun all repository verification;
6. commit the parent repository's updated Git submodule pointer.

Never use `git submodule update --remote` as a reproducible setup step.

## FFmpeg

FFmpeg was absent at the start of Slice 001. It was installed with the standard Apple Silicon Homebrew mechanism:

```sh
brew install ffmpeg
```

The installation added the `ffmpeg` formula and its required Homebrew dependencies: `dav1d`, `mpg123`, `lame`, `libvmaf`, `libvpx`, `ca-certificates`, `openssl@3`, `opus`, `sdl3`, `sdl2-compat`, `svt-av1`, `x264`, `x265`, and `xz`. Homebrew also refreshed its two configured taps before installation; it did not upgrade the one unrelated outdated formula it reported.

The resolved binary is `/opt/homebrew/bin/ffmpeg`, and the installed formula is `ffmpeg 9.0.1_1` (`ffmpeg version 9.0.1`). Exact dependency formula versions are recorded in the Slice 001 implementation result and can be rechecked with `brew list --versions`.

## Download and Offline Boundary

These are three separate operations:

1. **Dependency and source download:** allowed during controlled setup; completed for Python packages, FFmpeg, and Apple source.
2. **Future model-weight download:** not performed; requires an explicit Slice 002 action and an exact model revision.
3. **Model inference:** not performed; must run locally without API keys or cloud text encoding, prompt enhancement, TTS, image generation, or video generation.

Prepare future Hugging Face access with project-local cache paths. After the explicit weight preload, use the offline flags below:

```sh
export HF_HOME="$PWD/.cache/huggingface"
export HF_HUB_CACHE="$HF_HOME/hub"
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export DIFFUSERS_OFFLINE=1
```

These flags tell compatible libraries to use cached files, but flags alone are not proof that a process made no network calls. Slice 002 must combine them with an exact weight manifest and convincing process-level network isolation or observation during a repeated inference run.

## Verification

Run:

```sh
./scripts/verify-local-environment.sh
./.automation/scripts/aira-memory audit --mode project-local --fail-on-drift
```

The help check enables the future offline flags before invoking `txt2video.py --help`. Argument parsing exits before `WanPipeline` is instantiated, so it exercises imports and the CLI surface without requesting weights or running inference.
