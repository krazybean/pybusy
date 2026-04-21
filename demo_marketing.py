from __future__ import annotations

import time

from pybusy import busy


def wait(seconds: float) -> None:
    time.sleep(seconds)


def run_step(
    message: str,
    duration: float,
    *,
    spinner: str = "dots",
    frames=None,
    success_text: str,
) -> None:
    # Run one spinner step and finish with a clean success line.
    spin = busy(message, spinner=spinner, frames=frames)
    spin.start()
    wait(duration)
    spin.success(success_text)


def main() -> None:
    print("acme-cli v1.4.0")
    wait(0.5)

    # Install / setup
    print("\n$ acme init")
    run_step("Installing dependencies", 1.6, success_text="Dependencies installed")
    run_step("Setting up workspace", 1.4, spinner="line", success_text="Workspace ready")

    # Connecting
    print("\n$ acme connect production")
    run_step("Connecting to cluster", 1.6, spinner="simple", success_text="Connected to production")

    # Processing with a custom spinner.
    print("\n$ acme process orders --batch 240")
    moon_frames = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
    run_step("Processing order data", 1.8, frames=moon_frames, success_text="240 records processed")

    # Deploy with failure, retry, then success.
    print("\n$ acme deploy --region us-central")
    deploy = busy("Deploying release", spinner="line")
    deploy.start()
    wait(1.6)
    deploy.failure("Deployment failed: timeout")

    wait(0.8)
    print("$ acme deploy --region us-central --retry")
    retry = busy("Retrying deployment", spinner="dots")
    retry.start()
    wait(1.7)
    retry.success("Deployment successful")


if __name__ == "__main__":
    main()
