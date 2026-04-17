# pybusy

Minimal, dependency-free CLI spinner for Python.

Finally, a Python spinner that isn't bloated.

No configuration. No bloat. Just works.

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

## Why pybusy?

- No dependencies
- Clean terminal output
- Works in CI / non-TTY environments
- Minimal API surface
- Designed for real CLI tools

## Build and publish

```bash
# Build
python -m build

# Upload (first time)
pip install twine
twine upload dist/*
```
