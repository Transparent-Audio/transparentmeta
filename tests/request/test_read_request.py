# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

from pathlib import Path

import pytest

from transparentmeta.request.exceptions import (
    InvalidAudioFileError,
)
from transparentmeta.request.read_request import ReadRequest
from transparentmeta.use_case.exceptions import UnsupportedAudioFormatError


def test_that_valid_audio_file_is_accepted_byread_request(temp_mp3: Path):
    request = ReadRequest(filepath=temp_mp3)
    assert request.filepath == temp_mp3


def test_read_request_raises_file_not_found_if_file_does_not_exist(
    tmp_path: Path,
):
    non_existent_file = tmp_path / "missing.mp3"
    with pytest.raises(FileNotFoundError, match="File not found:"):
        ReadRequest(filepath=non_existent_file)


def test_read_request_raises_if_format_is_not_supported(tmp_path: Path):
    unsupported_file = tmp_path / "audio.txt"
    unsupported_file.write_text("not audio")
    with pytest.raises(
        UnsupportedAudioFormatError, match="Unsupported audio format"
    ):
        ReadRequest(filepath=unsupported_file)


def test_read_request_raises_if_not_a_functioning_audio_file(tmp_path: Path):
    fake_mp3 = tmp_path / "fake.mp3"
    fake_mp3.write_text("not real mp3 data")
    with pytest.raises(InvalidAudioFileError, match="Invalid audio file:"):
        ReadRequest(filepath=fake_mp3)
