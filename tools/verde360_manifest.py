#!/usr/bin/env python3
"""Write a non-sensitive build checkpoint; never infer device test results."""

import argparse
import hashlib
import json
import platform
import subprocess
from pathlib import Path

UPSTREAM = "87b176a078c316fde3adf67a217f0c44615b0e0d"


def command(args, cwd=None):
    try:
        result = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                                timeout=30, check=False)
        return result.stdout.strip() if result.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--artifacts", type=Path)
    parser.add_argument("--build-status", choices=["not_run", "passed", "failed"],
                        default="not_run")
    args = parser.parse_args()
    artifacts = []
    if args.artifacts and args.artifacts.exists():
        for path in sorted(args.artifacts.rglob("*.ipa")):
            artifacts.append({"path": path.relative_to(args.artifacts).as_posix(),
                              "size_bytes": path.stat().st_size,
                              "sha256": sha256(path),
                              "signing": "ad_hoc_requires_provisioned_resigning"})
    if args.build_status == "passed" and not artifacts:
        parser.error("a passed IPA build requires an existing IPA artifact")
    manifest = {
        "schema_version": 1,
        "upstream_commit": UPSTREAM,
        "source_commit": command(["git", "rev-parse", "HEAD"], args.source),
        "source_dirty": bool(command(["git", "status", "--porcelain",
                                      "--untracked-files=no"], args.source)),
        "toolchain": {
            "host_os": platform.system(), "python": platform.python_version(),
            "git": command(["git", "--version"]),
            "xcode": command(["xcodebuild", "-version"]),
            "iphoneos_sdk": command(["xcrun", "--sdk", "iphoneos",
                                      "--show-sdk-version"]),
            "cmake": command(["cmake", "--version"]),
            "ninja": command(["ninja", "--version"]),
        },
        "artifacts": artifacts,
        "tests": {"ios_build": args.build_status, "signing": "pending",
                  "installation": "pending", "jit_device": "pending",
                  "menus": "pending", "stock_fighter": "pending",
                  "created_fighter": "pending", "career_tutorial": "pending",
                  "sustained_match": "pending", "performance": "unmeasured"},
        "device_target": {"model": "iPhone 17 Pro Max", "ios": "26.0.1"},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
