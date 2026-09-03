---
project: living-literature
merged_baseline: slice-002-wan-1.3b-offline-benchmark-complete
active_slice: slice-003-quality-and-model-gate
next_slice: slice-003-quality-and-model-gate
active_risks: ["production-model-not-accepted", "bronze-age-specificity-insufficient", "heavier-model-resource-boundary-unmeasured", "human-publish-reviewer-unassigned"]
verification_reality: ["wan-1.3b-revision-and-four-runtime-files-pinned", "online-and-network-denied-offline-inference-passed", "outputs-byte-identical", "mlx-peak-memory-25.693-gb", "zero-swap-and-no-warning-observed"]
authoritative_since: 2026-09-03
---

# Current State

## Merged Baseline
- Slices 001 and 002 are complete in the local repository.
- Native arm64 CPython 3.12.13, MLX 0.32.2 Metal, PyTorch 2.14.0 MPS, and FFmpeg 9.0.1 are verified.
- Apple's MLX Wan2.1 source is pinned to `796f5b53cab69a3d48a44233ce21aae889e94a08`.
- `Wan-AI/Wan2.1-T2V-1.3B` is pinned to `37ec512624d61f7aa208f7ea8140a131f93afc9a`; the exact four-file runtime set and license evidence are checksum-verified.
- Online-capable and network-denied offline runs produced byte-identical 832×480, 81-frame MP4s at SHA-256 `9984555b3918a56c0ad8f4043b234cdbec2ba15bbaffc46e49eddae86838390f`.
- Offline wall time was 2,222 seconds; MLX peak was 25.693 GB; minimum free memory was 56%; swap and warning count were zero.

## Next Slice
- Active: `slice-003-quality-and-model-gate`.
- Select one next approach and define its download, resource, license, and benchmark boundary.
- Slice 003 authorizes no new model download or inference.

## Active Risks
- No production model is accepted; 1.3B lacks Bronze Age specificity and strong sail motion.
- BigBoy's heavier-model quality, runtime, memory, swap, and thermal boundaries remain unmeasured.
- Human editorial and legal publication review is not assigned.

## Verification Reality
- Slice 001 host and lockfile checks remain green; the Slice 002 verifier passed cache hashes, request pins, offline denial, media metadata, hashes, and full decodes.
- Playback showed stable restrained motion and no forbidden content, with insufficient historical specificity.
- The online wrapper closeout was recovered after a live-runner edit; offline closeout was normal. See the Slice 002 report.
