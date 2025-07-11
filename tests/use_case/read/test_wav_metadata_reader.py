# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

from mutagen.id3 import TXXX
from mutagen.wave import WAVE

from transparentmeta.use_case.constants import (
    TRANSPARENCY_METADATA_FIELD,
)
from transparentmeta.use_case.read.wav_metadata_reader import WAVMetadataReader


def test_wav_metadata_reader_reads_successfully(temp_wav_file_with_metadata):
    reader = WAVMetadataReader()
    audio_file_data_reading = reader.read(temp_wav_file_with_metadata)
    assert audio_file_data_reading.is_success
    assert audio_file_data_reading.metadata == "some_metadata"
    assert audio_file_data_reading.signature == "some_signature"


def test_wav_metadata_reader_when_file_has_no_tags(temp_wav):
    reader = WAVMetadataReader()
    audio_file_data_reading = reader.read(temp_wav)
    assert not audio_file_data_reading.is_success
    assert audio_file_data_reading.metadata is None
    assert audio_file_data_reading.signature is None


def test_wav_metadata_reader_missing_fields(temp_wav):
    audio = WAVE(temp_wav)
    audio.add_tags()
    audio.tags.add(
        TXXX(
            encoding=3, desc=TRANSPARENCY_METADATA_FIELD, text="some_metadata"
        )
    )
    audio.save()

    reader = WAVMetadataReader()
    audio_file_data_reading = reader.read(temp_wav)
    assert not audio_file_data_reading.is_success
    assert audio_file_data_reading.metadata is None
    assert audio_file_data_reading.signature is None
