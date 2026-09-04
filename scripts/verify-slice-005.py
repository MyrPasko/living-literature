#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

MODEL_REPOSITORY = "Wan-AI/Wan2.1-T2V-14B"
MODEL_REVISION = "a064a6c71f5be440641209c07bf2a5ce7a2ff5e4"
APPLE_REVISION = "796f5b53cab69a3d48a44233ce21aae889e94a08"
LICENSE_SHA256 = "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4"
RUNTIME_FILES = {
    "diffusion_pytorch_model.safetensors.index.json",
    "diffusion_pytorch_model-00001-of-00006.safetensors",
    "diffusion_pytorch_model-00002-of-00006.safetensors",
    "diffusion_pytorch_model-00003-of-00006.safetensors",
    "diffusion_pytorch_model-00004-of-00006.safetensors",
    "diffusion_pytorch_model-00005-of-00006.safetensors",
    "diffusion_pytorch_model-00006-of-00006.safetensors",
    "Wan2.1_VAE.pth",
    "models_t5_umt5-xxl-enc-bf16.pth",
    "google/umt5-xxl/tokenizer.json",
}
RUNTIME_REQUESTS = {
    "diffusion_pytorch_model.safetensors.index.json",
    "Wan2.1_VAE.pth",
    "models_t5_umt5-xxl-enc-bf16.pth",
    "google/umt5-xxl/tokenizer.json",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify Slice 005 model and benchmark evidence.")
    parser.add_argument("--model-only", action="store_true")
    parser.add_argument(
        "--model-store",
        type=Path,
        default=Path(
            os.environ.get(
                "LIVING_LITERATURE_MODEL_STORE",
                Path.home() / "models/huggingface/hub",
            )
        ),
    )
    return parser.parse_args()


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


def parse_time_metric(log: str, label: str) -> int:
    match = re.search(rf"^\s*(\d+)\s+{re.escape(label)}$", log, re.MULTILINE)
    if not match:
        raise RuntimeError(f"Missing time metric: {label}")
    return int(match.group(1))


def verify_model(repo_root: Path, model_store: Path) -> dict:
    benchmark = json.loads(
        (repo_root / "benchmarks/slice-005-wan-2.1-t2v-14b.json").read_text(
            encoding="utf-8"
        )
    )
    manifest = json.loads(
        (repo_root / "manifests/models/wan2.1-t2v-14b.json").read_text(
            encoding="utf-8"
        )
    )
    require(benchmark["model"]["repository"] == MODEL_REPOSITORY, "benchmark repository drift")
    require(benchmark["model"]["revision"] == MODEL_REVISION, "benchmark revision drift")
    require(
        benchmark["model"]["apple_implementation_revision"] == APPLE_REVISION,
        "benchmark Apple revision drift",
    )
    parameters = benchmark["parameters"]
    require(parameters["model"] == "t2v-14B", "model selector drift")
    require(parameters["width"] == 832 and parameters["height"] == 480, "size drift")
    require(parameters["frames"] == 81 and parameters["steps"] == 50, "frame/step drift")
    require(parameters["seed"] == 42, "seed drift")
    require(parameters["guidance"] == 5.0 and parameters["shift"] == 5.0, "guidance/shift drift")
    require(parameters["sampler"] == "unipc", "sampler drift")
    require(parameters["quantization_bits"] == 8, "quantization drift")
    require(parameters["teacache"] == 0.0, "TeaCache drift")
    require(parameters["metal_cache_enabled"] is False, "Metal cache drift")
    require(parameters["offloading"] == "none", "offloading drift")

    require(manifest["model_repository"] == MODEL_REPOSITORY, "manifest repository drift")
    require(manifest["model_revision"] == MODEL_REVISION, "manifest revision drift")
    require(manifest["license_sha256"] == LICENSE_SHA256, "license hash drift")
    require(manifest["production_model_accepted"] is False, "model prematurely accepted")
    require(manifest["cache_policy"] == "external-user-model-store", "cache policy drift")
    require(manifest["cache_root"] == "~/models/huggingface/hub", "cache root drift")
    require(manifest["runtime_file_count"] == 10, "runtime file count drift")
    require(manifest["runtime_size_bytes"] == 69_040_541_912, "runtime size drift")
    require(manifest["total_size_bytes"] == 69_040_570_250, "total file size drift")
    require(model_store.resolve().is_relative_to(Path.home() / "models"), "model store is outside ~/models")

    entries = {item["path"]: item for item in manifest["files"]}
    runtime_entries = {
        name: entry for name, entry in entries.items() if entry["runtime_required"]
    }
    require(set(runtime_entries) == RUNTIME_FILES, "runtime file set drift")
    for relative_path, entry in entries.items():
        cached = model_store / entry["cache_path"]
        require(cached.is_file(), f"missing cached model file: {relative_path}")
        require(cached.stat().st_size == entry["size_bytes"], f"size drift: {relative_path}")
        require(sha256(cached) == entry["sha256"], f"hash drift: {relative_path}")

    index_entry = entries["diffusion_pytorch_model.safetensors.index.json"]
    shard_index = json.loads(
        (model_store / index_entry["cache_path"]).read_text(encoding="utf-8")
    )
    indexed_shards = set(shard_index["weight_map"].values())
    expected_shards = {
        name for name in RUNTIME_FILES if name.startswith("diffusion_pytorch_model-")
    }
    require(indexed_shards == expected_shards, "DiT shard index drift")

    license_copy = repo_root / manifest["license_copy"]
    require(license_copy.is_file(), "missing tracked license copy")
    require(sha256(license_copy) == LICENSE_SHA256, "tracked license copy drift")
    actual_apple_revision = subprocess.run(
        ["git", "-C", str(repo_root / "third_party/mlx-examples"), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    require(actual_apple_revision == APPLE_REVISION, "Apple implementation drift")
    return benchmark


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    model_store = args.model_store.expanduser().resolve()
    benchmark = verify_model(repo_root, model_store)
    if args.model_only:
        print("slice-005-model-verification=pass")
        return 0

    results_path = repo_root / "manifests/benchmarks/slice-005-wan-14b-results.json"
    results = json.loads(results_path.read_text(encoding="utf-8"))
    require(results["benchmark_id"] == benchmark["benchmark_id"], "results benchmark drift")
    require(results["model"]["revision"] == MODEL_REVISION, "results revision drift")
    require(results["model"]["production_model_accepted"] is False, "production model accepted")
    result_runs = {item["run_id"]: item for item in results["runs"]}

    artifacts = repo_root / "benchmarks/artifacts/slice-005"
    run_specs = {
        "online-pinned-14b": {
            "mode": "online",
            "output": repo_root / "outputs/slice-005/wan-14b-online-seed-42.mp4",
            "preflight": "not-applicable",
        },
        "offline-network-denied-14b": {
            "mode": "offline",
            "output": repo_root / "outputs/slice-005/wan-14b-offline-seed-42.mp4",
            "preflight": "pass",
        },
    }

    output_hashes = []
    for run_id, spec in run_specs.items():
        run_root = artifacts / run_id
        summary = load_env(run_root / "summary.env")
        require(summary["run_id"] == run_id, f"run id drift: {run_id}")
        require(summary["mode"] == spec["mode"], f"mode drift: {run_id}")
        require(summary["network_denial_preflight"] == spec["preflight"], f"network preflight failed: {run_id}")
        require(summary["inference_exit_code"] == "0", f"inference failed: {run_id}")
        require(summary["wrapper_exit_code"] == "0", f"wrapper failed: {run_id}")
        require(summary["wrapper_closeout"] == "normal", f"wrapper closeout drift: {run_id}")
        require(summary["safety_stop"] == "none", f"unsafe stop: {run_id}")
        require(summary["full_decode"] == "pass", f"decode failed: {run_id}")
        require(int(summary["duration_seconds"]) <= 14_400, f"run exceeded four hours: {run_id}")

        sample_rows = (run_root / "system-samples.tsv").read_text(encoding="utf-8").splitlines()[1:]
        require(sample_rows, f"missing safety samples: {run_id}")
        columns = [row.split("\t") for row in sample_rows]
        minimum_free = min(int(float(row[1])) for row in columns)
        maximum_swap = max(float(row[2]) for row in columns)
        maximum_tree_rss_kb = max(int(row[5]) for row in columns)
        require(minimum_free > 10, f"memory safety boundary reached: {run_id}")
        require(maximum_swap <= 8192, f"swap safety boundary exceeded: {run_id}")
        require(all("No thermal warning" in row[6] and "No performance warning" in row[6] for row in columns), f"warning observed: {run_id}")

        output = spec["output"]
        require(output.is_file(), f"missing output: {run_id}")
        output_hash = sha256(output)
        output_hashes.append(output_hash)
        require(output_hash == summary["output_sha256"], f"output hash drift: {run_id}")
        require(output.stat().st_size == int(summary["output_size_bytes"]), f"output size drift: {run_id}")

        probe = json.loads((run_root / "ffprobe.json").read_text(encoding="utf-8"))
        video = next(stream for stream in probe["streams"] if stream["codec_name"])
        require(video["codec_name"] == "h264", f"codec drift: {run_id}")
        require(video["width"] == 832 and video["height"] == 480, f"frame size drift: {run_id}")
        require(video["nb_frames"] == "81", f"frame count drift: {run_id}")
        require(video["r_frame_rate"] == "16/1", f"frame rate drift: {run_id}")

        log = (run_root / "run.log").read_text(encoding="utf-8", errors="replace")
        require(f"model_revision={MODEL_REVISION}" in log, f"missing model pin: {run_id}")
        require(f"apple_revision={APPLE_REVISION}" in log, f"missing Apple pin: {run_id}")
        require("Quantized DiT to 8-bit" in log, f"quantization not observed: {run_id}")
        require("Peak memory overall:" in log, f"MLX peak missing: {run_id}")
        for filename in RUNTIME_FILES:
            marker = f"Preflight model file: {MODEL_REPOSITORY}/{filename}@{MODEL_REVISION}"
            require(log.count(marker) == 1, f"unexpected preflight count for {filename}: {run_id}")
        for filename in RUNTIME_REQUESTS:
            marker = f"Pinned model request: {MODEL_REPOSITORY}/{filename}@{MODEL_REVISION}"
            require(log.count(marker) == 1, f"unexpected request count for {filename}: {run_id}")
        require(f"offline={spec['mode'] == 'offline'}" in log, f"offline marker drift: {run_id}")

        result = result_runs[run_id]
        require(result["output_sha256"] == output_hash, f"results output hash drift: {run_id}")
        require(result["minimum_observed_memory_free_percent"] == minimum_free, f"results memory drift: {run_id}")
        require(result["maximum_observed_swap_mb"] == maximum_swap, f"results swap drift: {run_id}")
        require(result["maximum_sampled_process_tree_rss_kb"] == maximum_tree_rss_kb, f"results RSS drift: {run_id}")
        require(result["maximum_resident_set_bytes"] == parse_time_metric(log, "maximum resident set size"), f"results max RSS drift: {run_id}")
        require(result["peak_process_footprint_bytes"] == parse_time_metric(log, "peak memory footprint"), f"results footprint drift: {run_id}")

        subprocess.run(
            ["ffmpeg", "-v", "error", "-i", str(output), "-f", "null", "-"],
            check=True,
        )

    require(output_hashes[0] == output_hashes[1], "online and offline outputs differ")
    require(results["media"]["online_offline_outputs_byte_identical"] is True, "results identity failed")
    print("slice-005-verification=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
