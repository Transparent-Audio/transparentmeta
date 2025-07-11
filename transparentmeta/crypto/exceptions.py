# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""This module hosts all custom exceptions used in the crypto parckage."""


class NotEd25519KeyError(Exception):
    """Raised when a loaded key is not an Ed25519 key."""

    def __init__(self, message="Loaded key is not an Ed25519 key"):
        super().__init__(message)
