# PROJECT_CONTEXT.md

## Project
pybusy

## Overview
pybusy is a lightweight Python library for adding clean CLI busy indicators to command-line applications.

It is designed for developers who want simple visual feedback during long-running work without introducing heavy terminal UI dependencies or noisy output behavior.

pybusy should feel small, polished, and production-friendly.

---

## Problem
Many Python CLI tools perform work that takes noticeable time, but provide poor user feedback while that work is happening.

Common issues:
- no indication that work is still progressing
- messy or flickering spinner behavior
- logging output colliding with spinner rendering
- lack of simple async-friendly APIs
- overbuilt alternatives that pull in unnecessary terminal UI complexity

pybusy exists to solve the narrow but common need for clean "work is in progress" feedback.

---

## Target Users
- Python CLI tool authors
- internal tooling developers
- automation/scripting developers
- small libraries and apps that need minimal progress feedback
- developers who want something simpler than rich/textual-style UI systems

---

## Core Philosophy
- Minimal, clean output
- Tiny API surface
- Predictable behavior
- Works well with normal print/logging usage
- Friendly to both sync and async code
- Low dependency / low complexity
- Good defaults first, customization second

pybusy should be easy to adopt in under a minute.

---

## Product Positioning
pybusy is **not** a full terminal UI framework.

It is a focused utility for:
- spinners
- busy indicators
- lightweight step/progress messaging

It should be compared more against:
- "I just need a clean spinner"

than against:
- dashboard frameworks
- complex progress rendering systems
- interactive terminal apps

---

## Scope (Stage 2 / v1 expanded)
The library should support:

### 1. Spinner context manager
Simple synchronous usage:

```python
with busy("Processing..."):
    do_work()
```
