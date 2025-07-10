# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

from pathlib import Path

import pytest

from transparentmeta.crypto.key_management import generate_key_pair
from transparentmeta.crypto.signature_verifier import SignatureVerifier
from transparentmeta.request.read_request import ReadRequest
from transparentmeta.request.write_request import WriteRequest
from transparentmeta.serialization.metadata_serializer import (
    MetadataSerializer,
)
from transparentmeta.use_case.read.mp3_metadata_reader import MP3MetadataReader
from transparentmeta.use_case.read.read_use_case import ReadUseCase
from transparentmeta.use_case.read.wav_metadata_reader import WAVMetadataReader
from transparentmeta.use_case.write.factory import build_write_use_case

private_key, public_key = generate_key_pair()


@pytest.fixture
def tmp_mp3_file_with_signed_metadata(temp_mp3, metadata) -> Path:
    write_use_case = build_write_use_case(private_key, "mp3")
    write_use_case.write(WriteRequest(filepath=temp_mp3, metadata=metadata))
    yield temp_mp3


@pytest.fixture
def read_request(tmp_mp3_file_with_signed_metadata):
    return ReadRequest(filepath=tmp_mp3_file_with_signed_metadata)


@pytest.fixture
def read_request_with_file_without_metadata(temp_mp3):
    return ReadRequest(filepath=temp_mp3)


@pytest.fixture
def read_use_case():
    verifier = SignatureVerifier(public_key)
    reader = MP3MetadataReader()
    serializer = MetadataSerializer()

    read_use_case = ReadUseCase(
        metadata_reader=reader,
        signature_verifier=verifier,
        metadata_serializer=serializer,
    )
    return read_use_case


def test_read_use_case_reads_metadata_correctly(
    read_request, read_use_case, metadata
):
    read_result = read_use_case.read(read_request)
    assert read_result.is_success
    assert read_result.metadata == metadata


def test_read_use_case_provides_error_result_for_file_without_metadata(
    read_request_with_file_without_metadata, read_use_case
):
    read_result = read_use_case.read(read_request_with_file_without_metadata)
    assert not read_result.is_success
    assert read_result.metadata is None
    assert (
        read_result.error
        == "Metadata and/or signature are not present in the file."
    )


def test_read_use_case_setter_switches_reader(read_use_case):
    read_use_case.metadata_reader = WAVMetadataReader()
    assert isinstance(read_use_case.metadata_reader, WAVMetadataReader)
