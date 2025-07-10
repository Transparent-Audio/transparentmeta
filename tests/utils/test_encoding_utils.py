# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

import pytest

from transparentmeta.utils.encoding_utils import (
    decode_bytes_to_hexadecimal_string,
    encode_hexadecimal_string_to_bytes,
    encode_string_to_bytes,
)
from transparentmeta.utils.exceptions import InvalidHexadecimalStringError


def test_encode_hexadecimal_string_to_bytes_valid():
    hex_string = "68656c6c6f"  # "hello"
    expected = b"hello"
    result = encode_hexadecimal_string_to_bytes(hex_string)
    assert result == expected


def test_encode_hexadecimal_string_raises_error_with_non_hex_input():
    with pytest.raises(InvalidHexadecimalStringError):
        encode_hexadecimal_string_to_bytes("invalid!!hex")


@pytest.mark.parametrize(
    "input_bytes, encoding, expected_hex_string",
    [
        (b"hello", "utf-8", "68656c6c6f"),
        (b"\x00\xff", "utf-8", "00ff"),
    ],
)
def test_decode_bytes_to_hexadecimal_string_valid(
    input_bytes, encoding, expected_hex_string
):
    result = decode_bytes_to_hexadecimal_string(input_bytes, encoding)
    assert result == expected_hex_string


def test_decode_bytes_to_hexadecimal_string_invalid_encoding():
    with pytest.raises(LookupError):
        decode_bytes_to_hexadecimal_string(b"hello", "invalid-encoding")


@pytest.mark.parametrize(
    "input_str, encoding, expected",
    [
        ("hello", "utf-8", b"hello"),
        ("café", "utf-8", b"caf\xc3\xa9"),
        ("café", "latin-1", b"caf\xe9"),
    ],
)
def test_encode_string_to_bytes_valid(input_str, encoding, expected):
    assert encode_string_to_bytes(input_str, encoding) == expected


def test_encode_string_to_bytes_invalid_encoding():
    with pytest.raises(LookupError):
        encode_string_to_bytes("hello", "invalid-encoding")
