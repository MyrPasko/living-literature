---
project: living-literature
merged_baseline: slice-007-wan-2.2-i2v-a14b-motion-scout-complete-rejected
active_slice: none
next_slice: owner-decision-required-after-slice-008-motion-pass
postponed_slice: slice-004-rights-ledger-foundation
active_risks: ["production-model-not-accepted", "slice-008-reference-rights-unresolved", "wan2.2-full-run-envelope-unmeasured", "parallel-inference-out-of-scope"]
verification_reality: ["wan-14b-local-offline-byte-identical", "wan-14b-motion-gates-failed", "wan2.2-i2v-bf16-benchmark-candidate", "ltx-2.5-local-apple-route-deferred", "slice-007-technical-pass-motion-rejected", "slice-008-technical-and-owner-motion-pass-internal-only"]
authoritative_since: 2026-09-05
---

# Current State

## Merged Baseline
- The merged baseline contains completed Slices 001–003 and 005–007; Slice 004 remains postponed. Slice 008 is complete on its current branch and is not merged.
- Slice 005 proved local/offline Wan2.1 T2V 14B execution, but motion failed. Slice 007 passed Wan2.2 I2V-A14B technical checks, but reverse travel, wind/water causality, and speed failures rejected motion.

## Active Slice
- No slice is active. Slice 008 consumed its single authorized first/last-frame inference attempt; technical validation and all twelve owner motion gates passed.
- The pinned direct Wan CLI supports experimental A14B `--last-image`; the generic wrapper does not expose it.
- The durable attempt marker and output now exist, so no second attempt is authorized or permitted by the runner.

## Active Risks
- No production model is accepted; the passed 448×256 internal scout does not measure Wan2.2 full-run resources or quality.
- The approved anchors retain unresolved user-reference lineage and remain prohibited for publication or production use.
- LTX-2.5 Fast is locally viable on Apple Silicon but deferred behind its custom license, gated weights, beta runtime, and missing comparable M5 Max evidence.
- Parallel inference is out of scope; publication still requires human editorial and legal review.

## Verification Reality
- Slice 001 and Slice 002/005 checks pass; Slice 006 used only public metadata and FFmpeg extraction from existing outputs.
- Any further inference, download, runtime installation, longer run, or concurrency claim requires a new exact owner-approved slice.
