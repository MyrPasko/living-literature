---
task_id: slice-001-local-video-lab
task_type: infra
status: complete
branch: main
date: 2026-09-03
write_scope:
  - /Users/myroslavpasko/projects/living-literature
  - /Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/Index.md
  - /Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/Architecture.md
  - /Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/BRD.md
  - /Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/Product-Principles.md
  - /Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/Slices/Slice-001-Local-Video-Lab.md
  - /Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/project-memory/canon/current-state.md
forbidden_moves:
  - model-weight download
  - video inference or media generation
  - production-model acceptance
  - GitHub remote, push, or pull request
  - global Memory Core synchronization or promotion
  - Slice 002 implementation
verification_surface:
  - native arm64 Python 3.12
  - lockfile recreation
  - MLX import and Metal execution
  - PyTorch MPS availability
  - FFmpeg availability
  - pinned Apple source
  - Wan text-to-video help path
  - ignore rules and artifact scan
  - Memory Core project-local audit
  - English-only project documentation
success_criteria:
  - all Slice 001 acceptance criteria pass
slice_restrictions:
  - stop before model-weight download or inference
---

# Implementation Result

## Plan Summary

Create and verify the first bounded Living Literature local-video environment on Apple Silicon. The slice ends at the official Apple Wan2.1 text-to-video CLI help surface and must not resolve model files or run inference.

## Exact References

- The eight Living Literature Obsidian source-of-truth notes named in the accepted request.
- `/Users/myroslavpasko/projects/memory-core/README.md` and `install-memory-core.sh` for repo-local Memory Core V4.
- `https://github.com/ml-explore/mlx-examples.git` at `796f5b53cab69a3d48a44233ce21aae889e94a08`.
- Pinned `video/wan2.1/README.md`, `requirements.txt`, `txt2video.py`, source utilities, and root `LICENSE`.
- Apple MLX installation and Metal API documentation reviewed on 2026-09-03.
- `Wan-AI/Wan2.1-T2V-1.3B` license file reviewed only as candidate metadata; no model revision or weight was selected.

## Write-Scope

- `.gitmodules`
- `third_party/`
- `.automation/`
- `.claude/`
- `.gitignore`
- `.project-memory/`
- `AGENTS.md`
- `README.md`
- `benchmarks/`
- `docs/`
- `manifests/`
- `models/`
- `outputs/`
- `prompts/`
- `pyproject.toml`
- `scripts/`
- `source-packets/`
- `uv.lock`

## External Write-Scope

- The six exact Obsidian files listed in frontmatter; no unrelated vault note was changed.
- Homebrew's FFmpeg formula and required dependencies as the explicit system package-manager change.

## Forbidden Moves

- No Wan2.1 1.3B or 14B model-weight download.
- No inference, generated image, audio, or video.
- No LTX, image model, TTS, complete Short, YouTube integration, or publication work.
- No GitHub repository, remote, push, or pull request.
- No global Memory Core synchronization, adapter installation, or candidate promotion.
- No Slice 002 implementation.

## Changes Made

- Initialized a local Git repository on `main`.
- Installed Memory Core V4 in repo-local mode. Created `.project-memory/`, `.automation/`, `.claude/`, and `AGENTS.md`; specialized only the approved project-facing Memory Core files.
- Added `pyproject.toml`, `uv.lock`, and a project-local uv runtime boundary using `.python/`, `.venv/`, and `.cache/`.
- Locked and installed Python 3.12.13 with direct packages: MLX 0.32.2, MLX Metal 0.32.2, PyTorch 2.14.0, einops 0.8.2, huggingface-hub 1.30.0, NumPy 2.5.2, Pillow 12.3.0, tokenizers 0.23.2, and tqdm 4.70.0.
- Integrated Apple's official `mlx-examples` repository as a Git submodule pinned to `796f5b53cab69a3d48a44233ce21aae889e94a08`. The local sparse checkout contains the MIT license and `video/wan2.1`.
- Added `.gitignore` boundaries for environments, Hugging Face and MLX caches, weights, generated media, transient benchmark artifacts, secrets, and macOS metadata while retaining documentation, manifests, and source fixtures.
- Added `scripts/bootstrap-wan-source.sh`, `scripts/inspect-local-environment.sh`, and `scripts/verify-local-environment.sh`.
- Added the upstream manifest, environment documentation, tracked directory boundary notes, and this durable implementation result.
- Installed Homebrew `ffmpeg 9.0.1_1` at `/opt/homebrew/bin/ffmpeg`. Homebrew installed `dav1d 1.5.4`, `mpg123 1.33.7`, `lame 4.0`, `libvmaf 3.2.0`, `libvpx 1.17.0`, `ca-certificates 2026-08-13`, `openssl@3 3.6.4`, `opus 1.6.1`, `sdl3 3.4.16`, `sdl2-compat 2.32.72`, `svt-av1 4.2.0`, `x264 r3222`, `x265 4.3`, and `xz 5.8.3`; it also refreshed two taps and did not upgrade the unrelated outdated formula it reported.
- Converted the remaining mixed-language Living Literature documentation to English and updated Obsidian project paths, Slice 001 completion, architecture, and the former bootstrap current-state note. Staged and saved versions have matching SHA-256 hashes.

## Hardware Evidence

- MacBook Pro (`Mac17,6`) with Apple M5 Max.
- Native `arm64`.
- 18 CPU cores: 6 performance and 12 efficiency.
- 40 GPU cores and Metal 4 support.
- 128 GB unified memory.
- macOS 26.6.2, build 25G83.
- Approximately 7.0 TiB free on the project volume at inspection.
- 96% system-wide memory free and zero swap used at inspection.
- `uv 0.11.29` at `/Users/myroslavpasko/.local/bin/uv`.
- Xcode Command Line Tools 26.6.0.0.1781586589 at `/Library/Developer/CommandLineTools`.
- The standalone `metal` compiler is not included in this Command Line Tools installation; runtime Metal is independently verified through MLX.

No serial number, hardware UUID, or provisioning identifier was collected or recorded.

## Verification

- `command:` `./scripts/verify-local-environment.sh` on the actual host
  - `result:` pass
  - `notes:` Python 3.12.13 arm64; MLX 0.32.2; `metal=True`; evaluated GPU sum 6; PyTorch 2.14.0; MPS built and available; FFmpeg 9.0.1; exact Wan commit; offline-flagged CLI help; representative ignore checks; tracked artifact scan.
- `command:` `UV_CACHE_DIR=.cache/uv UV_PYTHON_INSTALL_DIR=.python UV_PROJECT_ENVIRONMENT=/private/tmp/living-literature-slice-001-lock-recreation-02/.venv uv sync --frozen --offline`
  - `result:` pass
  - `notes:` created a fresh arm64 Python 3.12.13 environment from `uv.lock` and installed the locked MLX 0.32.2 distribution from the populated uv cache.
- `command:` `ffmpeg -version` and `brew list --versions ...`
  - `result:` pass
  - `notes:` `/opt/homebrew/bin/ffmpeg`, executable version 9.0.1, formula 9.0.1_1, and dependency versions recorded above.
- `command:` `git -C third_party/mlx-examples rev-parse HEAD` and `git submodule status`
  - `result:` pass
  - `notes:` both resolve `796f5b53cab69a3d48a44233ce21aae889e94a08`.
- `command:` `find` scan for model weights and generated media outside the Python and uv caches
  - `result:` pass
  - `notes:` no files found; `models/` and `outputs/` contain only boundary README files.
- `command:` Cyrillic scan across repository project files and the exact Obsidian Living Literature subtree
  - `result:` pass
  - `notes:` no mixed-language project documentation remains. Original-language literary quotations would be permitted, but none were part of this slice.
- `command:` `./.automation/scripts/aira-memory audit --mode project-local --fail-on-drift`
  - `result:` pass
  - `notes:` project-local audit exited successfully with no findings.

## Review Closeout

- A sandboxed MLX process could not see the Metal device. The check was rerun through the smallest host approval and passed with a real evaluated GPU operation.
- The initial MLX version check incorrectly assumed a package `__version__`; it now uses installed distribution metadata.
- The initial GPU smoke expression used an unsupported `device` argument; it now sets MLX's default device before evaluating the operation.
- The first lock-recreation follow-up imported the GPU backend inside the sandbox after the fresh sync and therefore failed despite successful recreation. A second fresh offline recreation verified Python, architecture, and locked MLX distribution metadata, while the separate host check verified Metal execution.
- The ignore verifier initially accepted any representative ignored path; it now checks every model, video, cache, and secret representative independently.

## Known Constraints

- Offline inference is not proven.
- No model-weight revision is selected or downloaded.
- Generation runtime, memory behavior, swap behavior under load, thermals, output validity, quality, and repeatability are unmeasured.
- The current candidate model license must be bound to the exact model revision selected in Slice 002.
- Human editorial and legal publication review remains unassigned.

## Open Findings

- None

## Exact Recommendation for Slice 002

Execute only `slice-002-wan-1.3b-offline-benchmark`: select and pin the exact `Wan-AI/Wan2.1-T2V-1.3B` revision and license evidence, declare the minimum required file set, download only those files into the ignored project-local cache, run the fixed-seed 832×480 or nearest supported 81-frame benchmark while recording time, memory, swap, thermals, output metadata, and hash, then repeat the same inference with offline flags plus convincing process-level network isolation or observation. Do not add 14B, LTX, TTS, image generation, quality optimization, or publication work.

## Distillation Candidates

**Decision**: Pin Apple `mlx-examples` as a Git submodule with a sparse local working tree.
- **Rationale**: Preserve exact upstream revision and license provenance without modifying or duplicating Apple source.
- **Alternatives considered**: copied source snapshot, unpinned clone, scripted archive download.
- **Impact**: Fresh checkouts require submodule initialization, and all updates require an explicit parent gitlink change.

- **Issue**: Sandboxed macOS processes may report no Metal device.
- **Solution**: Run the identifier-safe GPU verification through the smallest host approval.
- **Prevention**: Keep host-versus-sandbox evidence explicit in verification documentation.

No candidate is promoted by this closeout. Promotion remains a separate owner-approved action.
