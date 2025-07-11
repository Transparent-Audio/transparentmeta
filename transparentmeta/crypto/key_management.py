# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
Ed25519 Key Management Module

This module provides functions for generating, storing, loading, and
converting Ed25519 cryptographic key pairs. These keys are used for digital
signatures and secure communications. User A can sign a message with their
private key, and User B can verify the signature using User A's public key.

Functions:
    generate_key_pair() -> tuple:
        Generates a new Ed25519 private and public key pair.

    save_private_key_to_pem_file(private_key, filepath) -> None:
        Saves a private key to a PEM file.

    save_public_key_to_pem_file(public_key, filepath) -> None:
        Saves a public key to a PEM file.

    load_private_key_from_pem_file(filepath) -> ed25519.Ed25519PrivateKey:
        Loads a private key from a PEM file.

    load_public_key_from_pem_file(filepath) -> ed25519.Ed25519PublicKey:
        Loads a public key from a PEM file.

    convert_private_key_to_hex(private_key) -> str:
        Converts a private key to a hex string.

    convert_public_key_to_hex(public_key) -> str:
        Converts a public key to a hex string.

    load_private_key_from_hex_string(hex_string) -> ed25519.Ed25519PrivateKey:
        Converts a hex-encoded private key back to an Ed25519PrivateKey object.

    load_public_key_from_hex_string(hex_string) -> ed25519.Ed25519PublicKey:
        Converts a hex-encoded public key back to an Ed25519PublicKey object.
"""

import binascii
import logging
from pathlib import Path
from typing import Tuple, cast

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from transparentmeta.crypto.exceptions import NotEd25519KeyError

logger = logging.getLogger(__name__)


def generate_key_pair() -> (
    Tuple[ed25519.Ed25519PrivateKey, ed25519.Ed25519PublicKey]
):
    """Generates a new Ed25519 private and public key pair.

    Returns:
        tuple: A tuple containing an Ed25519PrivateKey and Ed25519PublicKey.
    """
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    logger.info("Generated new Ed25519 key pair")
    return private_key, public_key


def save_private_key_to_pem_file(
    private_key: ed25519.Ed25519PrivateKey, filepath: Path
) -> None:
    """Saves a private key to a PEM file.

    Args:
        private_key (ed25519.Ed25519PrivateKey): The private key to save.
        filepath (Path): The Path object where the private key should be saved.
    """
    pem_data = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    filepath.write_bytes(pem_data)
    logger.info("Saved private key to PEM file: %s", filepath)


def save_public_key_to_pem_file(
    public_key: ed25519.Ed25519PublicKey, filepath: Path
) -> None:
    """Saves a public key to a PEM file.

    Args:
        public_key (ed25519.Ed25519PublicKey): The public key to save.
        filepath (Path): The Path object where the public key should be saved.
    """
    pem_data = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    filepath.write_bytes(pem_data)
    logger.info("Saved public key to PEM file: %s", filepath)


def load_private_key_from_pem_file(
    filepath: Path,
) -> ed25519.Ed25519PrivateKey:
    """Loads a private key from a PEM file and ensures it is Ed25519.

    Args:
        filepath (Path): The Path object of the private key to load.

    Returns:
        ed25519.Ed25519PrivateKey: The loaded private key object.

    Raises:
        NotEd25519KeyError: If the loaded key is not an Ed25519 private key.
    """
    key = serialization.load_pem_private_key(
        filepath.read_bytes(), password=None
    )

    if not isinstance(key, ed25519.Ed25519PrivateKey):
        raise NotEd25519KeyError()

    logger.info("Loaded private key from PEM file: %s", filepath)

    return cast(ed25519.Ed25519PrivateKey, key)


def load_public_key_from_pem_file(filepath: Path) -> ed25519.Ed25519PublicKey:
    """Loads a public key from a PEM file and ensures it is Ed25519.

    Args:
        filepath (Path): The Path object of the public key to load.

    Returns:
        ed25519.Ed25519PublicKey: The loaded public key object.

    Raises:
        NotEd25519KeyError: If the loaded key is not an Ed25519 public key.
    """
    key = serialization.load_pem_public_key(filepath.read_bytes())

    if not isinstance(key, ed25519.Ed25519PublicKey):
        raise NotEd25519KeyError()

    logger.info("Loaded public key from PEM file: %s", filepath)

    return cast(ed25519.Ed25519PublicKey, key)


def convert_private_key_to_hex(private_key: ed25519.Ed25519PrivateKey) -> str:
    """Converts a private key to a hex-encoded string.

    Args:
        private_key (ed25519.Ed25519PrivateKey): The private key to convert.

    Returns:
        hexadecimal_encoded_private_key (str): The hex-encoded private key.
    """
    hexadecimal_encoded_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    ).hex()

    logger.info("Converted private key to hexadecimal string")

    return hexadecimal_encoded_private_key


def convert_public_key_to_hex(public_key: ed25519.Ed25519PublicKey) -> str:
    """Converts a public key to a hex-encoded string.

    Args:
        public_key (ed25519.Ed25519PublicKey): The public key to convert.

    Returns:
        hexadecimal_encoded_public_key (str): The hex-encoded public key.
    """
    hexadecimal_encoded_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()

    logger.info("Converted public key to hexadecimal string")

    return hexadecimal_encoded_public_key


def load_private_key_from_hex_string(
    hex_encoded_private_key: str,
) -> ed25519.Ed25519PrivateKey:
    """Converts a hex-encoded private key back to an Ed25519PrivateKey object.

    Args:
        hex_string (str): The hex-encoded private key.

    Returns:
        private_key (ed25519.Ed25519PrivateKey): The decoded private key
            object.
    """
    private_key_bytes = binascii.unhexlify(hex_encoded_private_key)
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(
        private_key_bytes
    )

    logger.info("Loaded private key from hexadecimal string")

    return private_key


def load_public_key_from_hex_string(
    hex_encoded_public_key: str,
) -> ed25519.Ed25519PublicKey:
    """Converts a hex-encoded public key back to an Ed25519PublicKey object.

    Args:
        hex_encoded_public_key (str): The hex-encoded public key.

    Returns:
        public_key (ed25519.Ed25519PublicKey): The decoded public key object.
    """
    public_bytes = binascii.unhexlify(hex_encoded_public_key)
    public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_bytes)

    logger.info("Loaded public key from hexadecimal string")

    return public_key
