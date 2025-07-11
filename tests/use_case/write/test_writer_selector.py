# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

import pytest

from transparentmeta.use_case.write.mp3_metadata_writer import (
    MP3MetadataWriter,
)
from transparentmeta.use_case.write.wav_metadata_writer import (
    WAVMetadataWriter,
)
from transparentmeta.use_case.write.writer_selector import WriterSelector


@pytest.fixture
def writer_selector():
    return WriterSelector()


def test_get_writer_mp3(writer_selector):
    writer = writer_selector.get_writer("mp3")
    assert isinstance(writer, MP3MetadataWriter)


def test_get_writer_wav(writer_selector):
    writer = writer_selector.get_writer("wav")
    assert isinstance(writer, WAVMetadataWriter)


def test_get_writer_wave(writer_selector):
    writer = writer_selector.get_writer("wave")
    assert isinstance(writer, WAVMetadataWriter)


def test_get_writer_throws_key_error_with_unsupported_audio_format(
    writer_selector,
):
    with pytest.raises(KeyError):
        writer_selector.get_writer("dummy_format")
