---
project: living-literature
merged_baseline: slice-007-wan-2.2-i2v-a14b-motion-scout-complete-rejected
active_slice: none
next_slice: owner-decision-required-after-slice-009-pre-denoise-resolution-rejection
postponed_slice: slice-004-rights-ledger-foundation
active_risks: ["production-model-not-accepted", "slice-008-reference-rights-unresolved", "wan2.2-full-run-envelope-unmeasured", "parallel-inference-out-of-scope"]
verification_reality: ["wan-14b-local-offline-byte-identical", "wan-14b-motion-gates-failed", "wan2.2-i2v-bf16-benchmark-candidate", "ltx-2.5-local-apple-route-deferred", "slice-007-technical-pass-motion-rejected", "slice-008-motion-pass-internal-only", "slice-009-pre-denoise-resolution-contract-rejected"]
authoritative_since: 2026-09-05
---

# Current State

## Merged Baseline
- Slices 001–003 and 005–007 are merged; Slice 004 is postponed. Slice 008 is complete and unmerged.
- Slice 005 passed local/offline execution but failed motion; Slice 007 passed technically but failed motion.

## Active Slice
- No slice is active. Slice 009 stopped before denoising because `source-aspect` resolved 832×480 to 848×480.
- The pinned direct Wan CLI supports experimental A14B `--last-image`; the generic wrapper does not expose it.
- Slice 009 produced no video; its marker remains and no retry is authorized.

## Active Risks
- No production model is accepted; Slice 009 cannot resolve anchor rights.
- The anchors remain prohibited for publication or production use.
- LTX-2.5 Fast remains deferred behind licensing, runtime, and evidence gaps.
- Parallel inference is out of scope; publication still requires human editorial and legal review.

## Verification Reality
- Slice 001 and Slice 002/005 checks pass; Slice 006 used only public metadata and FFmpeg extraction from existing outputs.
- Any corrected launch, retry, offline duplicate, tuning, download, runtime installation, or concurrency claim requires a new exact owner-approved slice.
