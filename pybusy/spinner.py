from __future__ import annotations

import itertools
import shutil
import sys
import threading
import time
from typing import List, Optional, TextIO

from .styles import STYLES

HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"


def _resolve_frames(spinner_name: str, frames: Optional[List[str]]) -> List[str]:
    if frames:
        return list(frames)
    return STYLES.get(spinner_name, STYLES["dots"])


class Spinner:
    def __init__(
        self,
        message: str,
        style: str = "dots",
        spinner: Optional[str] = None,
        frames: Optional[List[str]] = None,
        stream: Optional[TextIO] = None,
        interval: float = 0.1,
        start_delay: float = 0.1,
    ):
        self.message = message
        spinner_name = spinner if spinner is not None else style
        self.frames = _resolve_frames(spinner_name, frames)
        self.interval = interval
        self._start_delay = start_delay
        self.stream = stream if stream is not None else sys.stderr
        self._enabled = bool(getattr(self.stream, "isatty", lambda: False)())
        self._stop = threading.Event()
        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None
        self._running = False
        self._cursor_hidden = False
        self._last_length = 0

    def _write(self, text: str):
        with self._lock:
            self.stream.write(text)
            self.stream.flush()

    def _terminal_width(self) -> int:
        return shutil.get_terminal_size(fallback=(80, 24)).columns

    def _hide_cursor(self):
        if self._enabled and not self._cursor_hidden:
            self._write(HIDE_CURSOR)
            self._cursor_hidden = True

    def _show_cursor(self):
        if self._enabled and self._cursor_hidden:
            self._write(SHOW_CURSOR)
            self._cursor_hidden = False

    def _clear(self):
        if not self._enabled:
            return
        width = max(self._terminal_width(), self._last_length)
        self._write("\r" + (" " * width) + "\r")
        self._last_length = 0

    def _animate(self):
        try:
            if self._stop.wait(self._start_delay):
                return
            self._hide_cursor()
            for frame in itertools.cycle(self.frames):
                if self._stop.is_set() or not self._running:
                    break
                line = f"{frame} {self.message}"
                padded = line.ljust(self._last_length)
                self._write("\r" + padded)
                self._last_length = len(padded)
                if self._stop.is_set() or not self._running:
                    break
                time.sleep(self.interval)
        finally:
            self._running = False
            self._show_cursor()

    def start(self) -> "Spinner":
        if self._thread and self._thread.is_alive():
            return self
        if not self._enabled:
            return self

        self._running = True
        self._stop.clear()
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()
        return self

    def stop(self) -> "Spinner":
        self._running = False
        self._stop.set()
        thread = self._thread
        if thread and thread.is_alive() and thread is not threading.current_thread():
            thread.join()
        self._clear()
        self._show_cursor()
        return self

    def _finish(self, symbol: str, default_message: str, message: Optional[str] = None) -> "Spinner":
        self.stop()
        text = default_message if message is None else message
        self._write(f"{symbol} {text}\n")
        return self

    def success(self, message: Optional[str] = None) -> "Spinner":
        return self._finish("✔", "Done", message)

    def failure(self, message: Optional[str] = None) -> "Spinner":
        return self._finish("✖", "Failed", message)

    def fail(self, message: Optional[str] = None) -> "Spinner":
        return self.failure(message)

    def update(self, message: str) -> "Spinner":
        self.message = message
        return self

    def step(self, message: str) -> "Spinner":
        return self.update(message)

    def __enter__(self) -> "Spinner":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc_type is not None:
            self.failure("Failed")
        else:
            self.success("Done")
        return False

    async def __aenter__(self) -> "Spinner":
        return self.__enter__()

    async def __aexit__(self, exc_type, exc, tb) -> bool:
        return self.__exit__(exc_type, exc, tb)


def spinner(
    message: str,
    style: str = "dots",
    spinner: Optional[str] = None,
    frames: Optional[List[str]] = None,
    stream: Optional[TextIO] = None,
    interval: float = 0.1,
    start_delay: float = 0.1,
) -> Spinner:
    return Spinner(
        message,
        style=style,
        spinner=spinner,
        frames=frames,
        stream=stream,
        interval=interval,
        start_delay=start_delay,
    )


def busy(
    message: str,
    style: str = "dots",
    spinner: Optional[str] = None,
    frames: Optional[List[str]] = None,
    stream: Optional[TextIO] = None,
    interval: float = 0.1,
    start_delay: float = 0.1,
) -> Spinner:
    return Spinner(
        message,
        style=style,
        spinner=spinner,
        frames=frames,
        stream=stream,
        interval=interval,
        start_delay=start_delay,
    )
