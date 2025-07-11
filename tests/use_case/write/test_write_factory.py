# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

import pytest
from cryptography.hazmat.primitives.asymmetric import ed25519

from transparentmeta.use_case.constants import (
    SIGNATURE_FIELD,
    TRANSPARENCY_METADATA_FIELD,
)
from transparentmeta.use_case.exceptions import UnsupportedAudioFormatError
from transparentmeta.use_case.write.factory import (
    build_metadata_writer,
    build_write_use_case,
)
from transparentmeta.use_case.write.mp3_metadata_writer import (
    MP3MetadataWriter,
)
from transparentmeta.use_case.write.wav_metadata_writer import (
    WAVMetadataWriter,
)
from transparentmeta.use_case.write.write_use_case import WriteUseCase


def test_build_metadata_writer_returns_mp3_writer():
    writer = build_metadata_writer("mp3")
    assert isinstance(writer, MP3MetadataWriter)
    assert writer.transparency_metadata_field == TRANSPARENCY_METADATA_FIELD
    assert writer.signature_field == SIGNATURE_FIELD


def test_build_metadata_writer_returns_wav_writer():
    writer = build_metadata_writer("wav")
    assert isinstance(writer, WAVMetadataWriter)
    assert writer.transparency_metadata_field == TRANSPARENCY_METADATA_FIELD
    assert writer.signature_field == SIGNATURE_FIELD


def test_build_metadata_writer_custom_id3_tag_fields():
    writer = build_metadata_writer("mp3", "meta", "sig")
    assert writer.transparency_metadata_field == "meta"
    assert writer.signature_field == "sig"


def test_build_metadata_writer_with_unsupported_audio_format_raises():
    with pytest.raises(
        UnsupportedAudioFormatError, match="Unsupported audio " "format"
    ):
        build_metadata_writer("flac")


def test_build_write_use_case_returns_write_use_case_with_correct_writer():
    private_key = ed25519.Ed25519PrivateKey.generate()
    use_case = build_write_use_case(private_key, "wav")

    assert isinstance(use_case, WriteUseCase)
    assert isinstance(use_case.metadata_writer, WAVMetadataWriter)
    assert (
        use_case.metadata_writer.transparency_metadata_field
        == TRANSPARENCY_METADATA_FIELD
    )
    assert use_case.metadata_writer.signature_field == SIGNATURE_FIELD


def test_build_write_use_case_with_custom_id3_tag_fields():
    private_key = ed25519.Ed25519PrivateKey.generate()
    use_case = build_write_use_case(
        private_key,
        audio_format="mp3",
        transparency_metadata_field="meta",
        signature_field="sig",
    )

    assert isinstance(use_case.metadata_writer, MP3MetadataWriter)
    assert use_case.metadata_writer.transparency_metadata_field == "meta"
    assert use_case.metadata_writer.signature_field == "sig"
