# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

"""
Example script: Write metadata to an audio file using transparentmeta.

This script shows how to embed structured transparency metadata into an MP3
file using the TransparentMeta SDK. The metadata is cryptographically signed
using a private Ed25519 key.

It:
1. Loads an Ed25519 private key from a PEM file.
2. Builds a TransparentMetadataWriter instance.
3. Creates a metadata dictionary with usage details and attribution.
4. Writes the metadata and signature into the target MP3 file.

This metadata can later be read and verified using the corresponding public key
with the `read_metadata.py` example.

---

Try modifying:
- The `metadata` fields to experiment with your own data.
- The `audio_path` to test with different audio files.
- The `private_key_path` to point to other key versions.
"""

import logging
from datetime import datetime
from pathlib import Path

from transparentmeta.crypto.key_management import (
    load_private_key_from_pem_file,
)
from transparentmeta.entity.metadata import AIUsageLevel
from transparentmeta.logger_config import configure_logging
from transparentmeta.sdk import build_transparent_metadata_writer

# Output file to write metadata to
# ➤ Change this to the path of the MP3 you want to tag
audio_path = Path("/home/valerio/Music/22.mp3")

# Location of your private key file
# ➤ This key should match the public key used to verify metadata
private_key_path = Path("private_key.pem")


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
        "created_at": datetime.utcnow(),
        "ai_usage_level": AIUsageLevel.AI_ASSISTED,
        "content_id": "12345",
        "user_id": "user_67890",
        "private_key_id": "dummy_private_key_id",
        "additional_info": {
            "attribution": {"lyrics": "John Doe", "composer": "Jane Smith"}
        },
    }

    # Write the metadata to the file (with embedded signature)
    transparent_metadata_writer.write(audio_path, metadata)


if __name__ == "__main__":
    main()
