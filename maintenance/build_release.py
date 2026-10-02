#!/usr/bin/env python3
"""Build and verify a deterministic source release from one explicit Git ref."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from check_release import PLUGIN_NAME, ReleaseError, check_release, included_path, safe_path


def git(repo: Path, *arguments: str) -> bytes:
    result = subprocess.run(["git", "-C", str(repo), *arguments], capture_output=True, check=False)
    if result.returncode:
        raise ReleaseError(f"git {arguments[0]} failed: {result.stderr.decode('utf-8', 'replace').strip()}")
    return result.stdout


def read_payload(repo: Path, ref: str) -> tuple[str, dict[str, tuple[bytes, int]]]:
    if not ref or ref.startswith("-"):
        raise ReleaseError("an explicit Git ref is required")
    commit = git(repo, "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}").decode("ascii").strip()
    payload = {}
    portable_names = set()
    for record in git(repo, "ls-tree", "-r", "-z", commit).split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        try:
            path = raw_path.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ReleaseError("Git tree contains a non-UTF-8 path") from error
        safe_path(path)
        mode, kind, oid = metadata.decode("ascii").split()
        if mode not in {"100644", "100755"} or kind != "blob":
            raise ReleaseError(f"only regular files are allowed; {path} has Git mode {mode} ({kind})")
        if included_path(path):
            if path.casefold() in portable_names:
                raise ReleaseError(f"case-colliding release path: {path}")
            portable_names.add(path.casefold())
            payload[path] = (git(repo, "cat-file", "blob", oid), int(mode, 8))
    return commit, payload


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_release(repo_root: Path, ref: str, output: Path, expected_version: str | None = None) -> dict:
    commit, payload = read_payload(repo_root.resolve(), ref)
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="release-", dir=output) as temporary:
        work = Path(temporary)
        source = work / "source"
        source.mkdir()
        for path, (data, mode) in sorted(payload.items()):
            destination = source / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            destination.chmod(mode & 0o777)
        checked = check_release(source, expected_version)
        version = checked["version"]
        prefix = f"{PLUGIN_NAME}-{version}"
        archive = work / f"{prefix}.zip"
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as zipped:
            for path, (data, mode) in sorted(payload.items()):
                entry = zipfile.ZipInfo(f"{prefix}/{path}", (1980, 1, 1, 0, 0, 0))
                entry.create_system = 3
                entry.external_attr = mode << 16
                entry.compress_type = zipfile.ZIP_STORED
                zipped.writestr(entry, data)
        extracted = work / "extracted"
        with zipfile.ZipFile(archive) as zipped:
            bad = zipped.testzip()
            if bad:
                raise ReleaseError(f"ZIP integrity check failed: {bad}")
            for entry in zipped.infolist():
                safe_path(entry.filename)
                if not entry.filename.startswith(prefix + "/"):
                    raise ReleaseError(f"unexpected archive path: {entry.filename}")
            zipped.extractall(extracted)
        check_release(extracted / prefix, version)
        archive_hash = sha256(archive)
        manifest = work / "release-manifest.json"
        manifest.write_text(json.dumps({
            "version": version,
            "sourceCommit": commit,
            "archive": archive.name,
            "archiveSha256": archive_hash,
            "files": [
                {"path": path, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}
                for path, (data, _mode) in sorted(payload.items())
            ],
        }, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        sums = work / "SHA256SUMS"
        sums.write_text(
            f"{archive_hash}  {archive.name}\n{sha256(manifest)}  {manifest.name}\n",
            encoding="ascii", newline="\n",
        )
        for path in (archive, manifest, sums):
            os.replace(path, output / path.name)
    return {
        "version": version, "sourceCommit": commit, "fileCount": len(payload),
        "archive": str(output / archive.name), "archiveSha256": archive_hash,
        "manifest": str(output / manifest.name), "checksums": str(output / sums.name),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--ref", required=True, help="Git commit, branch, or tag; the working tree is never packaged")
    parser.add_argument("--version", help="require this version; defaults to the plugin version at --ref")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(build_release(args.root, args.ref, args.output, args.version), ensure_ascii=False, sort_keys=True))
    except (ReleaseError, OSError, zipfile.BadZipFile) as error:
        print(f"release build failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
