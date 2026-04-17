# pybusy

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
