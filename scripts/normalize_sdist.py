#!/usr/bin/env python3
"""Repack a .tar.gz source distribution with stable gzip/tar metadata."""

from __future__ import annotations

import copy
import gzip
import io
import os
import sys
import tarfile
from pathlib import Path


def normalize(path: Path, mtime: int) -> None:
    entries: list[tuple[tarfile.TarInfo, bytes | None]] = []

    with tarfile.open(path, "r:gz") as source:
        for member in sorted(source.getmembers(), key=lambda item: item.name):
            normalized = copy.copy(member)
            normalized.uid = 0
            normalized.gid = 0
            normalized.uname = ""
            normalized.gname = ""
            normalized.mtime = mtime
            normalized.pax_headers = {}

            data = None
            if member.isfile():
                extracted = source.extractfile(member)
                data = extracted.read() if extracted else b""
                normalized.size = len(data)
            else:
                normalized.size = 0

            entries.append((normalized, data))

    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buffer, compresslevel=9, mtime=0) as gzip_file:
        with tarfile.open(fileobj=gzip_file, mode="w", format=tarfile.USTAR_FORMAT) as target:
            for member, data in entries:
                target.addfile(member, io.BytesIO(data) if data is not None else None)

    path.write_bytes(buffer.getvalue())


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: normalize_sdist.py dist/*.tar.gz", file=sys.stderr)
        return 2

    mtime = int(os.environ.get("SOURCE_DATE_EPOCH", "0"))
    for item in sys.argv[1:]:
        normalize(Path(item), mtime)

    return 0


if __name__ == "__main__":
    sys.exit(main())
