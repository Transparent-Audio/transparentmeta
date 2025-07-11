# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
This module provides a `ReadUseCase` class with the core business logic for
reading, verifying, and deserializing transparency metadata from audio files.
It acts as a facade over `MetadataReader`, `SignatureVerifier`, and
`MetadataSerializer`.
"""

import logging
from typing import cast

from transparentmeta.crypto.signature_verifier import SignatureVerifier
from transparentmeta.entity.metadata import Metadata
from transparentmeta.request.read_request import ReadRequest
from transparentmeta.result.result import ReadResult
from transparentmeta.serialization.metadata_serializer import (
    MetadataSerializer,
)
from transparentmeta.use_case.read.metadata_reader import (
    AudioFileDataReading,
    MetadataReader,
)

logger = logging.getLogger(__name__)


class ReadUseCase:
    """Facade for managing the reading, signature verification, and
    deserialization of transparency metadata from audio files.

    This class simplifies the process by:
    1. Extracting metadata and its signature from an audio file using
       `MetadataReader`.
    2. Verifying the signature using `SignatureVerifier`.
    3. Deserializing the metadata using `MetadataSerializer`.

    Attributes:
        metadata_reader (MetadataReader): The reader responsible for extracting
            metadata and signature from the file.
        signature_verifier (SignatureVerifier): Verifies the digital signature
            of the metadata.
        metadata_serializer (MetadataSerializer): Deserializes the raw metadata
            string into a metadata object.
    """

    def __init__(
        self,
        metadata_reader: MetadataReader,
        signature_verifier: SignatureVerifier,
        metadata_serializer: MetadataSerializer,
    ) -> None:
        """Initializes the ReadUseCase with reader, verifier, and serializer.

        Args:
            metadata_reader (MetadataReader): The metadata reader.
            signature_verifier (SignatureVerifier): The signature verifier.
            metadata_serializer (MetadataSerializer): The metadata deserializer.
        """
        self._metadata_reader = metadata_reader
        self.signature_verifier = signature_verifier
        self.metadata_serializer = metadata_serializer

    @property
    def metadata_reader(self) -> MetadataReader:
        """Gets the current metadata reader.

        Returns:
            MetadataReader: The active metadata reader instance.
        """
        return self._metadata_reader

    @metadata_reader.setter
    def metadata_reader(self, reader: MetadataReader) -> None:
        """Sets a new metadata reader dynamically.

        Args:
            reader (MetadataReader): The new metadata reader to use.
        """
        self._metadata_reader = reader

    def read(self, read_request: ReadRequest) -> ReadResult:
        """Reads metadata and its signature from the audio file, verifies the
        signature, and deserializes the metadata.

        Args:
            read_request (ReadRequest): Path to the audio file.

        Returns:
            ReadResult: A result object indicating whether the read was
                successful, and if so, includes the deserialized metadata.
        """
        logger.debug("Reading metadata for file %s", read_request.filepath)
        audio_file_data_reading = self._read_metadata(read_request)

        if not self._is_audio_file_data_reading_successful(
            audio_file_data_reading
        ):
            return ReadResult(
                is_success=False,
                error="Metadata and/or signature are not present in the file.",
            )

        metadata = cast(str, audio_file_data_reading.metadata)
        signature = cast(str, audio_file_data_reading.signature)

        logger.debug(
            "Verifying signature is valid for file %s", read_request.filepath
        )
        if not self._is_signature_valid(metadata, signature):
            return ReadResult(
                is_success=False, error="Signature verification failed."
            )

        logger.debug(
            "Deserializing metadata for file %s", read_request.filepath
        )
        metadata_obj = self._deserialize_metadata(metadata)
        return ReadResult(is_success=True, metadata=metadata_obj)

    def _read_metadata(
        self, read_request: ReadRequest
    ) -> AudioFileDataReading:
        filepath = read_request.filepath
        audio_file_data_reading = self.metadata_reader.read(filepath)
        return audio_file_data_reading

    @staticmethod
    def _is_audio_file_data_reading_successful(
        audio_file_data_reading: AudioFileDataReading,
    ) -> bool:
        return audio_file_data_reading.is_success

    def _deserialize_metadata(self, metadata: str) -> Metadata:
        return self.metadata_serializer.deserialize(metadata)

    def _is_signature_valid(self, metadata: str, signature: str) -> bool:
        return self.signature_verifier.is_signature_valid(metadata, signature)
