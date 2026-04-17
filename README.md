# pybusy

![PyPI](https://img.shields.io/pypi/v/pybusy?cacheSeconds=60)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/github/license/krazybean/pybusy)

Minimal, dependency-free CLI spinner for Python.

Finally, a spinner that doesn’t get in your way.

## Install

```bash
pip install pybusy
```

## Usage

### Context manager

```python
from pybusy import spinner
import time

with spinner("Processing..."):
    time.sleep(2)
```

### Manual control

```python
from pybusy import spinner
import time

s = spinner("Loading...")
s.start()
time.sleep(2)
s.success("Done")
```

## Demo

```text
✔ Processing files...
```

## Why pybusy?

- No dependencies
- Clean terminal output
- Works in CI / non-TTY environments
- Minimal API surface
