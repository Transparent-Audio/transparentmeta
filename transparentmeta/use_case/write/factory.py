# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
This module provides factory functions for creating instances of concrete
MetadataWriter classes and WriteUseCase.
"""

import logging
from typing import Callable, Dict

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from transparentmeta.crypto.signer import Signer
from transparentmeta.serialization.metadata_serializer import (
    MetadataSerializer,
)
from transparentmeta.use_case.constants import (
    SIGNATURE_FIELD,
    SUPPORTED_AUDIO_FORMATS,
    TRANSPARENCY_METADATA_FIELD,
)
from transparentmeta.use_case.exceptions import UnsupportedAudioFormatError
from transparentmeta.use_case.write.metadata_writer import MetadataWriter
from transparentmeta.use_case.write.mp3_metadata_writer import (
    MP3MetadataWriter,
)
from transparentmeta.use_case.write.wav_metadata_writer import (
    WAVMetadataWriter,
)
from transparentmeta.use_case.write.write_use_case import WriteUseCase

logger = logging.getLogger(__name__)

metadata_writer_constructors_map: Dict[
    str, Callable[[str, str], MetadataWriter]
] = {
    "mp3": MP3MetadataWriter,
    "wav": WAVMetadataWriter,
    "wave": WAVMetadataWriter,
}


def build_metadata_writer(
    audio_format: str,
    transparency_metadata_field: str = TRANSPARENCY_METADATA_FIELD,
    signature_field: str = SIGNATURE_FIELD,
) -> MetadataWriter:
    """Creates an instance of the appropriate concrete MetadataWriter based on
    audio format.

    Args:
        audio_format (str): The audio format, either "mp3" or "wav".
        transparency_metadata_field (str): ID3 TXXX field for storing metadata.
        signature_field (str): ID3 TXXX field for storing the metadata
            signature.

    Returns:
        metadata_writer (MetadataWriter): An instance of MP3MetadataWriter or
            WAVMetadataWriter.

    Raises:
        UnsupportedAudioFormatError: If the audio format is unsupported.
    """
    logger.debug("Building WriteUseCase instance for format: %s", audio_format)

    lowered_audio_format = audio_format.lower()
    metadata_writer_constructor = metadata_writer_constructors_map.get(
        lowered_audio_format
    )
    if metadata_writer_constructor is None:
        raise UnsupportedAudioFormatError(
            audio_format, SUPPORTED_AUDIO_FORMATS
        )

    metadata_writer = metadata_writer_constructor(
        transparency_metadata_field, signature_field
    )
    logger.debug("%s instance created", metadata_writer.__class__.__name__)
    return metadata_writer


def build_write_use_case(
    private_key: Ed25519PrivateKey,
    audio_format: str,
    transparency_metadata_field: str = TRANSPARENCY_METADATA_FIELD,
    signature_field: str = SIGNATURE_FIELD,
) -> WriteUseCase:
    """Creates an instance of WriteUseCase resolving all dependencies.

    Args:
        private_key (Ed25519PrivateKey): The private key used for signing.
        audio_format (str): The audio format, either "mp3" or "wav".
        transparency_metadata_field (str): ID3 TXXX field for storing metadata.
        signature_field (str): ID3 TXXX field for storing the metadata
            signature.

    Returns:
        write_use_case (WriteUseCase): An instance of WriteUseCase configured
            for the specified audio format.

    Raises:
        UnsupportedAudioFormatError: If the audio format is unsupported.
    """
    writer = build_metadata_writer(
        audio_format,
        transparency_metadata_field=transparency_metadata_field,
        signature_field=signature_field,
    )

    serializer = MetadataSerializer()
    logger.debug("MetadataSerializer instance created")

    signer = Signer(private_key)
    logger.debug("Signer instance created")

    write_use_case = WriteUseCase(serializer, signer, writer)
    logger.debug("WriteUseCase instance created")

    return write_use_case
