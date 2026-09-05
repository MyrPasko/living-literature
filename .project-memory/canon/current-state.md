---
project: living-literature
merged_baseline: slice-006-wan-2.2-i2v-a14b-decision-gate-complete
active_slice: slice-007-wan-2.2-i2v-a14b-motion-scout
next_slice: pending-slice-007-motion-verdict
postponed_slice: slice-004-rights-ledger-foundation
active_risks: ["production-model-not-accepted", "wan2.2-scout-and-full-envelope-unmeasured", "parallel-inference-out-of-scope"]
verification_reality: ["wan-14b-local-offline-byte-identical", "wan-14b-motion-gates-failed", "wan2.2-i2v-bf16-benchmark-candidate", "source-still-d-frame-48-pinned", "ltx-2.5-local-apple-route-deferred", "slice-006-no-inference", "slice-007-technical-pass-owner-review-pending"]
authoritative_since: 2026-09-05
---

# Current State

## Merged Baseline
- Slices 001–003, 005, and 006 are complete; Slice 004 remains postponed.
- Slice 005 proved local/network-denied Wan2.1 T2V 14B execution with byte-identical output and safe measured resources, but forward-wake and wind/water failures rejected production use.

## Active Slice
- The owner accepted the exact `slice-007-wan-2.2-i2v-a14b-motion-scout` plan on 2026-09-05.
- Slice 007 authorizes the pinned MLX-Gen 0.33.1 runtime, exact 44-file BF16 package, Git-ignored candidate D, and one sequential 448×256-requested motion scout only.
- The one authorized scout completed in 272 seconds with no safety stop, zero sampled swap, 89% minimum memory free, and a passing full decode; output SHA-256 is `112805f168d717825e11ce3b9796dedbb6ddb07f83e6fc97507a9da6768a9656`.
- The technical result is frozen while the owner reviews all ten motion hard gates. No route verdict is recorded yet.
- The next slice depends on the owner motion verdict; no full render, duplicate run, tuning, or production acceptance is authorized.
- `slice-004-rights-ledger-foundation` remains postponed without renumbering or deletion.

## Active Risks
- No production model is accepted; Wan2.2 full-run resources and quality remain unmeasured.
- LTX-2.5 Fast is locally viable on Apple Silicon but deferred behind its custom license, gated weights, beta runtime, and missing comparable M5 Max evidence.
- Parallel inference is out of scope; publication still requires human editorial and legal review.

## Verification Reality
- Slice 001 and Slice 002/005 checks pass; Slice 006 used only public metadata and FFmpeg extraction from existing outputs.
- Any download, runtime installation, motion scout, longer run, or concurrency claim requires a new exact owner-approved slice.
