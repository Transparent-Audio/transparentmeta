# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

from transparentmeta.use_case.exceptions import UnsupportedAudioFormatError

SUPPORTED_FORMATS = ["mp3", "wav", "wave"]


def test_unsupported_audio_format_error_with_path(tmp_path):
    dummy_file = tmp_path / "file.xyz"
    dummy_file.touch()

    error = UnsupportedAudioFormatError(dummy_file, SUPPORTED_FORMATS)

    assert isinstance(error, UnsupportedAudioFormatError)
    assert error.filepath == dummy_file
    assert error.audio_format == "xyz"
    assert "file.xyz" in str(error)
    assert "Supported formats are" in str(error)


def test_unsupported_audio_format_error_with_str_format():
    format_str = "ogg"
    error = UnsupportedAudioFormatError(format_str, SUPPORTED_FORMATS)

    assert isinstance(error, UnsupportedAudioFormatError)
    assert error.audio_format == "ogg"
    assert "ogg" in str(error)
    assert "Supported formats are" in str(error)
