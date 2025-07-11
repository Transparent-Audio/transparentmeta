# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
This module defines the CharacterEncoding enumeration, which provides
standard character encoding options for string-to-byte conversions.
"""

from enum import Enum


class CharacterEncoding(Enum):
    """Enum for character encoding options."""

    UTF8 = "utf-8"
    ASCII = "ascii"
