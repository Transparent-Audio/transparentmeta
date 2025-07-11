# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
This module provides a `SignatureVerifier` class that enables verifying
messages signed with the Ed25519 cryptographic algorithm. It supports
different character encodings for message conversion before verification.
"""

import logging

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import ed25519

from transparentmeta.crypto.character_encoding import CharacterEncoding
from transparentmeta.utils.encoding_utils import (
    encode_hexadecimal_string_to_bytes,
    encode_string_to_bytes,
)
from transparentmeta.utils.exceptions import InvalidHexadecimalStringError

logger = logging.getLogger(__name__)


class SignatureVerifier:
    """A utility class for verifying Ed25519 digital signatures.

    Attributes:
        public_key (ed25519.Ed25519PublicKey): The public key used for
            verifying signatures.
        character_encoding (CharacterEncoding): The encoding used for
            converting strings to bytes before verification.
    """

    def __init__(
        self,
        public_key: ed25519.Ed25519PublicKey,
        character_encoding: CharacterEncoding = CharacterEncoding.UTF8,
    ) -> None:
        """Initializes the verifier with a public key and a character encoding.

        Args:
            public_key (ed25519.Ed25519PublicKey): The public key for
                verifying signatures.
            character_encoding (CharacterEncoding): The encoding used for
                converting strings to bytes before verification.
        """
        self.public_key = public_key
        self.character_encoding = character_encoding

    def is_signature_valid(self, message: str, signature: str) -> bool:
        """Verifies an Ed25519 hex-encoded signature for a given message.

        Args:
            message (str): The original message that was signed.
            signature (str): The hex-encoded digital signature.

        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        try:
            message_bytes = self._encode_message(message)
            signature_bytes = self._encode_signature(signature)
            self._verify_signature(signature_bytes, message_bytes)

            logger.debug(
                "Signature '%s' for message '%s' is valid",
                signature,
                message,
            )

            return True

        except (InvalidSignature, InvalidHexadecimalStringError):

            logger.debug(
                "Signature '%s' for message '%s' is invalid",
                signature,
                message,
            )

            return False

    def _encode_message(self, message: str) -> bytes:
        return encode_string_to_bytes(message, self.character_encoding.value)

    def _encode_signature(self, signature: str) -> bytes:
        return encode_hexadecimal_string_to_bytes(signature)

    def _verify_signature(self, signature: bytes, message: bytes) -> None:
        self.public_key.verify(signature, message)
