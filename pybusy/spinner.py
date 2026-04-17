from __future__ import annotations

import itertools
import shutil
import sys
import threading
import time

from .styles import STYLES

HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"


class Spinner:
    def __init__(self, message: str, style: str = "dots"):
        self.message = message
        self.frames = STYLES.get(style, STYLES["dots"])
        self.interval = 0.1
        self._start_delay = 0.1
        self._enabled = sys.stdout.isatty()
        self._stop = threading.Event()
        self._lock = threading.Lock()
        self._thread = None
        self._running = False
        self._cursor_hidden = False
        self._last_length = 0

    def start(self):
        if self._thread and self._thread.is_alive():
            return self
        if not self._enabled:
            return self
        self._running = True
        self._stop.clear()
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()
        return self

    def _write(self, text: str):
        with self._lock:
            sys.stdout.write(text)
            sys.stdout.flush()

    def _terminal_width(self):
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

    def stop(self):
        self._running = False
        self._stop.set()
        thread = self._thread
        if thread and thread.is_alive() and thread is not threading.current_thread():
            thread.join()
        self._clear()
        self._show_cursor()

    def _finish(self, symbol: str, default_message: str, message: str = None):
        self.stop()
        text = default_message if message is None else message
        self._write(f"{symbol} {text}\n")

    def success(self, message: str = None):
        self._finish("✔", "Done", message)

    def fail(self, message: str = None):
        self._finish("✖", "Failed", message)

    def update(self, message: str):
        self.message = message

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            self.fail("Failed")
        else:
            self.success("Done")
        return False


def spinner(message: str, style: str = "dots"):
    return Spinner(message, style)
