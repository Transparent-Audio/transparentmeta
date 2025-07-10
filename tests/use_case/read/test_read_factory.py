# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

import pytest
from cryptography.hazmat.primitives.asymmetric import ed25519

from transparentmeta.use_case.constants import (
    SIGNATURE_FIELD,
    TRANSPARENCY_METADATA_FIELD,
)
from transparentmeta.use_case.exceptions import UnsupportedAudioFormatError
from transparentmeta.use_case.read.factory import (
    build_metadata_reader,
    build_read_use_case,
)
from transparentmeta.use_case.read.mp3_metadata_reader import MP3MetadataReader
from transparentmeta.use_case.read.read_use_case import ReadUseCase
from transparentmeta.use_case.read.wav_metadata_reader import WAVMetadataReader


def test_build_metadata_reader_returns_mp3_reader():
    reader = build_metadata_reader("mp3")
    assert isinstance(reader, MP3MetadataReader)
    assert reader.transparency_metadata_field == TRANSPARENCY_METADATA_FIELD
    assert reader.signature_field == SIGNATURE_FIELD


def test_build_metadata_reader_returns_wav_reader():
    reader = build_metadata_reader("wav")
    assert isinstance(reader, WAVMetadataReader)
    assert reader.transparency_metadata_field == TRANSPARENCY_METADATA_FIELD
    assert reader.signature_field == SIGNATURE_FIELD


def test_build_metadata_reader_with_custom_id3_tag_fields():
    reader = build_metadata_reader("mp3", "meta_custom", "sig_custom")
    assert isinstance(reader, MP3MetadataReader)
    assert reader.transparency_metadata_field == "meta_custom"
    assert reader.signature_field == "sig_custom"


def test_build_metadata_reader_invalid_format_raises():
    with pytest.raises(
        UnsupportedAudioFormatError, match="Unsupported audio " "format"
    ):
        build_metadata_reader("flac")


def test_build_read_use_case_returns_read_use_case_with_mp3_reader():
    public_key = ed25519.Ed25519PrivateKey.generate().public_key()
    use_case = build_read_use_case(public_key, "mp3")
    assert isinstance(use_case, ReadUseCase)
    assert isinstance(use_case.metadata_reader, MP3MetadataReader)


def test_build_read_use_case_returns_read_use_case_with_wav_reader():
    public_key = ed25519.Ed25519PrivateKey.generate().public_key()
    use_case = build_read_use_case(public_key, "wav")
    assert isinstance(use_case, ReadUseCase)
    assert isinstance(use_case.metadata_reader, WAVMetadataReader)


def test_build_read_use_case_with_custom_fields():
    public_key = ed25519.Ed25519PrivateKey.generate().public_key()
    use_case = build_read_use_case(
        public_key,
        audio_format="mp3",
        transparency_metadata_field="custom_meta",
        signature_field="custom_sig",
    )

    reader = use_case.metadata_reader
    assert isinstance(reader, MP3MetadataReader)
    assert reader.transparency_metadata_field == "custom_meta"
    assert reader.signature_field == "custom_sig"
