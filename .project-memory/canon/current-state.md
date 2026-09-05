---
project: living-literature
merged_baseline: slice-007-wan-2.2-i2v-a14b-motion-scout-complete-rejected
active_slice: slice-010-wan2.2-exact-first-last-full-render-owner-review
next_slice: owner-motion-verdict-on-slice-010-video
postponed_slice: slice-004-rights-ledger-foundation
active_risks: ["production-model-not-accepted", "slice-008-reference-rights-unresolved", "slice-010-owner-motion-review-pending", "parallel-inference-out-of-scope"]
verification_reality: ["wan-14b-local-offline-byte-identical", "wan-14b-motion-gates-failed", "wan2.2-i2v-bf16-benchmark-candidate", "ltx-2.5-local-apple-route-deferred", "slice-008-motion-pass-internal-only", "slice-009-pre-denoise-resolution-rejected", "slice-010-technical-pass-owner-review-pending"]
authoritative_since: 2026-09-05
---

# Current State

## Merged Baseline
- Slices 001–003 and 005–007 are merged; Slice 004 is postponed. Slice 008 is complete and unmerged.
- Slice 005 passed local/offline execution but failed motion; Slice 007 passed technically but failed motion.

## Active Slice
- Slice 010 completed one exact 832×480 Wan2.2 first/last-frame render and awaits owner motion review.
- The pinned direct Wan CLI supports experimental A14B `--last-image`; the generic wrapper does not expose it.
- Slice 010 passed technical validation; its marker/output exist and no retry is authorized.

## Active Risks
- No production model is accepted; technical success cannot resolve anchor rights or decide motion quality.
- The anchors remain prohibited for publication or production use.
- LTX-2.5 Fast remains deferred behind licensing, runtime, and evidence gaps.
- Parallel inference is out of scope; publication still requires human editorial and legal review.

## Verification Reality
- Slice 001 and Slice 002/005 checks pass; Slice 006 used only public metadata and FFmpeg extraction from existing outputs.
- Slice 010 used its single launch. Any retry, offline duplicate, tuning, download, runtime installation, or concurrency claim requires another exact owner-approved slice.
