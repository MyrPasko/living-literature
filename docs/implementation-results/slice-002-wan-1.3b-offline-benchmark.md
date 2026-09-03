---
task_id: slice-002-wan-1.3b-offline-benchmark
task_type: feature
status: complete
branch: main
date: 2026-09-03
write_scope:
  - /Users/myroslavpasko/projects/living-literature
  - /Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/Index.md
  - /Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/Slices/Slice-002-Wan-1.3B-Offline-Benchmark.md
  - /Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/project-memory/canon/current-state.md
forbidden_moves:
  - 14B or LTX download and inference
  - prompt tuning
  - production-model acceptance
  - image-to-video, audio, complete Short, or publication work
  - automatic Memory Core promotion
  - GitHub push or pull request
verification_surface:
  - exact model revision, file set, sizes, and hashes
  - fixed benchmark parameters
  - online-capable local inference
  - offline inference under OS network denial
  - runtime, memory, swap, disk, and thermal observations
  - MP4 metadata, hash, and full decode
  - normal-speed and sampled-frame quality review
  - repository safety and Memory Core audit
success_criteria:
  - all Slice 002 acceptance criteria pass
slice_restrictions:
  - stop before any heavier model download or inference
---

# Implementation Result

## Plan Summary

Pin and download only the required Wan2.1-T2V-1.3B files, run the declared fixed-seed benchmark locally, repeat it under convincing network denial, and record factual machine and quality evidence without accepting a production model.

## Exact References

- `Wan-AI/Wan2.1-T2V-1.3B` at `37ec512624d61f7aa208f7ea8140a131f93afc9a`.
- Model license and model card at the exact Hugging Face revision.
- Apple `mlx-examples/video/wan2.1` at `796f5b53cab69a3d48a44233ce21aae889e94a08`.
- Obsidian Slice 002 and Slice 003 notes under the exact Living Literature project subtree.
- `benchmarks/slice-002-wan-1.3b.json` as the immutable prompt and parameter source.

## Write-Scope

- `.project-memory/`
- `.automation/workspace/`
- `AGENTS.md`
- `README.md`
- `benchmarks/`
- `docs/`
- `manifests/`
- `outputs/`
- `scripts/`
- `/Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/Index.md`
- `/Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/Slices/Slice-002-Wan-1.3B-Offline-Benchmark.md`
- `/Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/project-memory/canon/current-state.md`

## Forbidden Moves

- No Wan 14B, Wan image-to-video, LTX, prompt extension, prompt-tuning loop, TTS, music, full Short, YouTube integration, or publication work.
- No production-model acceptance.
- No automatic Memory Core promotion.
- No GitHub push or pull request.

## Changes Made

- Attached the user-provided empty GitHub repository as `origin`; no push was performed.
- Pinned the Wan2.1-T2V-1.3B model revision and downloaded only its four runtime files plus exact license and model-card evidence into the ignored project-local Hugging Face cache.
- Verified 17,562,466,409 downloaded bytes against recorded file sizes and SHA-256 hashes.
- Added a guarded Python runner that rejects any unexpected repository or model-file request and always binds requests to the exact revision.
- Added an online/offline benchmark wrapper with memory, swap, disk, and thermal sampling and automatic safety stops at 10% free memory, 32 GiB swap, or 100 GiB free disk.
- Added an offline preflight that requires macOS network denial to reject a loopback socket bind before inference.
- Ran the fixed benchmark online-capable and again with Hugging Face offline flags, `local_files_only=True`, and macOS `(deny network*)`.
- Added a verifier that re-hashes cached runtime files, validates exact request logs, checks output hashes and video metadata, and fully decodes both MP4s.
- Reviewed normal-speed playback plus representative frames and recorded a factual quality rubric.
- Updated active state to Slice 003, the existing Quality and Model Gate, without authorizing another download or inference.

## Benchmark Evidence

- Fixed seed 42; 832×480; 81 frames; 50 steps; guidance 5.0; shift 5.0; UniPC; no quantization; TeaCache disabled; 16 fps.
- Online inference: 1,989.82 seconds; MLX peak 25.693 GB; minimum observed free memory 57%; zero swap; no warning.
- Offline inference: 2,200.93 seconds, 2,222 seconds wrapper wall time; MLX peak 25.693 GB; minimum observed free memory 56%; zero swap; no warning.
- Both outputs: H.264, 832×480, 81 frames, 16 fps, 5.0625 seconds, 615,420 bytes.
- Both outputs: SHA-256 `9984555b3918a56c0ad8f4043b234cdbec2ba15bbaffc46e49eddae86838390f`.
- Offline network-denial preflight: pass.

## Quality Evidence

- Strong dark wine-purple sea, pre-dawn cloudscape, cinematic mood, object stability, and restrained motion.
- No text, watermark, or obvious modern object.
- The vessel is a coherent black silhouette, but its two-masted form is generic rather than unmistakably Bronze Age Greek.
- Wind-driven sail motion is subtle.
- Result is a useful feasibility control and mood draft, not a production-model acceptance.

## Verification

- `command:` `.venv/bin/python scripts/download-wan-1.3b.py`
  - `result:` pass
  - `notes:` exact revision, six declared files, sizes, SHA-256 hashes, and Apache-2.0 license snapshot verified.
- `command:` `./scripts/run-slice-002-benchmark.sh online`
  - `result:` pass with wrapper closeout finding
  - `notes:` inference and MP4 save succeeded; wrapper finalization was independently recovered after its live file was edited.
- `command:` `./scripts/run-slice-002-benchmark.sh offline`
  - `result:` pass
  - `notes:` network denial preflight, inference, output hash, FFprobe, and wrapper closeout all passed.
- `command:` `.venv/bin/python scripts/verify-slice-002.py`
  - `result:` pass
  - `notes:` cache hashes, exact requests, offline marker, video hashes, metadata, and full decodes passed.
- `check:` normal-speed QuickTime playback and representative frame review
  - `result:` pass with quality limitations
  - `notes:` stable and coherent mood shot; insufficient Bronze Age specificity for production acceptance.

## Review Closeout

- The first long-running shell was patched while active and encountered an unexpected EOF only after the inference process and MP4 save completed. The successful model log, time metrics, safety samples, media metadata, output hash, and full decode were recovered. The offline run was then executed without modifying its entrypoints and completed normally.
- The offline preflight originally tested socket creation, which macOS allowed without network traffic. It was strengthened to require loopback socket binding to fail under the deny-network profile.
- Process RSS sampling targeted the `/usr/bin/time` wrapper and was not useful. Final resource reporting therefore uses macOS `/usr/bin/time` maximum resident set and peak footprint together with MLX peak memory and system-wide memory/swap samples. A future benchmark runner should sample the descendant process tree directly.

## Open Findings

- None

## Exact Recommendation for Slice 003

Execute only `slice-003-quality-and-model-gate`. Use the measured 1.3B quality and resource evidence, current primary-source documentation, exact licenses, download-size estimates, and conservative memory/runtime projections to select one next approach. The present evidence supports evaluating a heavier model, but Slice 003 itself must remain a decision gate and must not download or run it.

## Distillation Candidates

**Decision**: Treat the 1.3B result as a reproducible control, not a production-model acceptance.
- **Rationale**: Offline repeatability and resource headroom passed, while historical specificity remains insufficient.
- **Alternatives considered**: accept 1.3B immediately, tune the prompt inside Slice 002, or download 14B before closeout.
- **Impact**: Slice 003 can compare one heavier or more controllable approach against measured evidence without losing the baseline.

- **Issue**: Editing a long-running script while Bash was still reading it broke wrapper finalization.
- **Solution**: Preserve and independently validate the completed inference evidence, freeze the runner, and complete the offline repeat normally.
- **Prevention**: Never patch active entrypoints; prepare changes in a separate file and apply them only after all dependent processes exit.

- **Pattern Name**: Offline inference proof by layered denial.
- **New Solution**: Combine exact revision pinning, an allowlisted file set, local-only resolution, library offline flags, an OS network-denial sandbox, and a socket-bind denial preflight.
- **Reusable Insight**: Cache success alone does not prove offline operation; enforced network denial plus a successful repeated artifact does.

No candidate is promoted by this closeout. Promotion remains a separate owner-approved action.
