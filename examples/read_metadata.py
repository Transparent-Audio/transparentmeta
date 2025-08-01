# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
Example script: Read and verify metadata from an audio file using
TransparentMeta.

This script demonstrates how to read transparency metadata embedded in an audio
file using the TransparentMeta SDK. It also verifies the signature using the
public Ed25519 key that corresponds to the private key used for signing.

In this script, you'll learn how to:
1. Load a public key from a PEM file.
2. Build a TransparentMetadataReader instance with the relative factory
function.
3. Read and verify metadata from the specified audio file.
"""

import logging

from examples.config import public_key_path, test_audio_path
from transparentmeta.crypto.key_management import load_public_key_from_pem_file
from transparentmeta.logger_config import configure_logging
from transparentmeta.sdk import build_transparent_metadata_reader


def main():
    # Set up logging for detailed trace output
    configure_logging(level=logging.DEBUG)

    # Load the Ed25519 public key from PEM file
    public_key = load_public_key_from_pem_file(public_key_path)

    # Build the TransparentMetadataReader instance
    transparent_metadata_reader = build_transparent_metadata_reader(public_key)

    # Read and verify metadata from the MP3 file
    read_result = transparent_metadata_reader.read(test_audio_path)

    # Print the result to the console
    print(read_result)


if __name__ == "__main__":
    main()
