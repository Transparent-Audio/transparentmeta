# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

import pytest

from transparentmeta.use_case.read.mp3_metadata_reader import (
    MP3MetadataReader,
)
from transparentmeta.use_case.read.reader_selector import ReaderSelector
from transparentmeta.use_case.read.wav_metadata_reader import (
    WAVMetadataReader,
)


@pytest.fixture
def reader_selector():
    return ReaderSelector()


def test_get_reader_mp3(reader_selector):
    reader = reader_selector.get_reader("mp3")
    assert isinstance(reader, MP3MetadataReader)


def test_get_reader_wav(reader_selector):
    reader = reader_selector.get_reader("wav")
    assert isinstance(reader, WAVMetadataReader)


def test_get_reader_wave(reader_selector):
    reader = reader_selector.get_reader("wave")
    assert isinstance(reader, WAVMetadataReader)
