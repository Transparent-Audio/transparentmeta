# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from mutagen.mp3 import MP3

from transparentmeta.sdk.transparent_metadata_writer import (
    TransparentMetadataWriter,
)
from transparentmeta.use_case.write.factory import build_write_use_case
from transparentmeta.use_case.write.writer_selector import WriterSelector


@pytest.fixture
def transparent_metadata_writer():
    private_key = Ed25519PrivateKey.generate()
    writer_selector = WriterSelector()
    write_use_case = build_write_use_case(private_key, "mp3")

    writer = TransparentMetadataWriter(
        write_use_case=write_use_case, writer_selector=writer_selector
    )
    return writer


def test_transparent_metadata_writer_writes_metadata_to_mp3(
    temp_mp3, metadata_dict, transparent_metadata_writer
):
    # Write metadata to the file
    transparent_metadata_writer.write(
        filepath=temp_mp3, metadata=metadata_dict
    )

    # Read back the metadata
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


def test_transparent_metadata_writer_logs_correctly(
    temp_mp3, metadata_dict, caplog, transparent_metadata_writer
):

    with caplog.at_level("INFO"):
        transparent_metadata_writer.write(
            filepath=temp_mp3, metadata=metadata_dict
        )

    assert f"Starting metadata write for file: {temp_mp3}" in caplog.text
    assert (
        f"Successfully wrote metadata with signature to file: {temp_mp3}"
        in caplog.text
    )


def test_log_output_string(
    temp_mp3, metadata_dict, caplog, transparent_metadata_writer
):
    with caplog.at_level("INFO"):
        transparent_metadata_writer.write(
            filepath=temp_mp3, metadata=metadata_dict
        )

    assert len(caplog.records) >= 1
    record = caplog.records[0]

    assert record.levelname == "INFO"
    assert "transparentmeta.sdk.transparent_metadata_writer" in record.name
    assert "Starting metadata" in record.getMessage()
