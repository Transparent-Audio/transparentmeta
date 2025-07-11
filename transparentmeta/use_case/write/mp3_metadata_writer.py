# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
This module provides a `MP3MetadataWriter` class that writes metadata and
a digital signature to MP3 files using the Mutagen library for ID3 tagging.
"""

from pathlib import Path
from typing import cast

from mutagen.id3 import ID3
from mutagen.mp3 import MP3

from transparentmeta.use_case.write.metadata_writer import MetadataWriter


class MP3MetadataWriter(MetadataWriter):
    """Writes metadata and a digital signature to MP3 files."""

    def write(self, filepath: Path, metadata: str, signature: str) -> None:
        """Writes metadata and signature to ID3 TXXX fields of an MP3 file.

        Args:
            filepath (Path): The MP3 file path.
            metadata (str): Serialized use_case string with transparency info.
            signature (str): The signature string.
        """
        audio = MP3(filepath, ID3=ID3)
        audio = cast(MP3, self._write_id3_tags(audio, metadata, signature))
        audio.save()
