# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
SDK entry point for writing digitally signed metadata to audio files.

This module defines the `TransparentMetadataWriter` class, which acts as a
high-level orchestrator for embedding transparency metadata into
AI-generated audio content (e.g., MP3 or WAV). It handles metadata
preparation, format-specific writer selection, and invocation of the
underlying write use case.
"""

import logging
from pathlib import Path
from typing import Dict

from transparentmeta.entity.metadata import Metadata
from transparentmeta.request.write_request import WriteRequest
from transparentmeta.use_case.write.write_use_case import WriteUseCase
from transparentmeta.use_case.write.writer_selector import WriterSelector
from transparentmeta.utils.file_utils import get_file_extension

logger = logging.getLogger(__name__)


class TransparentMetadataWriter:
    """High-level interface for writing transparency metadata to audio files.

    The TransparentMetadataWriter coordinates the serialization, signing, and
    embedding of metadata into supported audio formats. It delegates signing to
    the WriteUseCase and uses a WriterSelector to choose the appropriate
    metadata writer based on file extension.

    Attributes:
        write_use_case (WriteUseCase): Handles signing and writing of metadata.
        writer_selector (WriterSelector): Resolves the appropriate writer for
            each file format.
    """

    def __init__(
        self, write_use_case: WriteUseCase, writer_selector: WriterSelector
    ) -> None:
        """Initializes the TransparentMetadataWriter.

        Args:
            write_use_case (WriteUseCase): The use case handling metadata
                signing and writing.
            writer_selector (WriterSelector): Format resolver for metadata
                writers.
        """
        self.write_use_case = write_use_case
        self.writer_selector = writer_selector

    def write(self, filepath: Path, metadata: Dict) -> None:
        """Writes signed transparency metadata to an audio file.

        This method constructs a WriteRequest from the given metadata,
        selects the appropriate metadata writer based on the file extension,
        and delegates the actual write operation to the WriteUseCase.

        Args:
            filepath (Path): Path to the target audio file (e.g., 'track.mp3').
            metadata (Dict): A dictionary of metadata fields. Must match the
                structure expected by `Metadata`. Example:

                {
                    "company": "Transparent Audio",
                    "model": "v2.1",
                    "created_at": datetime.utcnow(),
                    "ai_usage_level": AIUsageLevel.AI_ASSISTED,
                    "content_id": "12345abcd",
                    "user_id": "user_67890",
                    "private_key_id": "dummy_private_key_id",
                    "additional_info": {
                        "attribution": {
                            "lyrics": "John Doe",
                            "composer": "Jane Smith"
                        }
                    }
                }
        """
        logger.info("Starting metadata write for file: %s", filepath)

        write_request = WriteRequest(
            filepath=filepath, metadata=Metadata(**metadata)
        )
        self._write_metadata(write_request)

        logger.info(
            "Successfully wrote metadata with signature to file: %s", filepath
        )

    def _write_metadata(self, write_request: WriteRequest) -> None:
        extension = get_file_extension(write_request.filepath)
        self.write_use_case.metadata_writer = self.writer_selector.get_writer(
            extension
        )
        self.write_use_case.write(write_request)
