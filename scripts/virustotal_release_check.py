#!/usr/bin/env python3
"""Look up or optionally submit release artifacts to VirusTotal."""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path


API_BASE = "https://www.virustotal.com/api/v3"


def read_hashes(checksums: Path) -> list[str]:
    if not checksums.exists():
        return []

    hashes: list[str] = []
    for line in checksums.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if parts and len(parts[0]) == 64:
            hashes.append(parts[0])
    return hashes


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def request_json(method: str, url: str, api_key: str, body: bytes | None = None, content_type: str | None = None) -> tuple[int, dict]:
    headers = {"x-apikey": api_key}
    if content_type:
        headers["content-type"] = content_type

    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        text = error.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = {"error": {"message": text}}
        return error.code, payload


def lookup_hash(api_key: str, digest: str) -> str:
    status, payload = request_json("GET", f"{API_BASE}/files/{digest}", api_key)
    gui_url = f"https://www.virustotal.com/gui/file/{digest}"

    if status == 404:
        return f"- `{digest}`: not found in VirusTotal ({gui_url})"
    if status >= 400:
        message = payload.get("error", {}).get("message", "request failed")
        return f"- `{digest}`: lookup failed with HTTP {status}: {message}"

    stats = payload.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
    malicious = stats.get("malicious", 0)
    suspicious = stats.get("suspicious", 0)
    harmless = stats.get("harmless", 0)
    undetected = stats.get("undetected", 0)
    return (
        f"- `{digest}`: malicious={malicious}, suspicious={suspicious}, "
        f"harmless={harmless}, undetected={undetected} ({gui_url})"
    )


def multipart_file_body(path: Path) -> tuple[bytes, str]:
    boundary = f"----pybusy-{uuid.uuid4().hex}"
    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    header = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{path.name}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode("utf-8")
    footer = f"\r\n--{boundary}--\r\n".encode("utf-8")
    return header + path.read_bytes() + footer, f"multipart/form-data; boundary={boundary}"


def submit_file(api_key: str, path: Path) -> str:
    body, content_type = multipart_file_body(path)
    status, payload = request_json("POST", f"{API_BASE}/files", api_key, body, content_type)
    digest = sha256_file(path)
    gui_url = f"https://www.virustotal.com/gui/file/{digest}"

    if status >= 400:
        message = payload.get("error", {}).get("message", "request failed")
        return f"- `{path}`: submit failed with HTTP {status}: {message}"

    analysis_id = payload.get("data", {}).get("id", "unknown")
    return f"- `{path}`: submitted as analysis `{analysis_id}`; file report {gui_url}"


def main() -> int:
    parser = argparse.ArgumentParser(description="VirusTotal release artifact lookup/submission helper.")
    parser.add_argument("--checksums", default="dist/SHA256SUMS", type=Path, help="SHA256SUMS file to read for lookups.")
    parser.add_argument("--hash", action="append", dest="hashes", default=[], help="SHA256 hash to look up.")
    parser.add_argument("--submit", action="store_true", help="Submit matching files when they are not already known.")
    parser.add_argument("--file", action="append", dest="files", default=[], help="Artifact path or glob to submit.")
    parser.add_argument("--sleep", type=float, default=15.0, help="Seconds to wait between submit and follow-up lookup.")
    args = parser.parse_args()

    api_key = os.environ.get("VIRUSTOTAL_API_KEY")
    if not api_key:
        print("VIRUSTOTAL_API_KEY is not set; skipping VirusTotal checks.")
        return 0

    hashes = list(dict.fromkeys(args.hashes + read_hashes(args.checksums)))
    print("VirusTotal release artifact report")
    print()

    for digest in hashes:
        print(lookup_hash(api_key, digest))

    if args.submit:
        paths: list[Path] = []
        patterns = args.files or ["dist/*.whl", "dist/*.tar.gz"]
        for pattern in patterns:
            paths.extend(Path(match) for match in glob.glob(pattern))

        for path in sorted(set(paths)):
            if path.is_file():
                print(submit_file(api_key, path))

        if paths and args.sleep > 0:
            time.sleep(args.sleep)
            for path in sorted(set(paths)):
                if path.is_file():
                    print(lookup_hash(api_key, sha256_file(path)))

    return 0


if __name__ == "__main__":
    sys.exit(main())
