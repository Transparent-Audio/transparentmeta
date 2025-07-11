# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
This module provides an abstract `MetadataReader` class that defines the
interface for reading metadata and a digital signature from audio files using
ID3, using the Mutagen library for audio file handling.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, cast

from mutagen.id3 import ID3

from transparentmeta.use_case.constants import (
    SIGNATURE_FIELD,
    TRANSPARENCY_METADATA_FIELD,
)
from transparentmeta.use_case.types import MutagenID3AudioTypes
from transparentmeta.utils.metadata_tags_utils import (
    does_file_contain_any_id3_tags,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AudioFileDataReading:
    """
    Represents the result of reading metadata and signature from an audio file.

    Attributes:
        metadata (Optional[str]): The serialized metadata string, if found.
        signature (Optional[str]): The digital signature string, if found.
        is_success (bool): Indicates whether both metadata and signature were
            successfully retrieved.
    """

    is_success: bool
    metadata: Optional[str] = None
    signature: Optional[str] = None


class MetadataReader(ABC):
    """Abstract base class for reading metadata and a digital signature from
    ID3 metadata tags.

    Subclasses should implement the `_load_audio()` method for specific file
    formats (e.g., MP3, WAV).

    This class ensures consistency in how transparency metadata and its
    signature are retrieved.

    Attributes:
        transparency_metadata_field (str): ID3 TXXX field used to store
            transparency metadata. Defaults to "transparency".
        signature_field (str): ID3 TXXX field used to store the metadata
            signature. Defaults to "signature".
    """

    def __init__(
        self,
        transparency_metadata_field: str = TRANSPARENCY_METADATA_FIELD,
        signature_field: str = SIGNATURE_FIELD,
    ) -> None:
        """Initializes the MetadataReader with custom metadata and signature
        fields.

        Args:
            transparency_metadata_field (str): ID3 TXXX field used to store
                transparency metadata.
            signature_field (str): ID3 TXXX field used to store the signature.
        """
        self.transparency_metadata_field = transparency_metadata_field
        self.signature_field = signature_field
        self._custom_id3_tag_field = "TXXX"
        self._metadata_field = self._initiate_metadata_field()
        self._signature_field = self._initiate_signature_field()

    def read(self, filepath: Path) -> AudioFileDataReading:
        """Reads metadata and its signature from the specified audio file.

        This method uses the tags defined by `transparency_metadata_field` and
        `signature_field` to extract the information from ID3 tags.

        Args:
            filepath (Path): Path to the audio file to read.

        Returns:
            audio_file_data_reading (AudioFileDataReading): An object
                containing the metadata, signature, and success info. If
                either the metadata or the signature is missing,
                `is_success` will be False.
        """
        audio = self._load_audio(filepath)

        if not does_file_contain_any_id3_tags(audio):
            return AudioFileDataReading(
                metadata=None,
                signature=None,
                is_success=False,
            )

        if not self._do_metadata_and_signature_tags_exist(audio):
            return AudioFileDataReading(
                metadata=None,
                signature=None,
                is_success=False,
            )

        audio_file_data_reading = AudioFileDataReading(
            metadata=self._extract_metadata(audio),
            signature=self._extract_signature(audio),
            is_success=True,
        )

        logger.debug(
            "Read metadata and signature from file %s. Metadata: '%.40s'. "
            "Signature: '%s'",
            filepath,
            audio_file_data_reading.metadata,
            audio_file_data_reading.signature,
        )

        return audio_file_data_reading

    @abstractmethod
    def _load_audio(self, filepath: Path) -> MutagenID3AudioTypes:
        """Loads and returns an audio object for the given file path.

        Subclasses must implement this method to provide format-specific
        loading logic.

        Args:
            filepath (Path): The path to the audio file.

        Returns:
            An audio object that supports ID3 tagging.
        """

    def _initiate_metadata_field(self) -> str:
        return (
            f"{self._custom_id3_tag_field}:{self.transparency_metadata_field}"
        )

    def _initiate_signature_field(self) -> str:
        return f"{self._custom_id3_tag_field}:{self.signature_field}"

    def _extract_metadata(self, audio: MutagenID3AudioTypes) -> str:
        tags = cast(ID3, audio.tags)
        return tags[self._metadata_field].text[0]

    def _extract_signature(self, audio: MutagenID3AudioTypes) -> str:
        tags = cast(ID3, audio.tags)
        return tags[self._signature_field].text[0]

    def _do_metadata_and_signature_tags_exist(
        self, audio: MutagenID3AudioTypes
    ) -> bool:
        assert audio.tags is not None
        return (
            self._metadata_field in audio.tags
            and self._signature_field in audio.tags
        )
