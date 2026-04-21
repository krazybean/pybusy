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

## License

MIT
