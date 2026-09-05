---
project: living-literature
merged_baseline: slice-007-wan-2.2-i2v-a14b-motion-scout-complete-rejected
active_slice: slice-009-wan2.2-first-last-full-render-authorized
next_slice: execute-exactly-one-guarded-slice-009-full-render
postponed_slice: slice-004-rights-ledger-foundation
active_risks: ["production-model-not-accepted", "slice-008-reference-rights-unresolved", "wan2.2-full-run-envelope-unmeasured", "slice-009-one-attempt-only", "parallel-inference-out-of-scope"]
verification_reality: ["wan-14b-local-offline-byte-identical", "wan-14b-motion-gates-failed", "wan2.2-i2v-bf16-benchmark-candidate", "ltx-2.5-local-apple-route-deferred", "slice-007-technical-pass-motion-rejected", "slice-008-technical-and-owner-motion-pass-internal-only"]
authoritative_since: 2026-09-05
---

# Current State

## Merged Baseline
- Slices 001–003 and 005–007 are merged; Slice 004 is postponed. Slice 008 is complete and unmerged.
- Slice 005 passed local/offline execution but failed motion; Slice 007 passed technically but failed motion.

## Active Slice
- Slice 009 authorizes one guarded full-size Wan2.2 first/last-frame attempt after committed preflight.
- Frozen mapping: 832×480, 81 frames, 16 fps, 50 steps, seed 42, UniPC, guidance 5.0/5.0, flow shift 5.0, existing BF16 package, and unchanged Slice 008 anchors/prompts.
- The pinned direct Wan CLI supports experimental A14B `--last-image`; the generic wrapper does not expose it.
- Slice 009 has a separate durable marker and output and permits no retry.

## Active Risks
- No production model is accepted; Slice 009 cannot resolve anchor rights.
- The anchors remain prohibited for publication or production use.
- LTX-2.5 Fast remains deferred behind licensing, runtime, and evidence gaps.
- Parallel inference is out of scope; publication still requires human editorial and legal review.

## Verification Reality
- Slice 001 and Slice 002/005 checks pass; Slice 006 used only public metadata and FFmpeg extraction from existing outputs.
- Only the single exact Slice 009 attempt is authorized. Any retry, offline duplicate, tuning, download, runtime installation, or concurrency claim requires a new exact owner-approved slice.
