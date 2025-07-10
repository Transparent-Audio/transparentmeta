# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

import pytest

from transparentmeta.request.exceptions import (
    InvalidAudioFileError,
    NoWritePermissionsError,
)
from transparentmeta.request.file_validators import (
    validate_audio_file_is_functioning,
    validate_audio_format_is_supported,
    validate_file_exists,
    validate_file_has_write_permissions,
)
from transparentmeta.use_case.exceptions import UnsupportedAudioFormatError


@pytest.fixture
def non_existent_file(tmp_path):
    """Returns a Path to a non-existent file."""
    return tmp_path / "non_existent.wav"


@pytest.fixture
def unsupported_file_format(tmp_path):
    """Creates a file with an unsupported format."""
    file = tmp_path / "test.txt"
    file.touch()
    return file


@pytest.fixture
def unwritable_file(temp_wav):
    temp_wav.chmod(0o400)  # Read-only permission
    return temp_wav


def test_validate_file_exists_is_valid(temp_wav):
    assert validate_file_exists(temp_wav) == temp_wav


def test_validate_file_exists_throws_file_not_found_when_file_not_exist(
    non_existent_file,
):
    with pytest.raises(FileNotFoundError, match="File not found"):
        validate_file_exists(non_existent_file)


def test_validate_audio_format_is_supported_passes_with_supported_format(
    temp_wav, temp_mp3
):
    assert validate_audio_format_is_supported(temp_wav) == temp_wav
    assert validate_audio_format_is_supported(temp_mp3) == temp_mp3


def test_validator_throws_unsupported_audio_format_with_unsupported_file(
    unsupported_file_format,
):
    with pytest.raises(
        UnsupportedAudioFormatError, match="Unsupported audio format"
    ):
        validate_audio_format_is_supported(unsupported_file_format)


def test_validate_audio_file_is_functioning(temp_wav, temp_mp3):
    assert validate_audio_file_is_functioning(temp_wav) == temp_wav
    assert validate_audio_file_is_functioning(temp_mp3) == temp_mp3


def test_validator_throughs_invalid_audio_file_error_if_mp3_not_functioning(
    temp_corrupt_mp3,
):
    with pytest.raises(InvalidAudioFileError, match="Invalid audio file"):
        validate_audio_file_is_functioning(temp_corrupt_mp3)


def test_validator_throughs_invalid_audio_file_error_if_wav_not_functioning(
    temp_corrupt_wav,
):
    with pytest.raises(InvalidAudioFileError, match="Invalid audio file"):
        validate_audio_file_is_functioning(temp_corrupt_wav)


def test_validate_file_has_write_permissions_valid(temp_wav):
    assert validate_file_has_write_permissions(temp_wav) == temp_wav


def test_validate_file_has_write_permissions_invalid(unwritable_file):
    with pytest.raises(NoWritePermissionsError):
        validate_file_has_write_permissions(unwritable_file)
