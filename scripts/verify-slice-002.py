#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

EXPECTED_MODEL_REVISION = "37ec512624d61f7aa208f7ea8140a131f93afc9a"
EXPECTED_APPLE_REVISION = "796f5b53cab69a3d48a44233ce21aae889e94a08"
EXPECTED_REQUESTS = {
    "Wan2.1_VAE.pth",
    "diffusion_pytorch_model.safetensors",
    "google/umt5-xxl/tokenizer.json",
    "models_t5_umt5-xxl-enc-bf16.pth",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        key, separator, value = line.partition("=")
        if not separator:
            raise RuntimeError(f"Malformed summary line in {path}: {line}")
        values[key] = value
    return values


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    benchmark = json.loads(
        (repo_root / "benchmarks/slice-002-wan-1.3b.json").read_text(encoding="utf-8")
    )
    model_manifest = json.loads(
        (repo_root / "manifests/models/wan2.1-t2v-1.3b.json").read_text(
            encoding="utf-8"
        )
    )
    results_manifest = json.loads(
        (repo_root / "manifests/benchmarks/slice-002-wan-1.3b-results.json").read_text(
            encoding="utf-8"
        )
    )

    require(benchmark["model"]["revision"] == EXPECTED_MODEL_REVISION, "model revision drift")
    require(
        benchmark["model"]["apple_implementation_revision"] == EXPECTED_APPLE_REVISION,
        "Apple implementation revision drift",
    )
    require(model_manifest["model_revision"] == EXPECTED_MODEL_REVISION, "manifest revision drift")
    require(model_manifest["production_model_accepted"] is False, "candidate was marked accepted")
    require(results_manifest["model"]["production_model_accepted"] is False, "result accepted candidate")
    require(all(results_manifest["acceptance"].values()), "Slice 002 acceptance is incomplete")
    result_runs = {item["run_id"]: item for item in results_manifest["runs"]}

    runtime_entries = {
        item["path"]: item
        for item in model_manifest["files"]
        if item["path"] in EXPECTED_REQUESTS
    }
    require(set(runtime_entries) == EXPECTED_REQUESTS, "runtime file set drift")
    for relative_path, entry in runtime_entries.items():
        cached = repo_root / entry["cache_path"]
        require(cached.is_file(), f"missing cached model file: {relative_path}")
        require(cached.stat().st_size == entry["size_bytes"], f"size drift: {relative_path}")
        require(sha256(cached) == entry["sha256"], f"hash drift: {relative_path}")

    artifacts = repo_root / "benchmarks/artifacts/slice-002"
    outputs = repo_root / "outputs/slice-002"
    run_specs = {
        "online-pinned-baseline": {
            "mode": "online",
            "output": outputs / "wan-1.3b-online-seed-42.mp4",
            "preflight": "not-applicable",
            "wrapper_exit_code": "2",
            "wrapper_closeout": "recovered-after-live-runner-edit",
        },
        "offline-network-denied-repeat": {
            "mode": "offline",
            "output": outputs / "wan-1.3b-offline-seed-42.mp4",
            "preflight": "pass",
            "wrapper_exit_code": "0",
            "wrapper_closeout": "normal",
        },
    }

    for run_id, spec in run_specs.items():
        run_root = artifacts / run_id
        summary = load_env(run_root / "summary.env")
        require(summary["run_id"] == run_id, f"run id drift: {run_id}")
        require(summary["mode"] == spec["mode"], f"mode drift: {run_id}")
        require(summary["network_denial_preflight"] == spec["preflight"], f"preflight failed: {run_id}")
        require(summary["inference_exit_code"] == "0", f"inference failed: {run_id}")
        require(
            summary["wrapper_exit_code"] == spec["wrapper_exit_code"],
            f"wrapper result drift: {run_id}",
        )
        require(
            summary["wrapper_closeout"] == spec["wrapper_closeout"],
            f"wrapper closeout drift: {run_id}",
        )
        require(summary["safety_stop"] == "none", f"unsafe stop: {run_id}")

        result = result_runs[run_id]
        require(result["inference_exit_code"] == 0, f"result manifest inference failed: {run_id}")
        require(str(result["wrapper_exit_code"]) == summary["wrapper_exit_code"], f"result wrapper drift: {run_id}")

        sample_rows = (run_root / "system-samples.tsv").read_text(encoding="utf-8").splitlines()[1:]
        require(sample_rows, f"missing safety samples: {run_id}")
        columns = [row.split("\t") for row in sample_rows]
        minimum_free = min(int(float(row[1])) for row in columns)
        maximum_swap = max(float(row[2]) for row in columns)
        require(
            minimum_free == result["minimum_observed_memory_free_percent"],
            f"minimum memory sample drift: {run_id}",
        )
        require(maximum_swap == result["maximum_observed_swap_mb"], f"swap sample drift: {run_id}")
        require(
            all("No thermal warning" in row[5] and "No performance warning" in row[5] for row in columns),
            f"warning observed or evidence malformed: {run_id}",
        )

        output = spec["output"]
        require(output.is_file(), f"missing output: {output}")
        require(sha256(output) == summary["output_sha256"], f"output hash drift: {run_id}")
        require(sha256(output) == result["output_sha256"], f"result output hash drift: {run_id}")
        require(output.stat().st_size == int(summary["output_size_bytes"]), f"output size drift: {run_id}")
        require(output.stat().st_size == result["output_size_bytes"], f"result output size drift: {run_id}")

        probe = json.loads((run_root / "ffprobe.json").read_text(encoding="utf-8"))
        video = next(stream for stream in probe["streams"] if stream["codec_name"])
        require(video["width"] == 832 and video["height"] == 480, f"frame size drift: {run_id}")
        require(video["nb_frames"] == "81", f"frame count drift: {run_id}")
        require(video["r_frame_rate"] == "16/1", f"frame rate drift: {run_id}")

        log = (run_root / "run.log").read_text(encoding="utf-8")
        require(f"model_revision={EXPECTED_MODEL_REVISION}" in log, f"missing model pin: {run_id}")
        for filename in EXPECTED_REQUESTS:
            request = f"Wan-AI/Wan2.1-T2V-1.3B/{filename}@{EXPECTED_MODEL_REVISION}"
            require(log.count(request) == 1, f"unexpected request count for {filename}: {run_id}")
        require(f"offline={spec['mode'] == 'offline'}" in log, f"offline marker drift: {run_id}")

        subprocess.run(
            ["ffmpeg", "-v", "error", "-i", str(output), "-f", "null", "-"],
            check=True,
        )

    require(
        sha256(run_specs["online-pinned-baseline"]["output"])
        == sha256(run_specs["offline-network-denied-repeat"]["output"]),
        "online and offline outputs are not byte-identical",
    )

    print("slice-002-verification=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
