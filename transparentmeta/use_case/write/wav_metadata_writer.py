# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
This module provides a `WAVMetadataWriter` class that writes metadata and
a digital signature to WAV files using the Mutagen library for ID3 tagging.
"""

from pathlib import Path
from typing import cast

from mutagen.wave import WAVE

from transparentmeta.use_case.write.metadata_writer import MetadataWriter


class WAVMetadataWriter(MetadataWriter):
    """Writes metadata and a digital signature to WAV files using Mutagen."""

    def write(self, filepath: Path, metadata: str, signature: str) -> None:
        """Writes metadata and signature ID3 TXXX fields of a WAV file.

        Args:
            filepath (Path): The WAV file path.
            metadata (str): Serialized metadata string with transparency info.
            signature (str): The signature string.
        """
        audio = WAVE(filepath)
        audio = cast(WAVE, self._write_id3_tags(audio, metadata, signature))
        audio.save()
