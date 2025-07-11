# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
Exposes the main interfaces of the transparentmeta SDK for direct import from
the `transparentmeta.sdk` package.
"""

from transparentmeta.sdk.factory import (
    build_transparent_metadata_reader,
    build_transparent_metadata_writer,
)
from transparentmeta.sdk.transparent_metadata_reader import (
    TransparentMetadataReader,
)
from transparentmeta.sdk.transparent_metadata_writer import (
    TransparentMetadataWriter,
)

__all__ = [
    "TransparentMetadataWriter",
    "TransparentMetadataReader",
    "build_transparent_metadata_writer",
    "build_transparent_metadata_reader",
]
