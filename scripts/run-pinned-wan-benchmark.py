#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import runpy
import sys
from pathlib import Path

MODEL_REPOSITORY = "Wan-AI/Wan2.1-T2V-1.3B"
MODEL_REVISION = "37ec512624d61f7aa208f7ea8140a131f93afc9a"
RUNTIME_FILES = {
    "Wan2.1_VAE.pth",
    "diffusion_pytorch_model.safetensors",
    "google/umt5-xxl/tokenizer.json",
    "models_t5_umt5-xxl-enc-bf16.pth",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the fixed Slice 002 Wan benchmark with exact model revision pinning."
    )
    parser.add_argument("--network-mode", choices=("online", "offline"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    wan_root = repo_root / "third_party/mlx-examples/video/wan2.1"
    benchmark_path = repo_root / "benchmarks/slice-002-wan-1.3b.json"
    benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
    parameters = benchmark["parameters"]

    cache_root = repo_root / ".cache/huggingface"
    os.environ["HF_HOME"] = str(cache_root)
    os.environ["HF_HUB_CACHE"] = str(cache_root / "hub")
    offline = args.network_mode == "offline"
    if offline:
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
        os.environ["DIFFUSERS_OFFLINE"] = "1"
    else:
        os.environ.pop("HF_HUB_OFFLINE", None)
        os.environ.pop("TRANSFORMERS_OFFLINE", None)
        os.environ.pop("DIFFUSERS_OFFLINE", None)

    sys.path.insert(0, str(wan_root))
    import wan.utils as wan_utils
    from huggingface_hub import hf_hub_download

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
            cache_dir=cache_root / "hub",
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
        "--output",
        str(args.output),
        "--verbose",
    ]
    print(
        f"Starting fixed benchmark: network_mode={args.network_mode} model_revision={MODEL_REVISION}",
        flush=True,
    )
    runpy.run_path(str(wan_root / "txt2video.py"), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
