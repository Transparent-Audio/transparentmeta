# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

"""
Module featuring constants for core business logic in the use case package.
"""

from typing import Tuple

SUPPORTED_AUDIO_FORMATS: Tuple[str, ...] = ("mp3", "wav", "wave")

TRANSPARENCY_METADATA_FIELD: str = "transparency"
SIGNATURE_FIELD: str = "signature"
