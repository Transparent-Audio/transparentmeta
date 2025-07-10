# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

from pathlib import Path

from transparentmeta.request.exceptions import (
    InvalidAudioFileError,
    NoWritePermissionsError,
)


def test_invalid_audio_file_error():
    dummy_path = Path("/fake/path/audio.mp3")
    error_message = "Decoding failed"

    error = InvalidAudioFileError(dummy_path, error_message)

    assert isinstance(error, InvalidAudioFileError)
    assert error.filepath == dummy_path
    assert error.error_message == error_message
    assert "Invalid audio file" in str(error)
    assert str(dummy_path) in str(error)
    assert error_message in str(error)


def test_no_write_permissions_error():
    dummy_path = Path("/fake/path/audio.mp3")

    error = NoWritePermissionsError(dummy_path)

    assert isinstance(error, NoWritePermissionsError)
    assert error.filepath == dummy_path
    assert "File is not writable" in str(error)
    assert str(dummy_path) in str(error)
