# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
Example script: Configure logging for transparentmeta.

This script shows how to activate transparentmeta's built-in logger
configuration, which enables logging output for all internal SDK
operations.

By default:
- The logging level is set to INFO, which shows high-level messages
  (e.g., components initialized, read/write operations succeeded).
- You can set it to DEBUG to see detailed trace logs, including internal
  decisions, serialized data, and verification steps.

---

When to use this:
- Use `configure_logging()` at the start of your script if you don't
  already have your own logger configuration.
- If you're building an app or service with a centralized logging setup,
  you don't need to call this — transparentmeta logs will bubble up
  through the root logger.
"""

import logging

from transparentmeta.logger_config import configure_logging


def main():
    # Option 1: Default logging (INFO level)
    configure_logging()

    # Option 2: Uncomment to enable full trace-level output
    # configure_logging(level=logging.DEBUG)

    # Example message to show logging is active
    logging.getLogger("transparentmeta.sdk.factory").info(
        "If you see this, transparentmeta logging is working!"
    )

    # Reminder for developers
    print(
        "\nNote: You don't need to call `configure_logging()` if your app "
        "already sets up logging.\ntransparentmeta logs will propagate up "
        "through the standard logging hierarchy.\n"
    )


if __name__ == "__main__":
    main()
