from __future__ import annotations

import asyncio
import time

from pybusy import Spinner, busy


# Async alias for demo readability.
abusy = busy


def section_header(title: str) -> None:
    print(f"\n--- {title} ---")


def pause(seconds: float = 0.6) -> None:
    time.sleep(seconds)


def section_1_basic_spinner() -> None:
    # Basic spinner context manager.
    section_header("Basic Spinner")
    with busy("Processing..."):
        time.sleep(2.0)


def section_2_spinner_styles() -> None:
    # Show built-in spinner presets.
    section_header("Spinner Styles")
    for style in ("dots", "line", "simple"):
        with busy(f"Style: {style}", spinner=style):
            time.sleep(1.1)


def section_3_custom_frames() -> None:
    # Custom frame sequence example.
    section_header("Custom Frames")
    moon_frames = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
    with busy("Cycling moon phases", frames=moon_frames):
        time.sleep(1.4)


async def section_4_async_usage() -> None:
    # Async context manager usage.
    section_header("Async Usage")
    async with abusy("Awaiting async work..."):
        await asyncio.sleep(1.6)


def section_5_manual_lifecycle() -> None:
    # Manual lifecycle with in-flight updates.
    section_header("Manual Lifecycle")
    spin = Spinner("Connecting...")
    spin.start()
    time.sleep(0.8)
    spin.update("Uploading payload...")
    time.sleep(0.8)
    spin.update("Finalizing...")
    time.sleep(0.8)
    spin.success("Manual flow complete")


def section_6_step_progress() -> None:
    # Lightweight step-by-step progress.
    section_header("Step Progress")
    steps = [
        "1/4 Validate input",
        "2/4 Prepare workspace",
        "3/4 Process data",
        "4/4 Write output",
    ]
    spin = Spinner(steps[0], spinner="line")
    spin.start()
    for step in steps:
        spin.step(step)
        time.sleep(0.7)
    spin.success("All steps complete")


def section_7_failure_state() -> None:
    # Failure completion state.
    section_header("Failure State")
    with busy("Deploying release...", spinner="simple") as spin:
        time.sleep(1.3)
        spin.failure("Something went wrong")


def run_sync_sections() -> None:
    section_1_basic_spinner()
    pause()
    section_2_spinner_styles()
    pause()
    section_3_custom_frames()
    pause()


def run_post_async_sections() -> None:
    section_5_manual_lifecycle()
    pause()
    section_6_step_progress()
    pause()
    section_7_failure_state()


async def main() -> None:
    print("pybusy demo")
    run_sync_sections()
    await section_4_async_usage()
    pause()
    run_post_async_sections()
    print("\nDemo complete.")


if __name__ == "__main__":
    asyncio.run(main())
