# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
Example script: Write metadata to an audio file using TransparentMeta.

This script shows how to embed structured transparency metadata into a test
audio file using the TransparentMeta SDK. The metadata is cryptographically
signed using a private Ed25519 key.

In this script, you'll learn how to:
1. Load an Ed25519 private key from a PEM file.
2. Build a TransparentMetadataWriter instance.
3. Create a metadata dictionary with usage details and attribution.
4. Write the metadata and signature into the target MP3 file.

This metadata can later be read and verified using the corresponding public
key. You can learn how to do that from the `read_metadata.py` example.
"""

import logging
from datetime import datetime, timezone

from examples.config import private_key_path, test_audio_path
from transparentmeta.crypto.key_management import (
    load_private_key_from_pem_file,
)
from transparentmeta.entity.metadata import AIUsageLevel
from transparentmeta.logger_config import configure_logging
from transparentmeta.sdk import build_transparent_metadata_writer


def main():
    # Configure logging for full traceability
    configure_logging(level=logging.DEBUG)

    # Load your Ed25519 private key from PEM file
    private_key = load_private_key_from_pem_file(private_key_path)

    # Build the metadata writer with your signing key
    transparent_metadata_writer = build_transparent_metadata_writer(
        private_key
    )

    # Define the metadata to be embedded and signed
    # ➤ You can customize these fields for your own use case
    metadata = {
        "company": "Transparent Audio",
        "model": "v2.1",
        "created_at": datetime.now(timezone.utc),
        "ai_usage_level": AIUsageLevel.AI_ASSISTED,
        "content_id": "12345",
        "user_id": "user_67890",
        "private_key_id": "dummy_private_key_id",
        "additional_info": {
            "attribution": {
                "lyrics": "John Doe",
                "composer": "Jane Smith",
                "singer": "HAL 9000",
            }
        },
    }

    # Write the metadata to the file (with cryptographic signature)
    transparent_metadata_writer.write(test_audio_path, metadata)


if __name__ == "__main__":
    main()
