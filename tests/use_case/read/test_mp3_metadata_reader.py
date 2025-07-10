# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

from mutagen.id3 import ID3, TXXX
from mutagen.mp3 import MP3

from transparentmeta.use_case.constants import (
    SIGNATURE_FIELD,
)
from transparentmeta.use_case.read.mp3_metadata_reader import MP3MetadataReader


def test_mp3_metadata_reader_reads_successfully(temp_mp3_file_with_metadata):
    reader = MP3MetadataReader()
    audio_file_data_reading = reader.read(temp_mp3_file_with_metadata)
    assert audio_file_data_reading.is_success
    assert audio_file_data_reading.metadata == "some_metadata"
    assert audio_file_data_reading.signature == "some_signature"


def test_mp3_metadata_reader_when_file_has_no_tags(temp_mp3):
    reader = MP3MetadataReader()
    audio_file_data_reading = reader.read(temp_mp3)
    assert not audio_file_data_reading.is_success
    assert audio_file_data_reading.metadata is None
    assert audio_file_data_reading.signature is None


def test_mp3_metadata_reader_missing_fields(temp_mp3):
    audio = MP3(temp_mp3, ID3=ID3)
    audio.add_tags()
    audio.tags.add(
        TXXX(encoding=3, desc="some_other_field", text="some_metadata")
    )
    audio.tags.add(
        TXXX(encoding=3, desc=SIGNATURE_FIELD, text="some_signature")
    )
    audio.save()

    reader = MP3MetadataReader()
    audio_file_data_reading = reader.read(temp_mp3)
    assert not audio_file_data_reading.is_success
    assert audio_file_data_reading.metadata is None
    assert audio_file_data_reading.signature is None


def test_initiate_metadata_field():
    reader = MP3MetadataReader("transparency-field", "signature-field")
    assert reader._metadata_field == "TXXX:transparency-field"


def test_initiate_signature_field():
    reader = MP3MetadataReader("transparency-field", "signature-field")
    assert reader._signature_field == "TXXX:signature-field"
