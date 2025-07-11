# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
This module provides an `MP3MetadataReader` class that reads transparency
metadata and a digital signature from MP3 files using Mutagen's ID3 tagging
system.
"""

from pathlib import Path

from mutagen.id3 import ID3
from mutagen.mp3 import MP3

from transparentmeta.use_case.read.metadata_reader import MetadataReader


class MP3MetadataReader(MetadataReader):
    """Reads transparency metadata and a digital signature from MP3 files.

    This class loads an MP3 file and retrieves values from custom ID3 TXXX
    fields, providing consistent access to signed metadata.
    """

    def _load_audio(self, filepath: Path) -> MP3:
        """Loads the MP3 file and returns an object that supports ID3 tags.

        Args:
            filepath (Path): The path to the MP3 file.

        Returns:
            MP3: A Mutagen MP3 object with ID3 tag support.
        """
        return MP3(filepath, ID3=ID3)
