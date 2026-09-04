---
project: living-literature
merged_baseline: slice-005-wan-2.1-t2v-14b-benchmark-complete
active_slice: none
next_slice: slice-006-flagship-video-model-comparison-gate
postponed_slice: slice-004-rights-ledger-foundation
active_risks: ["production-model-not-accepted", "pure-t2v-motion-physics-failed", "next-flagship-benchmark-unselected", "parallel-14b-inference-unproven", "human-publish-reviewer-unassigned"]
verification_reality: ["wan-14b-local-runtime-proven", "wan-14b-network-denied-repeat-byte-identical", "wan-14b-quality-hard-gates-failed", "wan-14b-external-store-under-home-models"]
authoritative_since: 2026-09-04
---

# Current State

## Merged Baseline
- Slices 001–003 and 005 are complete; Slice 004 remains postponed.
- Slice 005 ran Wan2.1 T2V 14B revision `a064a6c71f5be440641209c07bf2a5ce7a2ff5e4` through Apple `796f5b53cab69a3d48a44233ce21aae889e94a08`, 8-bit DiT, from the 64.299 GiB external runtime set.
- Online/offline runs took 13,061/12,038 seconds, peaked at 29.722 GB MLX, kept swap at zero, and produced byte-identical 832×480 H.264 output with SHA-256 `ce7a61c21ef0811062ea6229b3ddf89c6843bdc6569234cab060915bd39f2ad4`.
- Image quality, color, atmosphere, and ancient silhouette passed. Filled-sail/calm-sea inconsistency and a forward wake failed motion hard gates; no production model is accepted.

## Next Slice
- `slice-006-flagship-video-model-comparison-gate` must refresh exact candidates and select bounded future benchmarks; it authorizes no download or inference by itself.
- Reuse the causal prompt and low-cost motion-scout requirements in `docs/t2v-prompt-motion-analysis.md`.
- `slice-004-rights-ledger-foundation` remains postponed without renumbering or deletion.

## Active Risks
- No production model is accepted; pure T2V motion physics failed despite strong visual direction.
- No next flagship checkpoint or Apple Silicon path is selected. Parallel 14B execution is unmeasured and not authorized.
- Human editorial and legal publication review is not assigned.

## Verification Reality
- Slice 001 host checks and Slice 002/005 deterministic verifiers pass.
- Wan 14B runs locally and offline on BigBoy within the declared four-hour, memory, swap, disk, and thermal gates.
- Another model, prompt rewrite, scout configuration, longer duration, or concurrency claim requires a new exact slice.
