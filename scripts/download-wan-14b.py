#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

from huggingface_hub import HfApi, hf_hub_download

MODEL_REPOSITORY = "Wan-AI/Wan2.1-T2V-14B"
MODEL_REVISION = "a064a6c71f5be440641209c07bf2a5ce7a2ff5e4"
LICENSE_NAME = "LICENSE.txt"
MINIMUM_DISK_GIB = 165
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
FILES = {
    "LICENSE.txt": {
        "size": 11_357,
        "sha256": "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4",
        "purpose": "license evidence",
    },
    "README.md": {
        "size": 16_981,
        "sha256": None,
        "purpose": "model card evidence",
    },
    "diffusion_pytorch_model.safetensors.index.json": {
        "size": 96_805,
        "sha256": None,
        "purpose": "14B diffusion transformer shard index",
    },
    "diffusion_pytorch_model-00001-of-00006.safetensors": {
        "size": 9_887_603_256,
        "sha256": "569d54a07279b89f8281421fccf27ee2459ea853ce6845d3536b8664b0070078",
        "purpose": "14B diffusion transformer shard 1 of 6",
    },
    "diffusion_pytorch_model-00002-of-00006.safetensors": {
        "size": 9_839_059_648,
        "sha256": "b17ff172f262b4da91c31e8c46d3b7707f62cecfff6e18dd0072ab29eb350e46",
        "purpose": "14B diffusion transformer shard 2 of 6",
    },
    "diffusion_pytorch_model-00003-of-00006.safetensors": {
        "size": 9_839_059_744,
        "sha256": "741fd1508cd0288f0bb0f4fb3df6734da521d5ff23746170c848564a367e2cea",
        "purpose": "14B diffusion transformer shard 3 of 6",
    },
    "diffusion_pytorch_model-00004-of-00006.safetensors": {
        "size": 9_839_059_744,
        "sha256": "47b08ba289b127fc64979bc877ee07e1c87aeb8eb8cd47bcfd112682847981ba",
        "purpose": "14B diffusion transformer shard 4 of 6",
    },
    "diffusion_pytorch_model-00005-of-00006.safetensors": {
        "size": 9_839_059_744,
        "sha256": "29e35f4cf0e3a61f4726c960f1babf71d65677a8c99fe704257d665c9498ee88",
        "purpose": "14B diffusion transformer shard 5 of 6",
    },
    "diffusion_pytorch_model-00006-of-00006.safetensors": {
        "size": 7_910_235_256,
        "sha256": "91ac087a40b814331e87f5f015af11ba999275d48d2af49591b6bf7727d3c146",
        "purpose": "14B diffusion transformer shard 6 of 6",
    },
    "Wan2.1_VAE.pth": {
        "size": 507_609_880,
        "sha256": "38071ab59bd94681c686fa51d75a1968f64e470262043be31f7a094e442fd981",
        "purpose": "video autoencoder weights",
    },
    "models_t5_umt5-xxl-enc-bf16.pth": {
        "size": 11_361_920_418,
        "sha256": "7cace0da2b446bbbbc57d031ab6cf163a3d59b366da94e5afe36745b746fd81d",
        "purpose": "local UMT5 text encoder weights",
    },
    "google/umt5-xxl/tokenizer.json": {
        "size": 16_837_417,
        "sha256": "6e197b4d3dbd71da14b4eb255f4fa91c9c1f2068b20a2de2472967ca3d22602b",
        "purpose": "text tokenizer",
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def portable_path(path: Path) -> str:
    home = Path.home().resolve()
    resolved = path.resolve()
    try:
        return f"~/{resolved.relative_to(home)}"
    except ValueError:
        return str(resolved)


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parent.parent
    default_store = Path(
        os.environ.get(
            "LIVING_LITERATURE_MODEL_STORE",
            Path.home() / "models/huggingface/hub",
        )
    )
    parser = argparse.ArgumentParser(
        description="Download and verify only the pinned Wan2.1 T2V 14B files required by Slice 005."
    )
    parser.add_argument("--model-store", type=Path, default=default_store)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=repo_root / "manifests/models/wan2.1-t2v-14b.json",
    )
    parser.add_argument(
        "--license-copy",
        type=Path,
        default=repo_root / "docs/licenses/wan2.1-t2v-14b-apache-2.0.txt",
    )
    return parser.parse_args()


def verify_remote_metadata() -> None:
    info = HfApi().model_info(MODEL_REPOSITORY, files_metadata=True)
    if info.sha != MODEL_REVISION:
        raise RuntimeError(
            f"Model revision drift: expected {MODEL_REVISION}, found {info.sha}"
        )
    siblings = {item.rfilename: item for item in info.siblings}
    if not set(FILES).issubset(siblings):
        missing = sorted(set(FILES) - set(siblings))
        raise RuntimeError(f"Remote file inventory is missing: {missing}")
    for filename, expected in FILES.items():
        actual_size = siblings[filename].size
        if actual_size != expected["size"]:
            raise RuntimeError(
                f"Remote size drift for {filename}: expected {expected['size']}, found {actual_size}"
            )
        remote_lfs = siblings[filename].lfs
        expected_hash = expected["sha256"]
        if remote_lfs and expected_hash and remote_lfs.sha256 != expected_hash:
            raise RuntimeError(f"Remote LFS hash drift for {filename}")


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    model_store = args.model_store.expanduser().resolve()
    model_store.mkdir(parents=True, exist_ok=True)

    disk_free = shutil.disk_usage(model_store).free
    minimum_disk = MINIMUM_DISK_GIB * 1024**3
    if disk_free < minimum_disk:
        raise RuntimeError(
            f"Refusing download: {disk_free / 1024**3:.1f} GiB free; {MINIMUM_DISK_GIB} GiB required"
        )

    verify_remote_metadata()
    print(
        f"Remote revision and {len(FILES)}-file inventory verified at {MODEL_REVISION}",
        flush=True,
    )

    downloaded = []
    resolved_paths: dict[str, Path] = {}
    for filename, expected in FILES.items():
        print(f"Resolving {filename} at {MODEL_REVISION}", flush=True)
        resolved = Path(
            hf_hub_download(
                repo_id=MODEL_REPOSITORY,
                filename=filename,
                revision=MODEL_REVISION,
                cache_dir=model_store,
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
                "runtime_required": filename in RUNTIME_FILES,
                "size_bytes": actual_size,
                "sha256": actual_hash,
                "cache_path": str(resolved.relative_to(model_store)),
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
        "cache_root": portable_path(model_store),
        "cache_policy": "external-user-model-store",
        "files": downloaded,
        "runtime_file_count": len(RUNTIME_FILES),
        "runtime_size_bytes": sum(
            item["size_bytes"] for item in downloaded if item["runtime_required"]
        ),
        "total_size_bytes": sum(item["size_bytes"] for item in downloaded),
        "production_model_accepted": False,
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.manifest}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
