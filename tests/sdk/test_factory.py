# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

from transparentmeta.sdk.factory import (
    build_transparent_metadata_reader,
    build_transparent_metadata_writer,
)
from transparentmeta.sdk.transparent_metadata_reader import (
    TransparentMetadataReader,
)
from transparentmeta.sdk.transparent_metadata_writer import (
    TransparentMetadataWriter,
)
from transparentmeta.use_case.read.read_use_case import ReadUseCase
from transparentmeta.use_case.read.reader_selector import ReaderSelector
from transparentmeta.use_case.write.write_use_case import WriteUseCase
from transparentmeta.use_case.write.writer_selector import WriterSelector


def test_build_transparent_metadata_writer(keys):
    private_key = keys["private_key"]
    writer = build_transparent_metadata_writer(private_key)

    assert isinstance(writer, TransparentMetadataWriter)
    assert isinstance(writer.write_use_case, WriteUseCase)
    assert isinstance(writer.writer_selector, WriterSelector)


def test_build_transparent_metadata_writer_logs_correctly(keys, caplog):
    private_key = keys["private_key"]
    writer = build_transparent_metadata_writer(private_key)

    with caplog.at_level("INFO"):
        assert isinstance(writer, TransparentMetadataWriter)

    assert (
        "Building TransparentMetadataWriter instance with provided private key"
        in caplog.text
    )
    assert "TransparentMetadataWriter instance created" in caplog.text


def test_build_transparent_metadata_reader(keys):
    public_key = keys["public_key"]
    reader = build_transparent_metadata_reader(public_key)

    assert isinstance(reader, TransparentMetadataReader)
    assert isinstance(reader.read_use_case, ReadUseCase)
    assert isinstance(reader.reader_selector, ReaderSelector)


def test_build_transparent_metadata_reader_logs_correctly(keys, caplog):
    public_key = keys["public_key"]
    reader = build_transparent_metadata_reader(public_key)

    with caplog.at_level("INFO"):
        assert isinstance(reader, TransparentMetadataReader)

    assert (
        "Building TransparentMetadataReader instance with provided public key"
        in caplog.text
    )
    assert "TransparentMetadataReader instance created" in caplog.text
