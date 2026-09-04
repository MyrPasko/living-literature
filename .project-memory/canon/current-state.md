---
project: living-literature
merged_baseline: slice-003-quality-and-model-gate-complete
active_slice: slice-004-rights-ledger-foundation
next_slice: slice-004-rights-ledger-foundation
queued_slice: slice-005-wan-2.1-t2v-14b-benchmark
active_risks: ["production-model-not-accepted", "wan-14b-quality-gain-unproven", "wan-14b-resource-boundary-unmeasured", "human-publish-reviewer-unassigned"]
verification_reality: ["wan-1.3b-offline-baseline-retained", "wan-14b-selected-for-one-future-benchmark", "wan-14b-current-runtime-inventory-64.299-gib", "slice-003-downloaded-no-weights-and-ran-no-inference"]
authoritative_since: 2026-09-03
---

# Current State

## Merged Baseline
- Slices 001–003 are complete.
- The pinned 1.3B/Apple revisions remain `37ec512624d61f7aa208f7ea8140a131f93afc9a` / `796f5b53cab69a3d48a44233ce21aae889e94a08`.
- Slice 002 proved byte-identical online/offline 832×480 output: 2,222 seconds wall, 25.693 GB MLX peak, 56% minimum free memory, zero swap/warnings. Quality lacked historical specificity and strong sail motion.
- Slice 003 selected T2V 14B revision `a064a6c71f5be440641209c07bf2a5ce7a2ff5e4`, 8-bit DiT, for one future benchmark. Its ten-file inventory is 64.299 GiB; no weights or inference were used.

## Next Slice
- `slice-004-rights-ledger-foundation` is active next.
- `slice-005-wan-2.1-t2v-14b-benchmark` is queued but requires separate download/inference authority.

## Active Risks
- No production model is accepted.
- T2V 14B quality, runtime, MLX/process memory, swap, and thermals are unmeasured on BigBoy.
- Human editorial and legal publication review is not assigned.

## Verification Reality
- Slice 001 host checks and the Slice 002 verifier pass.
- Slice 003 verified current primary-source revisions, licenses, inventories, and pinned Apple support.
- All future 14B resource ranges are estimates. See the Slice 003 report and Slice 005 plan.
