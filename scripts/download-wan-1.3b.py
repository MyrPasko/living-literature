#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from huggingface_hub import hf_hub_download

MODEL_REPOSITORY = "Wan-AI/Wan2.1-T2V-1.3B"
MODEL_REVISION = "37ec512624d61f7aa208f7ea8140a131f93afc9a"
LICENSE_NAME = "LICENSE.txt"

FILES = {
    "LICENSE.txt": {"size": 11_357, "sha256": None, "purpose": "license evidence"},
    "README.md": {"size": 16_913, "sha256": None, "purpose": "model card evidence"},
    "Wan2.1_VAE.pth": {
        "size": 507_609_880,
        "sha256": "38071ab59bd94681c686fa51d75a1968f64e470262043be31f7a094e442fd981",
        "purpose": "video autoencoder weights",
    },
    "diffusion_pytorch_model.safetensors": {
        "size": 5_676_070_424,
        "sha256": "96b6b242ca1c2f24e9d02cd6596066fab6d310e2d7538f33ae267cb18d957e8f",
        "purpose": "1.3B diffusion transformer weights",
    },
    "google/umt5-xxl/tokenizer.json": {
        "size": 16_837_417,
        "sha256": "6e197b4d3dbd71da14b4eb255f4fa91c9c1f2068b20a2de2472967ca3d22602b",
        "purpose": "text tokenizer",
    },
    "models_t5_umt5-xxl-enc-bf16.pth": {
        "size": 11_361_920_418,
        "sha256": "7cace0da2b446bbbbc57d031ab6cf163a3d59b366da94e5afe36745b746fd81d",
        "purpose": "local UMT5 text encoder weights",
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Download and verify only the pinned Wan2.1 1.3B files required by Slice 002."
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=repo_root / ".cache/huggingface/hub",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=repo_root / "manifests/models/wan2.1-t2v-1.3b.json",
    )
    parser.add_argument(
        "--license-copy",
        type=Path,
        default=repo_root / "docs/licenses/wan2.1-t2v-1.3b-apache-2.0.txt",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    args.cache_dir.mkdir(parents=True, exist_ok=True)

    downloaded = []
    resolved_paths: dict[str, Path] = {}
    for filename, expected in FILES.items():
        print(f"Resolving {filename} at {MODEL_REVISION}", flush=True)
        resolved = Path(
            hf_hub_download(
                repo_id=MODEL_REPOSITORY,
                filename=filename,
                revision=MODEL_REVISION,
                cache_dir=args.cache_dir,
            )
        )
        actual_size = resolved.stat().st_size
        actual_hash = sha256(resolved)
        if actual_size != expected["size"]:
            raise RuntimeError(
                f"Size mismatch for {filename}: expected {expected['size']}, found {actual_size}"
            )
        if expected["sha256"] and actual_hash != expected["sha256"]:
            raise RuntimeError(
                f"SHA-256 mismatch for {filename}: expected {expected['sha256']}, found {actual_hash}"
            )
        resolved_paths[filename] = resolved
        downloaded.append(
            {
                "path": filename,
                "purpose": expected["purpose"],
                "size_bytes": actual_size,
                "sha256": actual_hash,
                "cache_path": str(resolved.relative_to(repo_root)),
            }
        )
        print(f"Verified {filename}: {actual_size} bytes, sha256={actual_hash}", flush=True)

    args.license_copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(resolved_paths[LICENSE_NAME], args.license_copy)
    license_hash = sha256(args.license_copy)

    manifest = {
        "model_repository": MODEL_REPOSITORY,
        "model_revision": MODEL_REVISION,
        "license": "Apache-2.0",
        "license_source": f"https://huggingface.co/{MODEL_REPOSITORY}/blob/{MODEL_REVISION}/{LICENSE_NAME}",
        "license_copy": str(args.license_copy.relative_to(repo_root)),
        "license_sha256": license_hash,
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "cache_root": str(args.cache_dir.relative_to(repo_root)),
        "files": downloaded,
        "total_size_bytes": sum(item["size_bytes"] for item in downloaded),
        "production_model_accepted": False,
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.manifest}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
