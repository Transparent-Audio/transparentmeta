# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""Utility functions for encoding and decoding strings and bytes."""

import binascii

from transparentmeta.utils.exceptions import InvalidHexadecimalStringError


def encode_hexadecimal_string_to_bytes(hex_string: str) -> bytes:
    """Encodes a hexadecimal string to bytes.

    Args:
        hex_string (str): The hexadecimal string to decode.

    Returns:
        bytes: The corresponding byte representation.

    Raises:
        InvalidHexadecimalStringError: If the input is not a valid hexadecimal
            string.
    """
    try:
        return binascii.unhexlify(hex_string)
    except binascii.Error as err:
        raise InvalidHexadecimalStringError(hex_string) from err


def decode_bytes_to_hexadecimal_string(
    byte_data: bytes, character_encoding: str
) -> str:
    """Decodes bytes to a hexadecimal string.

    Args:
        byte_data (bytes): The bytes to encode.
        character_encoding (str): The character encoding to use (e.g., "utf-8").

    Returns:
        str: The hexadecimal representation of the bytes encoded with the
            specified character encoding.
    """
    hex_bytes = binascii.hexlify(byte_data)
    return hex_bytes.decode(character_encoding)


def encode_string_to_bytes(string: str, character_encoding: str) -> bytes:
    """Encodes a string to bytes using the specified character encoding.

    Args:
        string (str): The string to encode.
        character_encoding (str): The character encoding to use (e.g., "utf-8").

    Returns:
        bytes: The byte representation of the string encoded with the specified
               character encoding.
    """
    return string.encode(character_encoding)
