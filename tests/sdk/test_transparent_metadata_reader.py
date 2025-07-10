# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

from pathlib import Path

import pytest

from transparentmeta.crypto.key_management import generate_key_pair
from transparentmeta.request.write_request import WriteRequest
from transparentmeta.result.result import ReadResult
from transparentmeta.sdk.transparent_metadata_reader import (
    TransparentMetadataReader,
)
from transparentmeta.use_case.read.factory import build_read_use_case
from transparentmeta.use_case.read.reader_selector import ReaderSelector
from transparentmeta.use_case.write.factory import build_write_use_case

private_key, public_key = generate_key_pair()


@pytest.fixture
def tmp_mp3_file_with_signed_metadata(temp_mp3, metadata) -> Path:
    write_use_case = build_write_use_case(private_key, "mp3")
    write_use_case.write(WriteRequest(filepath=temp_mp3, metadata=metadata))
    return temp_mp3


@pytest.fixture
def transparent_metadata_reader():
    reader_selector = ReaderSelector()
    read_use_case = build_read_use_case(public_key, "mp3")
    return TransparentMetadataReader(
        read_use_case=read_use_case, reader_selector=reader_selector
    )


def test_transparent_metadata_reader_reads_metadata_from_mp3_correctly(
    tmp_mp3_file_with_signed_metadata, metadata, transparent_metadata_reader
):
    read_result = transparent_metadata_reader.read(
        filepath=tmp_mp3_file_with_signed_metadata
    )

    assert read_result.metadata == metadata
    assert read_result.is_success
    assert read_result.error is None


def test_transparent_metadata_reader_logs_successful_read(
    tmp_mp3_file_with_signed_metadata, caplog, transparent_metadata_reader
):
    with caplog.at_level("INFO"):
        transparent_metadata_reader.read(
            filepath=tmp_mp3_file_with_signed_metadata
        )

    assert (
        f"Starting metadata read for file: {tmp_mp3_file_with_signed_metadata}"
        in caplog.text
    )
    assert (
        f"Successfully read metadata from file: {tmp_mp3_file_with_signed_metadata}"
        in caplog.text
    )


def test_transparent_metadata_reader_logs_failed_read(
    mocker, temp_mp3, caplog, transparent_metadata_reader
):
    mock_result = ReadResult(is_success=False, error="Dummy error")
    mocker.patch.object(
        transparent_metadata_reader.read_use_case,
        "read",
        return_value=mock_result,
    )

    with caplog.at_level("INFO"):
        result = transparent_metadata_reader.read(filepath=temp_mp3)

    assert not result.is_success
    assert f"Starting metadata read for file: {temp_mp3}" in caplog.text
    assert (
        f"Metadata read failed for file {temp_mp3}: Dummy error" in caplog.text
    )
