# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
This module provides a `Signer` class that enables signing messages using
the Ed25519 cryptographic algorithm. It supports different character
encodings for message conversion before signing.
"""

import logging

from cryptography.hazmat.primitives.asymmetric import ed25519

from transparentmeta.crypto.character_encoding import CharacterEncoding
from transparentmeta.utils.encoding_utils import (
    decode_bytes_to_hexadecimal_string,
    encode_string_to_bytes,
)

logger = logging.getLogger(__name__)


class Signer:
    """A utility class for digitally signing messages using the Ed25519
    cryptographic algorithm.

    Attributes:
        private_key (ed25519.Ed25519PrivateKey): The private key used for
            signing messages.
        character_encoding (CharacterEncoding): The encoding used for
            converting strings to bytes before signing.
    """

    def __init__(
        self,
        private_key: ed25519.Ed25519PrivateKey,
        character_encoding: CharacterEncoding = CharacterEncoding.UTF8,
    ) -> None:
        """Initializes the signer with a private key and a character encoding.

        Args:
            private_key (ed25519.Ed25519PrivateKey): The private key for
                signing messages.
            character_encoding (CharacterEncoding): The encoding used for
                converting strings to bytes before signing.
        """
        self.private_key = private_key
        self.character_encoding = character_encoding

    def sign(self, message: str) -> str:
        """Signs a message using Ed25519 and returns a hex-encoded signature.

        Args:
            message (str): The message to sign.

        Returns:
            str: Hex-encoded digital signature.
        """
        signature_bytes = self._sign(message)
        signature = self._decode_signature(signature_bytes)

        logger.debug(
            "Signed message '%.40s' with signature: '%s'",
            message,
            signature,
        )

        return signature

    def _sign(self, message: str) -> bytes:
        message_bytes = encode_string_to_bytes(
            message, self.character_encoding.value
        )
        signature_bytes = self.private_key.sign(message_bytes)
        return signature_bytes

    def _decode_signature(self, signature_bytes: bytes) -> str:
        return decode_bytes_to_hexadecimal_string(
            signature_bytes, self.character_encoding.value
        )
