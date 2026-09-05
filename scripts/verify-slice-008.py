#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import os
import struct
import subprocess
from pathlib import Path


BENCHMARK_ID = "slice-008-corrected-first-last-motion-scout"
MODEL_REVISION = "ef2a0bfe5b4ca7edb84c93f1675edb1a8bfe7d60"
RUNTIME_VERSION = "0.33.1"
RUNTIME_COMMIT = "23cee803f10aacdf943a9565f7cd67c25c825080"
RUNTIME_WHEEL_SHA256 = "1a19e6510a166cbe0fe4975146813fb61adf98f0e073abb4e63f27f012882d0a"
FIRST_SHA256 = "9441f1a783f42ef1e7b605f0c4c6981462e071c46f49c7607a4ba6ab9533ffde"
LAST_SHA256 = "6c0f3d2ee62e4ff563a1fc02d6e42a3f255bc75d3bed8fa6210904f862ef85ce"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as source:
        header = source.read(24)
    require(header[:8] == b"\x89PNG\r\n\x1a\n", f"not a PNG: {path}")
    require(header[12:16] == b"IHDR", f"missing PNG IHDR: {path}")
    return struct.unpack(">II", header[16:24])


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    benchmark_path = repo_root / "benchmarks/slice-008-corrected-first-last-motion-scout.json"
    benchmark = load_json(benchmark_path)
    require(benchmark["benchmark_id"] == BENCHMARK_ID, "benchmark id drift")
    require(benchmark["status"] == "anchors-and-prompts-approved", "preparation status drift")
    require(benchmark["model"]["revision"] == MODEL_REVISION, "model revision drift")
    require(benchmark["model"]["download_authorized"] is False, "model download was authorized")
    runtime = benchmark["runtime"]
    require(runtime["version"] == RUNTIME_VERSION, "runtime version drift")
    require(runtime["source_commit"] == RUNTIME_COMMIT, "runtime commit drift")
    require(runtime["wheel_sha256"] == RUNTIME_WHEEL_SHA256, "runtime wheel drift")
    require(runtime["executable"] == "mlxgen-generate-wan", "wrong runtime executable")
    require(runtime["endpoint_option"] == "--last-image", "endpoint option drift")
    require(runtime["generic_wrapper_exposes_endpoint_option"] is False, "generic wrapper claim drift")

    anchors = benchmark["anchors"]
    for name, expected_hash in (("first", FIRST_SHA256), ("last", LAST_SHA256)):
        record = anchors[name]
        path = repo_root / record["path"]
        require(path.is_file(), f"missing {name} anchor")
        require(sha256(path) == record["sha256"] == expected_hash, f"{name} anchor hash drift")
        require(png_dimensions(path) == (record["width"], record["height"]) == (1672, 940), f"{name} anchor dimensions drift")
        ignored = subprocess.run(
            ["git", "-C", str(repo_root), "check-ignore", "-q", str(path)], check=False
        ).returncode == 0
        require(ignored and record["git_ignored"] is True, f"{name} anchor is not Git-ignored")

    first_provenance = load_json(
        repo_root / "outputs/next-slice-reference-candidates/right-facing-aegean-galley-start-frame-candidate-v2.provenance.json"
    )
    last_provenance = load_json(
        repo_root / "outputs/next-slice-reference-candidates/right-facing-aegean-galley-approved-end-frame-v1.provenance.json"
    )
    require(first_provenance["sha256"] == FIRST_SHA256, "first-anchor provenance drift")
    require(last_provenance["sha256"] == LAST_SHA256, "last-anchor provenance drift")
    require(anchors["rights_status"] == "internal-evaluation-only-unresolved-user-reference-lineage", "rights boundary drift")

    parameters = benchmark["parameters"]
    require((parameters["requested_width"], parameters["requested_height"]) == (448, 256), "canvas drift")
    require((parameters["frames"], parameters["fps"], parameters["steps"]) == (41, 8, 15), "frame/fps/step drift")
    require(parameters["seed"] == 42, "seed drift")
    require((parameters["guidance"], parameters["guidance_2"], parameters["flow_shift"]) == (4.0, 3.0, 3.0), "guidance drift")
    require(parameters["solver"] == "unipc", "solver drift")
    require(parameters["low_ram"] and parameters["metadata"], "low-RAM or metadata missing")
    require(parameters["prompt_cache"] is False and parameters["parallel_process"] is False, "forbidden runtime setting enabled")
    require(len(benchmark["hard_gates"]) == 12, "hard-gate count drift")
    require(all(value is False for key, value in benchmark["slice_restrictions"].items() if key != "slice_004_remains_postponed"), "pre-approval authority enabled")
    require(benchmark["slice_restrictions"]["slice_004_remains_postponed"] is True, "Slice 004 disposition drift")
    approval = benchmark["approval_gate"]
    require(approval["approved_at_date"] == "2026-09-05", "approval date drift")
    require(approval["first_anchor_approved"] is True, "first anchor is not approved")
    require(approval["last_anchor_approved_for_slice_008"] is True, "last anchor is not approved")
    require(approval["prompt_approved"] is True, "prompt is not approved")
    require(approval["inference_authorized_in_current_session"] is False, "current-session inference was authorized")
    require(approval["next_session_prompt_authorizes_one_inference_when_pasted"] is True, "next-session authorization boundary drift")

    runtime_root = Path(
        os.environ.get(
            "LIVING_LITERATURE_RUNTIME_ROOT",
            "~/models/living-literature/runtimes/mlx-gen-0.33.1",
        )
    ).expanduser()
    wan_cli = runtime_root / ".venv/bin/mlxgen-generate-wan"
    generic_cli = runtime_root / ".venv/bin/mlxgen"
    require(wan_cli.is_file() and os.access(wan_cli, os.X_OK), "direct Wan CLI missing")
    require(generic_cli.is_file() and os.access(generic_cli, os.X_OK), "generic MLX-Gen CLI missing")
    wan_help = subprocess.run([str(wan_cli), "--help"], check=True, capture_output=True, text=True).stdout
    generic_help = subprocess.run([str(generic_cli), "generate", "--help"], check=True, capture_output=True, text=True).stdout
    require("--last-image" in wan_help, "direct Wan CLI lacks endpoint conditioning")
    require("--last-image" not in generic_help, "generic wrapper endpoint claim is stale")

    print("slice-008-verification=pass state=anchors-and-prompts-approved inference=current-session-not-authorized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
