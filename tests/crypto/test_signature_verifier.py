# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

import binascii

import pytest
from cryptography.hazmat.primitives.asymmetric import ed25519

from transparentmeta.crypto.character_encoding import CharacterEncoding
from transparentmeta.crypto.signature_verifier import SignatureVerifier
from transparentmeta.crypto.signer import Signer


@pytest.fixture
def signing():
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    signer = Signer(private_key, CharacterEncoding.UTF8)
    verifier = SignatureVerifier(public_key, CharacterEncoding.UTF8)
    return signer, verifier


def test_that_a_valid_signature_is_successfully_verified(signing):
    signer, verifier = signing

    message = "Test Message"
    signature = signer.sign(message)

    assert verifier.is_signature_valid(
        message, signature
    ), "Valid signature should pass"


def test_sinagure_verification_fails_if_message_tampered_with(signing):
    signer, verifier = signing

    original_message = "Original Message"
    tampered_message = "Tampered Message"
    signature = signer.sign(original_message)

    assert not verifier.is_signature_valid(
        tampered_message, signature
    ), "Tampered message should fail verification"


def test_sinagure_verification_fails_if_signature_tampered_with(signing):
    signer, verifier = signing

    message = "Test Message"
    signature = signer.sign(message)

    # Tamper with the signature (flip one character)
    tampered_signature = signature[:-1] + (
        "0" if signature[-1] != "0" else "1"
    )

    assert not verifier.is_signature_valid(
        message, tampered_signature
    ), "Tampered signature should fail verification"


def test_signature_verification_fails_passing_non_hexadecimal_signature(
    signing,
):
    signer, verifier = signing

    message = "Test Message"
    non_hexadecimal_signature = "not_a_hex_string"
    assert not verifier.is_signature_valid(message, non_hexadecimal_signature)


def test_signature_verification_with_empty_message_works(signing):
    signer, verifier = signing

    message = ""
    signature = signer.sign(message)

    assert verifier.is_signature_valid(
        message, signature
    ), "Empty message should verify correctly"
