# pybusy

Minimal, clean CLI spinners for Python - no noise, no heavy dependencies.

![pybusy demo](media/pybusy-demo-marketing.gif)

![PyPI](https://img.shields.io/pypi/v/pybusy?cacheSeconds=60)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/github/license/krazybean/pybusy)

pybusy is a focused utility for one job: showing that work is in progress, cleanly.

It stays intentionally small while covering real CLI needs:
- sync and async context manager support
- manual spinner lifecycle control
- clean success/failure completion states
- non-TTY-safe behavior for CI and logs

## Install

```bash
pip install pybusy
```

## Quick Start

```python
from pybusy import busy
import time

with busy("Processing..."):
    time.sleep(2)
```

## Why pybusy?

- Minimal API surface you can learn in minutes
- No external runtime dependencies
- Clean terminal behavior without noisy redraw artifacts
- Works with normal CLI output patterns
- Built for practical scripts and internal tooling

## Demo

Feature showcase:

![pybusy feature demo](media/pybusy.gif)

## Usage

### Sync context manager

```python
from pybusy import busy
import time

with busy("Indexing files..."):
    time.sleep(2)
```

### Async context manager

```python
import asyncio
from pybusy import busy

async def main():
    async with busy("Waiting for API..."):
        await asyncio.sleep(2)

asyncio.run(main())
```

### Manual lifecycle control

```python
from pybusy import Spinner
import time

spin = Spinner("Connecting...")
spin.start()
time.sleep(1)
spin.update("Syncing data...")
time.sleep(1)
spin.success("Ready")
```

### Spinner styles

Built-in presets: `dots` (default), `line`, `simple`.

```python
from pybusy import busy

with busy("Deploying...", spinner="line"):
    run_deploy()
```

### Custom frames

```python
from pybusy import busy

with busy("Processing...", frames=[".", "o", "O", "o"]):
    run_job()
```

### Failure state

```python
from pybusy import spinner

s = spinner("Deploying...")
s.start()
# ...
s.failure("Something went wrong")
```

## Behavior

- Writes to `stderr` by default
- Animates only on TTYs
- Still emits clean completion lines in non-interactive environments

## Package integrity

pybusy releases are intended to be built from a tagged source commit and published to PyPI by GitHub Actions using PyPI Trusted Publishing. Trusted Publishing uses short-lived OpenID Connect credentials instead of a long-lived PyPI API token.

To inspect the source for an installed version, compare the PyPI version with the matching Git tag:

```bash
git fetch --tags
git checkout "v$(python3 -c 'import pybusy; print(pybusy.__version__)')"
```

Release builds generate SHA256 checksums for the source distribution and wheel in `dist/SHA256SUMS`. To verify downloaded artifacts against that file:

```bash
cd dist
shasum -a 256 -c SHA256SUMS
```

PyPI also supports digital attestations for packages published through supported Trusted Publishing workflows. These attestations can link a PyPI artifact to the repository, workflow, and commit that published it. They are provenance signals, not a guarantee that the code is safe or correct.

You can inspect PyPI provenance with:

```bash
python3 -m pip install pypi-attestations
export WHEEL_DIRECT_URL="https://files.pythonhosted.org/.../pybusy-<version>-py3-none-any.whl"
pypi-attestations verify pypi --repository https://github.com/krazybean/pybusy "$WHEEL_DIRECT_URL"
```

Release maintainers may optionally look up or submit artifact hashes to VirusTotal:

```bash
VIRUSTOTAL_API_KEY=... python3 scripts/virustotal_release_check.py
VIRUSTOTAL_API_KEY=... python3 scripts/virustotal_release_check.py --submit
```

VirusTotal results are an additional transparency signal. They can be delayed, rate-limited, incomplete, or contain false positives, so they should not be treated as a pass/fail security verdict.

## Building releases

For local release checks:

```bash
python3 -m pip install build twine
scripts/build-dist.sh
```

The script removes previous local build outputs, builds both the source distribution and wheel, runs `twine check` when available, and writes `dist/SHA256SUMS`. Built artifacts remain ignored by git.

## License

MIT
