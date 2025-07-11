# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

import binascii
import logging
import tempfile
from pathlib import Path

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, rsa

import transparentmeta.crypto.key_management as keys_manager
from transparentmeta.crypto.exceptions import NotEd25519KeyError


@pytest.fixture
def invalid_pem_file(tmp_path):
    invalid_key_path = tmp_path / "invalid_private.pem"
    invalid_key_path.write_text("not_a_valid_key")
    return invalid_key_path


def test_generate_key_pair():
    private_key, public_key = keys_manager.generate_key_pair()

    assert isinstance(private_key, ed25519.Ed25519PrivateKey)
    assert isinstance(public_key, ed25519.Ed25519PublicKey)


def test_save_private_key_to_pem_file():
    private_key, _ = keys_manager.generate_key_pair()

    with tempfile.TemporaryDirectory() as temp_dir:
        key_path = Path(temp_dir) / "private_key.pem"
        keys_manager.save_private_key_to_pem_file(private_key, key_path)

        assert key_path.exists()
        assert key_path.stat().st_size > 0  # Ensure file is not empty


def test_save_public_key_to_a_pem_file():
    _, public_key = keys_manager.generate_key_pair()

    with tempfile.TemporaryDirectory() as temp_dir:
        key_path = Path(temp_dir) / "public_key.pem"
        keys_manager.save_public_key_to_pem_file(public_key, key_path)

        assert key_path.exists()
        assert key_path.stat().st_size > 0  # Ensure file is not empty


def test_load_private_key_from_pem_file(tmp_path):
    private_key, _ = keys_manager.generate_key_pair()

    key_path = tmp_path / "private_key.pem"
    keys_manager.save_private_key_to_pem_file(private_key, key_path)

    loaded_private_key = keys_manager.load_private_key_from_pem_file(key_path)

    assert isinstance(loaded_private_key, ed25519.Ed25519PrivateKey)
    assert private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    ) == loaded_private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )


def test_load_invalid_private_key_raises_not_ed25519_error(tmp_path):
    rsa_key_path = tmp_path / "rsa_private.pem"
    rsa_private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048
    )
    pem_data = rsa_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    rsa_key_path.write_bytes(pem_data)

    with pytest.raises(NotEd25519KeyError):
        keys_manager.load_private_key_from_pem_file(rsa_key_path)


def test_load_public_key_from_pem_file(tmp_path):
    _, public_key = keys_manager.generate_key_pair()

    key_path = tmp_path / "public_key.pem"
    keys_manager.save_public_key_to_pem_file(public_key, key_path)

    loaded_public_key = keys_manager.load_public_key_from_pem_file(key_path)

    assert isinstance(loaded_public_key, ed25519.Ed25519PublicKey)
    assert public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ) == loaded_public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )


def test_load_invalid_public_key_raises_not_ed25519_error(tmp_path):
    rsa_key_path = tmp_path / "rsa_public.pem"

    # Generate RSA public key
    rsa_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    rsa_public_key = rsa_key.public_key()

    # Serialize to PEM
    pem_data = rsa_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    rsa_key_path.write_bytes(pem_data)

    # Expect failure when trying to load non-Ed25519 key
    with pytest.raises(NotEd25519KeyError):
        keys_manager.load_public_key_from_pem_file(rsa_key_path)


def test_convert_private_key_to_hex_string():
    private_key, _ = keys_manager.generate_key_pair()

    private_hex = keys_manager.convert_private_key_to_hex(private_key)

    assert isinstance(private_hex, str)
    assert len(private_hex) > 0
    assert all(
        c in "0123456789abcdef" for c in private_hex
    )  # Ensure valid hex characters


def test_convert_public_key_to_hex_string():
    _, public_key = keys_manager.generate_key_pair()

    public_hex = keys_manager.convert_public_key_to_hex(public_key)

    assert isinstance(public_hex, str)
    assert len(public_hex) > 0
    assert all(
        c in "0123456789abcdef" for c in public_hex
    )  # Ensure valid hex characters


def test_load_private_key_from_hex():
    private_key, _ = keys_manager.generate_key_pair()

    private_hex = keys_manager.convert_private_key_to_hex(private_key)
    loaded_private_key = keys_manager.load_private_key_from_hex_string(
        private_hex
    )

    assert isinstance(loaded_private_key, ed25519.Ed25519PrivateKey)
    assert private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    ) == loaded_private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )


def test_load_public_key_from_hex_string():
    _, public_key = keys_manager.generate_key_pair()

    public_hex = keys_manager.convert_public_key_to_hex(public_key)
    loaded_public_key = keys_manager.load_public_key_from_hex_string(
        public_hex
    )

    assert isinstance(loaded_public_key, ed25519.Ed25519PublicKey)
    assert public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ) == loaded_public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )


def test_load_private_key_from_hex_raises_error_with_invalid_hex_string():
    with pytest.raises(binascii.Error):
        keys_manager.load_private_key_from_hex_string("invalidhex")


def test_load_public_key_from_hex_raises_error_with_invalid_hex_string():
    with pytest.raises(binascii.Error):
        keys_manager.load_public_key_from_hex_string("invalidhex")


def test_load_private_key_from_pem_raises_error_if_invalid_pem_file(
    invalid_pem_file,
):
    with pytest.raises(ValueError):
        keys_manager.load_private_key_from_pem_file(invalid_pem_file)


def test_load_public_key_from_pem_raises_error_if_invalid_pem_file(
    invalid_pem_file,
):
    with pytest.raises(ValueError):
        keys_manager.load_public_key_from_pem_file(invalid_pem_file)


def test_generate_key_pair_logs_info(caplog):
    with caplog.at_level(logging.INFO):
        _, _ = keys_manager.generate_key_pair()

    assert any(record.levelname == "INFO" for record in caplog.records)


def test_save_private_key_to_pem_file_logs_info(caplog):
    private_key, _ = keys_manager.generate_key_pair()
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "private.pem"
        with caplog.at_level(logging.INFO):
            keys_manager.save_private_key_to_pem_file(private_key, path)

    assert any(record.levelname == "INFO" for record in caplog.records)


def test_save_public_key_to_pem_file_logs_info(caplog):
    _, public_key = keys_manager.generate_key_pair()
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "public.pem"
        with caplog.at_level(logging.INFO):
            keys_manager.save_public_key_to_pem_file(public_key, path)

    assert any(record.levelname == "INFO" for record in caplog.records)


def test_load_private_key_from_pem_file_logs_info(tmp_path, caplog):
    private_key, _ = keys_manager.generate_key_pair()
    path = tmp_path / "key.pem"
    keys_manager.save_private_key_to_pem_file(private_key, path)

    with caplog.at_level(logging.INFO):
        _ = keys_manager.load_private_key_from_pem_file(path)

    assert any(record.levelname == "INFO" for record in caplog.records)


def test_load_public_key_from_pem_file_logs_info(tmp_path, caplog):
    _, public_key = keys_manager.generate_key_pair()
    path = tmp_path / "key.pem"
    keys_manager.save_public_key_to_pem_file(public_key, path)

    with caplog.at_level(logging.INFO):
        _ = keys_manager.load_public_key_from_pem_file(path)

    assert any(record.levelname == "INFO" for record in caplog.records)


def test_convert_private_key_to_hex_logs_info(caplog):
    private_key, _ = keys_manager.generate_key_pair()
    with caplog.at_level(logging.INFO):
        _ = keys_manager.convert_private_key_to_hex(private_key)

    assert any(record.levelname == "INFO" for record in caplog.records)


def test_convert_public_key_to_hex_logs_info(caplog):
    _, public_key = keys_manager.generate_key_pair()
    with caplog.at_level(logging.INFO):
        _ = keys_manager.convert_public_key_to_hex(public_key)

    assert any(record.levelname == "INFO" for record in caplog.records)


def test_load_private_key_from_hex_logs_info(caplog):
    private_key, _ = keys_manager.generate_key_pair()
    hex_str = keys_manager.convert_private_key_to_hex(private_key)

    with caplog.at_level(logging.INFO):
        _ = keys_manager.load_private_key_from_hex_string(hex_str)

    assert any(record.levelname == "INFO" for record in caplog.records)


def test_load_public_key_from_hex_logs_info(caplog):
    _, public_key = keys_manager.generate_key_pair()
    hex_str = keys_manager.convert_public_key_to_hex(public_key)

    with caplog.at_level(logging.INFO):
        _ = keys_manager.load_public_key_from_hex_string(hex_str)

    assert any(record.levelname == "INFO" for record in caplog.records)
