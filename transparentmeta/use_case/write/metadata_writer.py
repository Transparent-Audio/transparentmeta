# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
This module provides an abstract `MetadataWriter` class that defines the
interface for writing metadata and a digital signature to audio files using ID3.
"""

import logging
from abc import ABC, abstractmethod
from pathlib import Path

from transparentmeta.use_case.constants import (
    SIGNATURE_FIELD,
    TRANSPARENCY_METADATA_FIELD,
)
from transparentmeta.use_case.types import MutagenID3AudioTypes
from transparentmeta.utils.metadata_tags_utils import (
    create_id3_tags_in_file_if_none_exists,
    set_txxx_id3_tag,
)

logger = logging.getLogger(__name__)


class MetadataWriter(ABC):
    """
    Abstract base class for writing metadata and a digital signature to audio
    files using ID3 tagging.

    This class provides a standard interface for writing metadata in ID3-based
    formats like MP3 and WAV. It ensures metadata consistency across
    different audio file types by using TXXX frames.

    The class uses the mutagen library to inject ID3 tags into audio files.

    Subclasses should implement the `write()` method for specific file formats
    (e.g., MP3, WAV).

    Attributes:
        transparency_metadata_field (str): ID3 TXXX field for storing
            metadata.
        signature_field (str): ID3 TXXX field for storing the metadata
            signature.
    """

    def __init__(
        self,
        transparency_metadata_field: str = TRANSPARENCY_METADATA_FIELD,
        signature_field: str = SIGNATURE_FIELD,
    ) -> None:
        """
        Initializes the MetadataWriter with custom metadata and signature
        fields.

        Args:
            transparency_metadata_field (str): ID3 TXXX field for storing
                metadata.
            signature_field (str): ID3 TXXX field for storing the metadata
                signature.
        """
        self.transparency_metadata_field = transparency_metadata_field
        self.signature_field = signature_field

    @abstractmethod
    def write(self, filepath: Path, metadata: str, signature: str) -> None:
        """Writes metadata and a digital signature to an audio file. This
        method must be implemented by subclasses.

        Args:
            filepath (Path): The path to the audio file.
            metadata (str): The serialized metadata string with transparency
                info.
            signature (str): The signature string.
        """

    def _write_id3_tags(
        self, audio: MutagenID3AudioTypes, metadata: str, signature: str
    ) -> MutagenID3AudioTypes:
        """Applies metadata and a digital signature to an ID3-tagged audio file.

        This method ensures the audio file has ID3 tags and then writes
        metadata and signature to TXXX frames.

        Args:
            audio (MutagenID3AudioTypes): A Mutagen audio file object with ID3
                support.
            metadata (str): Serialized metadata string.
            signature (str): The digital signature string.

        Returns:
            MutagenID3AudioTypes: The modified audio file object with ID3
                metadata tags.
        """
        audio = create_id3_tags_in_file_if_none_exists(audio)
        audio = self._set_metadata_id3_tag(audio, metadata)
        audio = self._set_signature_id3_tag(audio, signature)

        logger.debug(
            "Data written to ID3 tags. Metadata: '%.40s'. Signature: '%s'",
            metadata,
            signature,
        )

        return audio

    def _set_metadata_id3_tag(
        self, audio: MutagenID3AudioTypes, metadata: str
    ) -> MutagenID3AudioTypes:
        return set_txxx_id3_tag(
            audio, self.transparency_metadata_field, metadata
        )

    def _set_signature_id3_tag(
        self, audio: MutagenID3AudioTypes, signature: str
    ) -> MutagenID3AudioTypes:
        return set_txxx_id3_tag(audio, self.signature_field, signature)
