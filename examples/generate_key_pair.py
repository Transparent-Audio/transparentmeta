# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

"""
Example script: Generate an Ed25519 key pair for transparentmeta.

This script demonstrates how to generate a public/private key pair used for
cryptographically signing and verifying metadata embedded in audio files (
e.g., MP3 or WAV) using the transparentmeta SDK.

It:
1. Generates a new Ed25519 private/public key pair.
2. Saves the private key to a PEM file.
3. Saves the public key to a PEM file.

Transparentmeta uses the private key to sign metadata before embedding it in an
audio file, and the public key to verify metadata authenticity when
reading from an audio file.

---

Try modifying the filenames or output directories if you'd like to manage
multiple key sets or integrate with versioning workflows.
"""

import logging
from pathlib import Path

from transparentmeta.crypto.key_management import (
    generate_key_pair,
    save_private_key_to_pem_file,
    save_public_key_to_pem_file,
)
from transparentmeta.logger_config import configure_logging

# Output file paths for storing the generated key pair
# ➤ You can change these to save keys elsewhere or under different names
private_key_path = Path("private_key.pem")
public_key_path = Path("public_key.pem")


def main():
    # Configure the transparentmeta logger for full debug visibility
    configure_logging(level=logging.DEBUG)

    # Generate a new Ed25519 key pair
    private_key, public_key = generate_key_pair()

    # Save the private key to a PEM file
    # Store this securely — it's used for signing metadata
    save_private_key_to_pem_file(private_key, private_key_path)

    # Save the public key to a PEM file
    # Share this freely — it's used for verifying signatures
    save_public_key_to_pem_file(public_key, public_key_path)


if __name__ == "__main__":
    main()
