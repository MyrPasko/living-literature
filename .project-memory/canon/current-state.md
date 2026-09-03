---
project: living-literature
merged_baseline: slice-001-local-video-lab-complete
active_slice: slice-002-wan-1.3b-offline-benchmark
next_slice: slice-002-wan-1.3b-offline-benchmark
active_risks: ["offline-inference-not-proven", "model-weight-revision-not-selected", "production-model-not-accepted", "human-publish-reviewer-unassigned"]
verification_reality: ["native-arm64-python-3.12.13-locked", "mlx-0.32.2-metal-and-torch-mps-verified", "wan-cli-help-passed-with-offline-flags", "no-model-weights-or-inference-in-slice-001"]
authoritative_since: 2026-09-03
---

# Current State

## Merged Baseline
- Slice 001 is complete in the local repository.
- Repo-local Memory Core V4 is installed without global skills, adapters, or automatic Obsidian sync.
- A uv-managed native arm64 CPython 3.12.13 environment is locked in `uv.lock`.
- MLX 0.32.2 imports successfully; a real Metal GPU operation and PyTorch MPS availability passed on the host.
- FFmpeg 9.0.1_1 is installed through Homebrew at `/opt/homebrew/bin/ffmpeg`.
- Apple's official MLX Wan2.1 example is a Git submodule pinned to `796f5b53cab69a3d48a44233ce21aae889e94a08`.
- `txt2video.py --help` passed with offline-library flags enabled and without model resolution, weight download, or inference.

## Next Slice
- Active: `slice-002-wan-1.3b-offline-benchmark`.
- Pin the exact `Wan-AI/Wan2.1-T2V-1.3B` model revision, download only that candidate's required files, run a declared fixed-seed benchmark, and repeat it under convincing network isolation.

## Active Risks
- Offline model inference has not been proven.
- No model-weight revision is selected or downloaded.
- `Wan2.1-T2V-1.3B` is a feasibility candidate, not an accepted production model.
- Video quality, runtime, memory behavior, thermals, and repeatability are unmeasured.
- Human editorial and legal publication review is not assigned.

## Verification Reality
- Host verification passed for arm64 Python 3.12.13, MLX 0.32.2, Metal execution, PyTorch 2.14.0 MPS availability, FFmpeg 9.0.1, the exact Wan source revision, the offline-flagged Wan help surface, ignore rules, and tracked-artifact scanning.
- A fresh environment was recreated from `uv.lock` with `uv sync --frozen --offline` using the populated uv cache.
- No model file, generated media, secret, benchmark result, or inference output was created.
