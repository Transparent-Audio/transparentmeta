# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
This module provides factory functions for creating instances of concrete
MetadataReader classes and ReadUseCase.
"""

import logging
from typing import Callable, Dict

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from transparentmeta.crypto.signature_verifier import SignatureVerifier
from transparentmeta.serialization.metadata_serializer import (
    MetadataSerializer,
)
from transparentmeta.use_case.constants import (
    SIGNATURE_FIELD,
    SUPPORTED_AUDIO_FORMATS,
    TRANSPARENCY_METADATA_FIELD,
)
from transparentmeta.use_case.exceptions import UnsupportedAudioFormatError
from transparentmeta.use_case.read.metadata_reader import MetadataReader
from transparentmeta.use_case.read.mp3_metadata_reader import MP3MetadataReader
from transparentmeta.use_case.read.read_use_case import ReadUseCase
from transparentmeta.use_case.read.wav_metadata_reader import WAVMetadataReader

logger = logging.getLogger(__name__)


metadata_reader_constructors_map: Dict[
    str, Callable[[str, str], MetadataReader]
] = {
    "mp3": MP3MetadataReader,
    "wav": WAVMetadataReader,
    "wave": WAVMetadataReader,
}


def build_metadata_reader(
    audio_format: str,
    transparency_metadata_field: str = TRANSPARENCY_METADATA_FIELD,
    signature_field: str = SIGNATURE_FIELD,
) -> MetadataReader:
    """Creates an instance of the appropriate concrete MetadataReader based on
    audio format.

    Args:
        audio_format (str): The audio format, either "mp3" or "wav".
        transparency_metadata_field (str): ID3 TXXX field for storing metadata.
        signature_field (str): ID3 TXXX field for storing the metadata
            signature.

    Returns:
        metadata_reader (MetadataReader): An instance of MP3MetadataReader or
            WAVMetadataReader.

    Raises:
        UnsupportedAudioFormatError: If the audio format is unsupported.
    """
    logger.debug("Building ReadUseCase instance for format: %s", audio_format)

    lowered_audio_format = audio_format.lower()
    metadata_reader_constructor = metadata_reader_constructors_map.get(
        lowered_audio_format
    )
    if metadata_reader_constructor is None:
        raise UnsupportedAudioFormatError(
            audio_format, SUPPORTED_AUDIO_FORMATS
        )

    metadata_reader = metadata_reader_constructor(
        transparency_metadata_field, signature_field
    )
    logger.debug("%s instance created", metadata_reader.__class__.__name__)

    return metadata_reader


def build_read_use_case(
    public_key: Ed25519PublicKey,
    audio_format: str,
    transparency_metadata_field: str = TRANSPARENCY_METADATA_FIELD,
    signature_field: str = SIGNATURE_FIELD,
) -> ReadUseCase:
    """Creates an instance of ReadUseCase by resolving all dependencies.

    Args:
        public_key (Ed25519PublicKey): The public key used for signature
            verification.
        audio_format (str): The audio format, either "mp3" or "wav".
        transparency_metadata_field (str): ID3 TXXX field for storing metadata.
            Defaults to "transparency".
        signature_field (str): ID3 TXXX field for storing the metadata
            signature. Defaults to "signature".

    Returns:
        read_use_case (ReadUseCase): An instance of ReadUseCase configured
            for the specified audio format.

    Raises:
        UnsupportedAudioFormatError: If the audio format is unsupported.
    """
    reader = build_metadata_reader(
        audio_format, transparency_metadata_field, signature_field
    )

    verifier = SignatureVerifier(public_key)
    logger.debug("SignatureVerifier instance created")

    serializer = MetadataSerializer()
    logger.debug("MetadataSerializer instance created")

    read_use_case = ReadUseCase(reader, verifier, serializer)
    logger.debug("ReadUseCase instance created")

    return read_use_case
