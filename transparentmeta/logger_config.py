# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
Logging configuration for the transparentmeta library.

This module provides a utility function to configure a default logger
for the library. In most cases, users of the library should configure their
own logging and control output from `transparentmeta` using standard Python
logging.
"""

import logging


def configure_logging(level=logging.INFO):
    """Configures logging for the transparentmeta library.

    This function sets up a logger named 'transparentmeta' with a stream
    handler, formatter, and log level. It avoids adding duplicate handlers
    if already set.

    Args:
        level (int): The logging level (e.g., logging.INFO, logging.DEBUG).
            Defaults to logging.INFO.

    Notes:
        - If the logger already has handlers, no changes are made.
        - This function is optional. Users can instead configure logging
            themselves.
    """
    logger = logging.getLogger("transparentmeta")
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s.%(funcName)s: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
