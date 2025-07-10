# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

from transparentmeta.utils.exceptions import InvalidHexadecimalStringError


def test_invalid_hexadecimal_string_error():
    invalid_hex_string = "xyz123!"
    error = InvalidHexadecimalStringError(invalid_hex_string)
    assert isinstance(error, InvalidHexadecimalStringError)
    assert (
        str(error)
        == f"String {invalid_hex_string} is not a valid hexadecimal string"
    )
