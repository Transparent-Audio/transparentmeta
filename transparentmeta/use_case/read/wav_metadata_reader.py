# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
This module provides a `WAVMetadataReader` class that reads transparency
metadata and a digital signature from WAV files using Mutagen's ID3 tagging
system.
"""

from pathlib import Path

from mutagen.wave import WAVE

from transparentmeta.use_case.read.metadata_reader import MetadataReader


class WAVMetadataReader(MetadataReader):
    """Reads transparency metadata and a digital signature from WAV files.

    This class loads a WAV file and retrieves values from custom ID3 TXXX
    fields, enabling consistent extraction of signed metadata.
    """

    def _load_audio(self, filepath: Path) -> WAVE:
        """Loads the WAV file and returns an object that supports ID3 tags.

        Args:
            filepath (Path): The path to the WAV file.

        Returns:
            WAVE: A Mutagen WAVE object with ID3 tag support.
        """
        return WAVE(filepath)
