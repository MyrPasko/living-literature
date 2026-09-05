---
project: living-literature
merged_baseline: slice-007-wan-2.2-i2v-a14b-motion-scout-complete-rejected
active_slice: slice-008-corrected-first-last-motion-scout
next_slice: slice-008-owner-motion-review-and-closeout
postponed_slice: slice-004-rights-ledger-foundation
active_risks: ["production-model-not-accepted", "slice-008-owner-motion-review-pending", "parallel-inference-out-of-scope"]
verification_reality: ["wan-14b-local-offline-byte-identical", "wan-14b-motion-gates-failed", "wan2.2-i2v-bf16-benchmark-candidate", "ltx-2.5-local-apple-route-deferred", "slice-007-technical-pass-motion-rejected", "slice-008-technical-pass-owner-review-pending"]
authoritative_since: 2026-09-05
---

# Current State

## Merged Baseline
- Slices 001–003 and 005–007 are complete; Slice 004 remains postponed.
- Slice 005 proved local/offline Wan2.1 T2V 14B execution, but motion failed. Slice 007 passed Wan2.2 I2V-A14B technical checks, but reverse travel, wind/water causality, and speed failures rejected motion.

## Active Slice
- Slice 008 consumed its single authorized first/last-frame inference attempt. Technical validation passed; the owner’s twelve motion verdicts remain pending.
- The pinned direct Wan CLI supports experimental A14B `--last-image`; the generic wrapper does not expose it.
- The durable attempt marker and output now exist, so no second attempt is authorized or permitted by the runner.

## Active Risks
- No production model is accepted; Wan2.2 full-run resources and quality remain unmeasured.
- LTX-2.5 Fast is locally viable on Apple Silicon but deferred behind its custom license, gated weights, beta runtime, and missing comparable M5 Max evidence.
- Parallel inference is out of scope; publication still requires human editorial and legal review.

## Verification Reality
- Slice 001 and Slice 002/005 checks pass; Slice 006 used only public metadata and FFmpeg extraction from existing outputs.
- Any further inference, download, runtime installation, longer run, or concurrency claim requires a new exact owner-approved slice.
