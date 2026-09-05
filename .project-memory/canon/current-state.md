---
project: living-literature
merged_baseline: slice-010-wan2.2-exact-first-last-full-render-complete-rejected-motion
active_slice: none
next_slice: owner-decision-on-corrected-hull-and-steering-oar-motion-scout
postponed_slice: slice-004-rights-ledger-foundation
active_risks: ["production-model-not-accepted", "slice-008-reference-rights-unresolved", "slice-010-hull-pitch-and-steering-oar-motion-and-rigidity-failed", "parallel-inference-out-of-scope"]
verification_reality: ["wan-14b-local-offline-byte-identical", "wan-14b-motion-gates-failed", "wan2.2-i2v-bf16-benchmark-candidate", "ltx-2.5-local-apple-route-deferred", "slice-008-motion-pass-internal-only", "slice-009-pre-denoise-resolution-rejected", "slice-010-technical-pass-motion-rejected"]
authoritative_since: 2026-09-05
---

# Current State

## Merged Baseline
- Slices 001–003 and 005–010 are merged; Slice 004 is postponed.
- Slice 005 passed local/offline execution but failed motion; Slice 007 passed technically but failed motion.

## Active Slice
- No inference slice is active. A corrected motion scout requires a new exact owner-approved slice.
- The pinned direct Wan CLI supports experimental A14B `--last-image`; the generic wrapper does not expose it.
- Slice 010 passed technical validation, but the owner rejected its hull pitch/bobbing and the steering oar's rowing-like motion and flexible-tail deformation; its marker/output exist and no retry is authorized.

## Active Risks
- No production model is accepted; technical success cannot resolve anchor rights or decide motion quality.
- The anchors remain prohibited for publication or production use.
- LTX-2.5 Fast remains deferred behind licensing, runtime, and evidence gaps.
- Parallel inference is out of scope; publication still requires human editorial and legal review.

## Verification Reality
- Slice 001 and Slice 002/005 checks pass; Slice 006 used only public metadata and FFmpeg extraction from existing outputs.
- Slice 010 used its single launch. Any retry, offline duplicate, tuning, download, runtime installation, or concurrency claim requires another exact owner-approved slice.
