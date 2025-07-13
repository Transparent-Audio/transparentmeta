# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
Example script: Read and verify metadata from an audio file using
transparentmeta.

This script demonstrates how to read transparency metadata embedded in an audio
file using the transparentmeta SDK. It also verifies the signature using the
public Ed25519 key that corresponds to the private key used for signing.

It:
1. Loads a public key from a PEM file.
2. Builds a TransparentMetadataReader instance with the relative factory
function.
3. Reads and verifies metadata from the specified audio file.
4. Prints the result, including any errors or the decoded metadata.

---

Try modifying:
- The `audio_path` to test with different files.
- The `public_key_path` to load alternate key versions.
"""

import logging
from pathlib import Path

from transparentmeta.crypto.key_management import load_public_key_from_pem_file
from transparentmeta.logger_config import configure_logging
from transparentmeta.sdk import build_transparent_metadata_reader

# Path to the MP3/WAV file you want to inspect
# ➤ Replace with your own test file path
audio_path = Path("/home/valerio/Music/sound3.WavE")

# Path to the public key PEM file used to verify the signature
public_key_path = Path("public_key.pem")


def main():
    # Set up logging for detailed trace output
    configure_logging(level=logging.DEBUG)

    # Load the Ed25519 public key from PEM file
    public_key = load_public_key_from_pem_file(public_key_path)

    # Build the TransparentMetadataReader instance
    transparent_metadata_reader = build_transparent_metadata_reader(public_key)

    # Read and verify metadata from the MP3 file
    read_result = transparent_metadata_reader.read(audio_path)

    # Print the result to the console
    print(read_result)


if __name__ == "__main__":
    main()
