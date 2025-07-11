# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
This module defines a registry of available metadata writers (e.g., for MP3 and
WAV) and provides the `WriterSelector` class to dispatch the correct writer
instance based on the file extension of an audio file. It serves as an
abstraction layer to decouple audio format-specific logic from higher-level
orchestration.
"""

import logging
from types import MappingProxyType
from typing import Mapping

from transparentmeta.use_case.write.metadata_writer import MetadataWriter
from transparentmeta.use_case.write.mp3_metadata_writer import (
    MP3MetadataWriter,
)
from transparentmeta.use_case.write.wav_metadata_writer import (
    WAVMetadataWriter,
)

mp3_metadata_writer = MP3MetadataWriter()
wav_metadata_writer = WAVMetadataWriter()

MetadataWriterRegistry = Mapping[str, MetadataWriter]
metadata_writer_registry = MappingProxyType(
    {
        "mp3": mp3_metadata_writer,
        "wav": wav_metadata_writer,
        "wave": wav_metadata_writer,
    }
)

logger = logging.getLogger(__name__)


class WriterSelector:
    """Selects the appropriate MetadataWriter based on the audio file
    extension.

    This class acts as a lightweight strategy resolver for mapping file
    extensions (such as 'mp3', 'wav', or 'wave') to their corresponding
    metadata writer instances. It abstracts away the logic of
    format-specific handling, promoting modularity and extensibility.

    Attributes:
        metadata_writers (MetadataWriterRegistry):
            A mapping of file extensions to metadata writer instances.
    """

    def __init__(
        self,
        metadata_writers: MetadataWriterRegistry = metadata_writer_registry,
    ):
        """Initializes the WriterSelector with a registry of available
        metadata writers.

        Args:
            metadata_writers (MetadataWriterRegistry): An immutable
                dictionary mapping file extensions to their corresponding
                metadata writer implementations.
        """
        self.metadata_writers = metadata_writers

    def get_writer(self, file_format: str) -> MetadataWriter:
        """Selects the appropriate metadata writer based on the file extension.

        Args:
            file_format (str): The file extension of the audio file (e.g.,
                'mp3', 'wav').

        Returns:
            metadata_writer (MetadataWriter): The corresponding metadata
                writer for the file extension.
        """
        lower_file_format = file_format.lower()
        metadata_writer = self.metadata_writers[lower_file_format]

        logger.debug(
            "Selected metadata writer for '%s': %s",
            lower_file_format,
            type(metadata_writer).__name__,
        )

        return metadata_writer
