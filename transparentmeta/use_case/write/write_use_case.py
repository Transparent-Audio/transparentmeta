# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
This module provides a `WriteUseCase` class with the core business logic for
the process of serializing metadata, signing it, and writing it to ID3
tags in audio files.

This class acts as a facade over `MetadataSerializer`, `Signer`, and
`MetadataWriter`.
"""

import logging
from pathlib import Path

from transparentmeta.crypto.signer import Signer
from transparentmeta.entity.metadata import Metadata
from transparentmeta.request.write_request import WriteRequest
from transparentmeta.serialization.metadata_serializer import (
    MetadataSerializer,
)
from transparentmeta.use_case.write.metadata_writer import MetadataWriter

logger = logging.getLogger(__name__)


class WriteUseCase:
    """Facade for managing metadata writing, serialization, and signing in one
    go. It takes care of the core business logic for writing metadata to audio
    files.

    This class simplifies metadata writing by:
    1. Serializing metadata using `MetadataSerializer`.
    2. Creating a signature using `Signer`.
    3. Writing metadata and its signature to an audio file using a concrete
       MetadataWriter.

    Attributes:
        metadata_serializer (MetadataSerializer): Handles serialization.
        signer (Signer): Handles signing metadata.
        metadata_writer (MetadataWriter): Writes metadata to audio files.
    """

    def __init__(
        self,
        metadata_serializer: MetadataSerializer,
        signer: Signer,
        metadata_writer: MetadataWriter,
    ) -> None:
        """Initializes the WriteUseCase with serializer, signer, and
        writer.

        Args:
            metadata_serializer (MetadataSerializer): The Metadata serializer.
            signer (Signer): The signer for generating metadata signatures.
            metadata_writer (MetadataWriter): The writer for embedding
                metadata.
        """
        self.metadata_serializer = metadata_serializer
        self.signer = signer
        self._metadata_writer = metadata_writer

    @property
    def metadata_writer(self) -> MetadataWriter:
        """Gets the current metadata writer.

        Returns:
            MetadataWriter: The active metadata writer instance.
        """
        return self._metadata_writer

    @metadata_writer.setter
    def metadata_writer(self, writer: MetadataWriter) -> None:
        """Sets a new metadata writer dynamically.

        Args:
            writer (MetadataWriter): The new metadata writer to use.
        """
        self._metadata_writer = writer

    def write(self, write_request: WriteRequest) -> None:
        """Serializes metadata, signs it, and writes it to the audio file in
        ID3 tags.

        Args:
            write_request (WriteRequest): The request containing the
                filepath and metadata to write.
        """
        metadata = write_request.metadata
        filepath = write_request.filepath

        logger.debug(
            "Serializing metadata for file %s", write_request.filepath
        )
        serialized_metadata = self._serialize_metadata(metadata)

        logger.debug("Signing metadata for file %s", write_request.filepath)
        signature_payload = self._sign_metadata(serialized_metadata)

        logger.debug(
            "Writing metadata and signature to ID3 tags for file %s",
            write_request.filepath,
        )
        self._write_metadata_and_signature_in_id3_tags(
            filepath, serialized_metadata, signature_payload
        )

    def _serialize_metadata(self, metadata: Metadata) -> str:
        return self.metadata_serializer.serialize(metadata)

    def _sign_metadata(self, serialized_metadata: str) -> str:
        return self.signer.sign(serialized_metadata)

    def _write_metadata_and_signature_in_id3_tags(
        self, filepath: Path, serialized_metadata: str, signature: str
    ) -> None:
        self.metadata_writer.write(filepath, serialized_metadata, signature)
