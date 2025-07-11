# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""This module hosts all custom exceptions used in utils."""


class InvalidHexadecimalStringError(Exception):
    """Raised when a string is not a valid hexadecimal string."""

    def __init__(self, string):
        super().__init__(f"String {string} is not a valid hexadecimal string")
