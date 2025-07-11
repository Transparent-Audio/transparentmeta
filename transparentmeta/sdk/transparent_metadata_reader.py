# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
SDK entry point for reading digitally signed metadata from audio files.

The `TransparentMetadataReader` class acts as a user-facing API that handles
deserialization and signature verification of metadata embedded in MP3 or
WAV files through a single method call.
"""

import logging
from pathlib import Path

from transparentmeta.request.read_request import ReadRequest
from transparentmeta.result.result import ReadResult
from transparentmeta.use_case.read.read_use_case import ReadUseCase
from transparentmeta.use_case.read.reader_selector import ReaderSelector
from transparentmeta.utils.file_utils import get_file_extension

logger = logging.getLogger(__name__)


class TransparentMetadataReader:
    """High-level interface for reading transparency metadata from audio files.

    The TransparentMetadataReader coordinates the extraction, deserialization,
    and signature verification of metadata embedded in supported audio formats.
    It delegates verification to the ReadUseCase and uses a ReaderSelector to
    choose the appropriate metadata reader based on file extension.

    Attributes:
        read_use_case (ReadUseCase): Handles deserialization and signature
            verification.
        reader_selector (ReaderSelector): Selects the appropriate reader
            based on file format.
    """

    def __init__(
        self, read_use_case: ReadUseCase, reader_selector: ReaderSelector
    ) -> None:
        """Initializes the TransparentMetadataReader.

        Args:
            read_use_case (ReadUseCase): The use case for metadata extraction
                and signature verification.
            reader_selector (ReaderSelector): Resolves format-specific readers
                based on the extension of the audio file passed.
        """
        self.read_use_case = read_use_case
        self.reader_selector = reader_selector

    def read(self, filepath: Path) -> ReadResult:
        """Reads and verifies transparency metadata from an audio file.

        Selects the appropriate metadata reader based on file extension
        (e.g., 'mp3', 'wav', 'wave'), extracts and deserializes the metadata,
        and verifies its digital signature.

        Args:
            filepath (Path): Path to the audio file from which metadata should
                be read and verified.

        Returns:
            ReadResult: Contains the extracted metadata, validation status,
                and any related error information.
        """
        logger.info("Starting metadata read for file: %s", filepath)

        read_request = ReadRequest(filepath=filepath)
        read_result = self._read_metadata(read_request)

        self._log_read_outcome(filepath, read_result)
        return read_result

    def _read_metadata(self, read_request: ReadRequest) -> ReadResult:
        extension = get_file_extension(read_request.filepath)
        self.read_use_case.metadata_reader = self.reader_selector.get_reader(
            extension
        )
        return self.read_use_case.read(read_request)

    def _log_read_outcome(
        self, filepath: Path, read_result: ReadResult
    ) -> None:
        if not read_result.is_success:
            logger.info(
                "Metadata read failed for file %s: %s",
                filepath,
                read_result.error or "Unknown error",
            )
        else:
            logger.info("Successfully read metadata from file: %s", filepath)
