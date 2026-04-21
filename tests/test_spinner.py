import asyncio
import io
import time
import unittest

from pybusy.spinner import HIDE_CURSOR, SHOW_CURSOR, Spinner, busy, spinner
from pybusy.styles import STYLES


class MemoryStream(io.StringIO):
    def __init__(self, tty=False):
        super().__init__()
        self._tty = tty

    def isatty(self):
        return self._tty


class SpinnerTests(unittest.TestCase):
    def test_preset_spinner_selection(self):
        s = busy("Processing", spinner="line")
        self.assertEqual(s.frames, STYLES["line"])

    def test_custom_frames_usage(self):
        custom = [".", "o", "O", "o"]
        s = busy("Processing", frames=custom)
        self.assertEqual(s.frames, custom)

    def test_invalid_spinner_name_falls_back_to_dots(self):
        s = busy("Processing", spinner="not-a-spinner")
        self.assertEqual(s.frames, STYLES["dots"])

    def test_sync_context_success_non_tty(self):
        stream = MemoryStream(tty=False)

        with busy("Processing", stream=stream):
            pass

        out = stream.getvalue()
        self.assertTrue(out.endswith("✔ Done\n"))
        self.assertNotIn("\r", out)
        self.assertNotIn(HIDE_CURSOR, out)

    def test_sync_context_failure_non_tty(self):
        stream = MemoryStream(tty=False)

        with self.assertRaises(RuntimeError):
            with spinner("Processing", stream=stream):
                raise RuntimeError("boom")

        self.assertTrue(stream.getvalue().endswith("✖ Failed\n"))

    def test_async_context_manager_success(self):
        stream = MemoryStream(tty=False)

        async def _run():
            async with busy("Async work", stream=stream):
                await asyncio.sleep(0)

        asyncio.run(_run())
        self.assertTrue(stream.getvalue().endswith("✔ Done\n"))

    def test_manual_lifecycle_and_updates(self):
        stream = MemoryStream(tty=False)
        s = Spinner("Loading", stream=stream)

        s.start()
        s.update("Step 1")
        s.step("Step 2")
        s.success("Completed")

        self.assertEqual(s.message, "Step 2")
        self.assertTrue(stream.getvalue().endswith("✔ Completed\n"))

    def test_failure_aliases(self):
        stream = MemoryStream(tty=False)
        s = spinner("Loading", stream=stream)
        s.fail("Nope")
        s.failure("Still nope")

        out = stream.getvalue()
        self.assertIn("✖ Nope\n", out)
        self.assertTrue(out.endswith("✖ Still nope\n"))

    def test_tty_spinner_hides_and_shows_cursor_on_stop(self):
        stream = MemoryStream(tty=True)
        s = spinner("Loading", stream=stream, start_delay=0.0, interval=0.01)

        s.start()
        time.sleep(0.03)
        s.stop()

        out = stream.getvalue()
        self.assertIn(HIDE_CURSOR, out)
        self.assertIn(SHOW_CURSOR, out)


if __name__ == "__main__":
    unittest.main()
