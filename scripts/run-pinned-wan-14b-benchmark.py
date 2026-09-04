#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import runpy
import subprocess
import sys
from pathlib import Path

MODEL_REPOSITORY = "Wan-AI/Wan2.1-T2V-14B"
MODEL_REVISION = "a064a6c71f5be440641209c07bf2a5ce7a2ff5e4"
APPLE_REVISION = "796f5b53cab69a3d48a44233ce21aae889e94a08"
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the fixed Slice 005 Wan 14B benchmark with exact revision pinning."
    )
    parser.add_argument("--network-mode", choices=("online", "offline"), required=True)
    parser.add_argument("--output", type=Path, required=True)
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


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    wan_root = repo_root / "third_party/mlx-examples/video/wan2.1"
    benchmark_path = repo_root / "benchmarks/slice-005-wan-2.1-t2v-14b.json"
    benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
    parameters = benchmark["parameters"]

    if benchmark["model"]["revision"] != MODEL_REVISION:
        raise RuntimeError("Benchmark model revision drift")
    if benchmark["model"]["apple_implementation_revision"] != APPLE_REVISION:
        raise RuntimeError("Benchmark Apple implementation revision drift")
    actual_apple_revision = subprocess.run(
        ["git", "-C", str(repo_root / "third_party/mlx-examples"), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if actual_apple_revision != APPLE_REVISION:
        raise RuntimeError(
            f"Apple implementation drift: expected {APPLE_REVISION}, found {actual_apple_revision}"
        )
    if os.environ.get("WAN_T2V_14B"):
        raise RuntimeError("WAN_T2V_14B override is forbidden for the fixed benchmark")

    model_store = args.model_store.expanduser().resolve()
    os.environ["HF_HOME"] = str(model_store.parent)
    os.environ["HF_HUB_CACHE"] = str(model_store)
    offline = args.network_mode == "offline"
    if offline:
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
        os.environ["DIFFUSERS_OFFLINE"] = "1"
    else:
        os.environ.pop("HF_HUB_OFFLINE", None)
        os.environ.pop("TRANSFORMERS_OFFLINE", None)
        os.environ.pop("DIFFUSERS_OFFLINE", None)

    from huggingface_hub import hf_hub_download

    for filename in sorted(RUNTIME_FILES):
        resolved = hf_hub_download(
            repo_id=MODEL_REPOSITORY,
            filename=filename,
            revision=MODEL_REVISION,
            cache_dir=model_store,
            local_files_only=offline,
        )
        print(
            f"Preflight model file: {MODEL_REPOSITORY}/{filename}@{MODEL_REVISION} "
            f"offline={offline} path={Path(resolved).relative_to(model_store)}",
            flush=True,
        )

    sys.path.insert(0, str(wan_root))
    import wan.utils as wan_utils

    def pinned_download(repo_id: str, filename: str) -> str:
        if repo_id != MODEL_REPOSITORY:
            raise RuntimeError(f"Unexpected model repository request: {repo_id}")
        if filename not in RUNTIME_FILES:
            raise RuntimeError(f"Unexpected model file request: {filename}")
        print(
            f"Pinned model request: {repo_id}/{filename}@{MODEL_REVISION} offline={offline}",
            flush=True,
        )
        return hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            revision=MODEL_REVISION,
            cache_dir=model_store,
            local_files_only=offline,
        )

    wan_utils._hf_download = pinned_download
    args.output.parent.mkdir(parents=True, exist_ok=True)

    size = f"{parameters['width']}x{parameters['height']}"
    sys.argv = [
        str(wan_root / "txt2video.py"),
        benchmark["prompt"],
        "--model",
        parameters["model"],
        "--size",
        size,
        "--frames",
        str(parameters["frames"]),
        "--steps",
        str(parameters["steps"]),
        "--guidance",
        str(parameters["guidance"]),
        "--shift",
        str(parameters["shift"]),
        "--seed",
        str(parameters["seed"]),
        "--sampler",
        parameters["sampler"],
        "--quantize",
        str(parameters["quantization_bits"]),
        "--teacache",
        str(parameters["teacache"]),
        "--n-prompt",
        benchmark["negative_prompt"],
        "--no-cache",
        "--output",
        str(args.output),
        "--verbose",
    ]
    print(
        f"Starting fixed Slice 005 benchmark: network_mode={args.network_mode} "
        f"model_revision={MODEL_REVISION} apple_revision={APPLE_REVISION}",
        flush=True,
    )
    runpy.run_path(str(wan_root / "txt2video.py"), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
