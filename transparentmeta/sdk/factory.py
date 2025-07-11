# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
This module provides factory functions for creating instances of
`TransparentMetadataWriter` and `TransparentMetadataReader` with a simple
function call.

Developers should use these functions as the primary interface for
instantiating these classes, which serve as the main entry points for
writing and reading digitally-signed metadata in audio files using
transparentmeta.
"""

import logging

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from transparentmeta.sdk.transparent_metadata_reader import (
    TransparentMetadataReader,
)
from transparentmeta.sdk.transparent_metadata_writer import (
    TransparentMetadataWriter,
)
from transparentmeta.use_case.read.factory import build_read_use_case
from transparentmeta.use_case.read.reader_selector import ReaderSelector
from transparentmeta.use_case.write.factory import build_write_use_case
from transparentmeta.use_case.write.writer_selector import WriterSelector

logger = logging.getLogger(__name__)


def build_transparent_metadata_writer(
    private_key: Ed25519PrivateKey,
) -> TransparentMetadataWriter:
    """Creates an instance of TransparentWriter with all dependencies resolved.

    Args:
        private_key (Ed25519PrivateKey): The private key used for signing.

    Returns:
        transparent_metadata_writer (TransparentMetadataWriter): An instance
            of TransparentWriter ready to be used for metadata writing
    """
    logger.info(
        "Building TransparentMetadataWriter instance with provided private key"
    )

    writer_selector = WriterSelector()
    logger.debug("WriterSelector instance created ")

    write_use_case = build_write_use_case(
        private_key,
        "mp3",
    )

    transparent_metadata_writer = TransparentMetadataWriter(
        write_use_case, writer_selector
    )
    logger.info("TransparentMetadataWriter instance created")

    return transparent_metadata_writer


def build_transparent_metadata_reader(
    public_key: Ed25519PublicKey,
) -> TransparentMetadataReader:
    """Creates an instance of TransparentReader with all dependencies resolved.

    Args:
        public_key (Ed25519PrivateKey): The public key used for signature
            verification.

    Returns:
        transparent_metadata_reader (TransparentMetadataReader): An instance
            of TransparentReader ready to be used for metadata reading
    """
    logger.info(
        "Building TransparentMetadataReader instance with provided "
        "public key"
    )

    reader_selector = ReaderSelector()
    logger.debug("ReaderSelector instance created")

    read_use_case = build_read_use_case(
        public_key,
        "mp3",
    )

    transparent_metadata_reader = TransparentMetadataReader(
        read_use_case, reader_selector
    )
    logger.info("TransparentMetadataReader instance created")

    return transparent_metadata_reader
