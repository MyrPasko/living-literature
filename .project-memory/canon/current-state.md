---
project: living-literature
merged_baseline: slice-006-wan-2.2-i2v-a14b-decision-gate-complete
active_slice: none
next_slice: slice-007-wan-2.2-i2v-a14b-motion-scout
postponed_slice: slice-004-rights-ledger-foundation
active_risks: ["production-model-not-accepted", "wan2.2-scout-and-full-envelope-unmeasured", "parallel-inference-out-of-scope"]
verification_reality: ["wan-14b-local-offline-byte-identical", "wan-14b-motion-gates-failed", "wan2.2-i2v-bf16-benchmark-candidate", "source-still-d-frame-48-pinned", "ltx-2.5-local-apple-route-deferred", "slice-006-no-inference"]
authoritative_since: 2026-09-04
---

# Current State

## Merged Baseline
- Slices 001–003, 005, and 006 are complete; Slice 004 remains postponed.
- Slice 005 proved local/network-denied Wan2.1 T2V 14B execution with byte-identical output and safe measured resources, but forward-wake and wind/water failures rejected production use.

## Next Slice
- Slice 006 selected Wan2.2 I2V-A14B BF16 through MLX-Gen 0.33.1 and pinned Git-ignored candidate D: Slice 005 frame 48 at `00:00:03.000`, SHA-256 `7e7f0a20ebaa62551cad700d7e17fecd0fdc68a7003c9e1eb2e846f7fd6ec0c7`.
- `slice-007-wan-2.2-i2v-a14b-motion-scout` requires a separate plan; no runtime install, weight download, or inference is authorized yet.
- `slice-004-rights-ledger-foundation` remains postponed without renumbering or deletion.

## Active Risks
- No production model is accepted; Wan2.2 full-run resources and quality remain unmeasured.
- LTX-2.5 Fast is locally viable on Apple Silicon but deferred behind its custom license, gated weights, beta runtime, and missing comparable M5 Max evidence.
- Parallel inference is out of scope; publication still requires human editorial and legal review.

## Verification Reality
- Slice 001 and Slice 002/005 checks pass; Slice 006 used only public metadata and FFmpeg extraction from existing outputs.
- Any download, runtime installation, motion scout, longer run, or concurrency claim requires a new exact owner-approved slice.
