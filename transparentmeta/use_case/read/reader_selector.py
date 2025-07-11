# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
Module for selecting the appropriate metadata reader based on audio file format.

This module defines a registry of available metadata readers (e.g., for MP3 and
WAV) and provides the `ReaderSelector` class to dispatch the correct reader
instance based on the file extension. It serves as an abstraction layer to
decouple audio format-specific logic from higher-level orchestration.
"""

import logging
from types import MappingProxyType
from typing import Mapping

from transparentmeta.use_case.read.metadata_reader import MetadataReader
from transparentmeta.use_case.read.mp3_metadata_reader import MP3MetadataReader
from transparentmeta.use_case.read.wav_metadata_reader import WAVMetadataReader

mp3_metadata_reader = MP3MetadataReader()
wav_metadata_reader = WAVMetadataReader()

MetadataReaderRegistry = Mapping[str, MetadataReader]
metadata_reader_registry = MappingProxyType(
    {
        "mp3": mp3_metadata_reader,
        "wav": wav_metadata_reader,
        "wave": wav_metadata_reader,
    }
)

logger = logging.getLogger(__name__)


class ReaderSelector:
    """Selects the appropriate MetadataReader based on the audio file extension.

    This class acts as a lightweight strategy resolver for mapping file
    extensions (such as 'mp3', 'wav', or 'wave') to their corresponding
    metadata reader instances. It abstracts away the logic of
    format-specific handling, promoting modularity and extensibility.

    Attributes:
        metadata_readers (Mapping[str, MetadataReader]): An immutable mapping
            of file extensions to metadata reader instances.
    """

    def __init__(
        self,
        metadata_readers: Mapping[
            str, MetadataReader
        ] = metadata_reader_registry,
    ):
        """Initializes the ReaderSelector with a registry of metadata readers.

        Args:
            metadata_readers (Mapping[str, MetadataReader]): An immutable
            dictionary mapping file extensions to their corresponding
            metadata reader implementations.
        """
        self.metadata_readers = metadata_readers

    def get_reader(self, file_format: str) -> MetadataReader:
        """Selects the appropriate metadata reader based on the file extension.

        Args:
            file_format (str): The file extension of the audio file (e.g.,
                'mp3', 'wav').

        Returns:
            metadata_reader (MetadataReader): The corresponding metadata
                reader for the file extension.
        """
        lower_file_format = file_format.lower()
        metadata_reader = self.metadata_readers[lower_file_format]

        logger.debug(
            "Selected metadata reader for '%s': %s",
            lower_file_format,
            type(metadata_reader).__name__,
        )

        return metadata_reader
