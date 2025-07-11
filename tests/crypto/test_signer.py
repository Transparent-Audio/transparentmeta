# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

import binascii

import pytest
from cryptography.hazmat.primitives.asymmetric import ed25519

from transparentmeta.crypto.character_encoding import CharacterEncoding
from transparentmeta.crypto.signer import Signer


@pytest.fixture
def ed25519_key():
    return ed25519.Ed25519PrivateKey.generate()


@pytest.mark.parametrize(
    "encoding", [CharacterEncoding.UTF8, CharacterEncoding.ASCII]
)
def test_sign_message(ed25519_key, encoding):
    """
    Test signing a message with different character encodings.
    Ensures the output is a valid hex-encoded string.
    """
    signer = Signer(ed25519_key, encoding)
    message = "Hello, Ed25519!"
    signature = signer.sign(message)

    # Check that the output is a valid hex string
    assert isinstance(signature, str)
    assert all(
        c in "0123456789abcdef" for c in signature
    ), "Invalid hex format"
    assert len(signature) > 0, "Signature should not be empty"


def test_sign_empty_message(ed25519_key):
    """
    Test signing an empty message.
    Ensures signing an empty string does not cause errors.
    """
    signer = Signer(ed25519_key, CharacterEncoding.UTF8)
    signature = signer.sign("")

    assert isinstance(signature, str)
    assert all(
        c in "0123456789abcdef" for c in signature
    ), "Invalid hex format"
    assert len(signature) > 0, "Signature should not be empty"


def test_sign_different_messages_produces_different_signatures(ed25519_key):
    """
    Test signing different messages.
    Ensures different messages produce different signatures.
    """
    signer = Signer(ed25519_key, CharacterEncoding.UTF8)
    signature_1 = signer.sign("Message 1")
    signature_2 = signer.sign("Message 2")

    assert (
        signature_1 != signature_2
    ), "Different messages should have different signatures"


def test_signing_the_same_messages_produces_same_signature_result(ed25519_key):
    signer = Signer(ed25519_key, CharacterEncoding.UTF8)
    message = "Repeatable Test"

    signature_1 = signer.sign(message)
    signature_2 = signer.sign(message)

    assert (
        signature_1 == signature_2
    ), "Same message should produce the same signature"


def test_signature_length(ed25519_key):
    signer = Signer(ed25519_key, CharacterEncoding.UTF8)
    message = "Length Test"
    signature = signer.sign(message)

    # Ensure the hex-encoded signature has the expected length
    assert (
        len(signature) == ed25519_key.sign(b"test").hex().__len__()
    ), "Signature length should be consistent"
