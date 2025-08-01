# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

from pathlib import Path

from transparentmeta.request.exceptions import (
    InvalidAudioFileError,
    NoWritePermissionsError,
    WAVTooLargeError,
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


def test_wav_too_large_error():
    dummy_path = Path("/fake/path/audio.wav")
    max_size = 10485760  # 10 MB
    file_size = 20971520  # 20 MB

    error = WAVTooLargeError(dummy_path, max_size, file_size)

    assert isinstance(error, WAVTooLargeError)
    assert error.filepath == dummy_path
    assert error.max_size == max_size
    assert error.file_size == file_size
    assert "exceeds the maximum size" in str(error)
    assert str(dummy_path) in str(error)
    assert f"maximum size of {max_size} bytes" in str(error)
    assert f"File size: {file_size} bytes" in str(error)
