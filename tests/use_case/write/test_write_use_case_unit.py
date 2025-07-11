# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

import pytest

from transparentmeta.crypto.signer import Signer
from transparentmeta.request.write_request import WriteRequest
from transparentmeta.serialization.metadata_serializer import (
    MetadataSerializer,
)
from transparentmeta.use_case.write.metadata_writer import MetadataWriter
from transparentmeta.use_case.write.write_use_case import WriteUseCase


@pytest.fixture
def mock_serializer(mocker):
    serializer = mocker.Mock(spec=MetadataSerializer)
    serializer.serialize.return_value = "serialized_metadata"
    return serializer


@pytest.fixture
def mock_signer(mocker):
    signer = mocker.Mock(spec=Signer)
    signer.sign.return_value = "digital_signature"
    return signer


@pytest.fixture
def mock_writer(mocker):
    return mocker.Mock(spec=MetadataWriter)


@pytest.fixture
def mock_write_request(mocker):
    request = mocker.Mock(spec=WriteRequest)
    request.filepath = "dummy"
    request.metadata = "dummy_metadata"
    return request


@pytest.fixture
def write_use_case(mock_serializer, mock_signer, mock_writer):
    return WriteUseCase(mock_serializer, mock_signer, mock_writer)


def test_write_calls_serializer_signer_and_writer_correctly(
    write_use_case,
    mock_serializer,
    mock_signer,
    mock_writer,
    mock_write_request,
):
    write_use_case.write(mock_write_request)

    mock_serializer.serialize.assert_called_once_with(
        mock_write_request.metadata
    )
    mock_signer.sign.assert_called_once_with("serialized_metadata")
    mock_writer.write.assert_called_once_with(
        mock_write_request.filepath,
        "serialized_metadata",
        "digital_signature",
    )


def test_write_use_case_writer_getter_works(write_use_case, mocker):
    assert isinstance(write_use_case.metadata_writer, MetadataWriter)


def test_write_use_case_writer_setter_works(write_use_case, mocker):
    new_writer = mocker.Mock(spec=MetadataWriter)
    write_use_case.metadata_writer = new_writer
    assert write_use_case.metadata_writer == new_writer
