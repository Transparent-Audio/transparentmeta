# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

import pytest
from mutagen.mp3 import MP3
from mutagen.wave import WAVE

from transparentmeta.crypto.signer import Signer
from transparentmeta.request.write_request import WriteRequest
from transparentmeta.serialization.metadata_serializer import (
    MetadataSerializer,
)
from transparentmeta.use_case.write.mp3_metadata_writer import (
    MP3MetadataWriter,
)
from transparentmeta.use_case.write.wav_metadata_writer import (
    WAVMetadataWriter,
)
from transparentmeta.use_case.write.write_use_case import (
    WriteUseCase,
)


@pytest.fixture
def signer(keys):
    private_key = keys["private_key"]
    return Signer(private_key)


@pytest.fixture
def write_use_case_mp3(signer):
    return WriteUseCase(
        metadata_serializer=MetadataSerializer(),
        signer=signer,
        metadata_writer=MP3MetadataWriter(),
    )


@pytest.fixture
def write_use_case_wav(signer):
    return WriteUseCase(
        metadata_serializer=MetadataSerializer(),
        signer=signer,
        metadata_writer=WAVMetadataWriter(),
    )


@pytest.fixture
def write_request_mp3(temp_mp3, metadata):
    return WriteRequest(filepath=temp_mp3, metadata=metadata)


@pytest.fixture
def write_request_wav(temp_wav, metadata):
    return WriteRequest(filepath=temp_wav, metadata=metadata)


def test_end_to_end_mp3_write_use_case(
    write_use_case_mp3, temp_mp3, write_request_mp3
):
    write_use_case_mp3.write(write_request_mp3)

    # Read back metadata
    audio = MP3(temp_mp3)
    assert "TXXX:transparency" in audio.tags
    assert "TXXX:signature" in audio.tags
    assert (
        '{"company":"Transparent Audio"'
        in audio.tags["TXXX:transparency"].text[0]
    )
    assert isinstance(
        audio.tags["TXXX:signature"].text[0], str
    )  # Ensure signature is written


def test_end_to_end_wav_write_use_case(
    write_use_case_wav, temp_wav, write_request_wav
):
    write_use_case_wav.write(write_request_wav)

    # Read back metadata
    audio = WAVE(temp_wav)
    assert "TXXX:transparency" in audio.tags
    assert "TXXX:signature" in audio.tags
    assert (
        '{"company":"Transparent Audio"'
        in audio.tags["TXXX:transparency"].text[0]
    )
    assert isinstance(
        audio.tags["TXXX:signature"].text[0], str
    )  # Ensure signature is written
