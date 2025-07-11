# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

from pathlib import Path

import pytest

from transparentmeta.use_case.read.metadata_reader import AudioFileDataReading
from transparentmeta.use_case.read.read_use_case import ReadUseCase


@pytest.fixture
def use_case(mocker):
    mock_metadata_reader = mocker.Mock()
    mock_signature_verifier = mocker.Mock()
    mock_metadata_serializer = mocker.Mock()
    return ReadUseCase(
        metadata_reader=mock_metadata_reader,
        signature_verifier=mock_signature_verifier,
        metadata_serializer=mock_metadata_serializer,
    )


def test_successful_read_use_case(mocker, use_case):
    # Setup
    fake_metadata = '{"foo": "bar"}'
    fake_signature = "valid_signature"
    fake_metadata_obj = {"foo": "bar"}
    filepath = Path("fake_audio.mp3")

    mock_metadata_reader = use_case.metadata_reader
    mock_signature_verifier = use_case.signature_verifier
    mock_metadata_serializer = use_case.metadata_serializer

    mock_read_request = mocker.Mock()
    mock_read_request.filepath = filepath

    mock_metadata_reader.read.return_value = AudioFileDataReading(
        is_success=True, metadata=fake_metadata, signature=fake_signature
    )
    mock_signature_verifier.is_signature_valid.return_value = True
    mock_metadata_serializer.deserialize.return_value = fake_metadata_obj

    # Act
    result = use_case.read(mock_read_request)

    # Assert
    assert result.is_success
    assert result.error is None
    assert result.metadata == fake_metadata_obj


def test_read_use_case_fails_due_to_missing_metadata_or_signature(
    mocker, use_case
):
    filepath = Path("missing.mp3")
    mock_read_request = mocker.Mock()
    mock_read_request.filepath = filepath

    mock_metadata_reader = use_case.metadata_reader
    mock_metadata_reader.read.return_value = AudioFileDataReading(
        is_success=False,
    )

    result = use_case.read(mock_read_request)

    assert not result.is_success
    assert (
        result.error
        == "Metadata and/or signature are not present in the file."
    )
    assert result.metadata is None


def test_read_use_case_fails_due_to_invalid_signature(mocker, use_case):
    fake_metadata = '{"foo": "bar"}'
    fake_signature = "invalid_signature"
    filepath = Path("fake.mp3")

    mock_metadata_reader = use_case.metadata_reader
    mock_signature_verifier = use_case.signature_verifier

    mock_read_request = mocker.Mock()
    mock_read_request.filepath = filepath

    mock_metadata_reader.read.return_value = AudioFileDataReading(
        is_success=True, metadata=fake_metadata, signature=fake_signature
    )
    mock_signature_verifier.is_signature_valid.return_value = False

    result = use_case.read(mock_read_request)

    assert not result.is_success
    assert result.error == "Signature verification failed."
    assert result.metadata is None
