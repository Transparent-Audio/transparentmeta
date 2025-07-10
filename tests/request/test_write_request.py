# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

from pathlib import Path

import pytest
from pydantic import ValidationError

from transparentmeta.entity.metadata import AIUsageLevel, Metadata
from transparentmeta.request.write_request import WriteRequest


@pytest.fixture
def mock_valid_file_validators(mocker):
    """Mocks all file validator functions to return a valid Path."""
    path = Path("/valid/path.wav")
    mocker.patch(
        "transparentmeta.request.write_request.validate_file_exists",
        return_value=path,
    )
    mocker.patch(
        "transparentmeta.request.write_request.validate_audio_format_is_supported",
        return_value=path,
    )
    mocker.patch(
        "transparentmeta.request.write_request.validate_audio_file_is_functioning",
        return_value=path,
    )
    mocker.patch(
        "transparentmeta.request.write_request.validate_file_has_write_permissions",
        return_value=path,
    )


def test_that_valid_write_request_is_created_succesfully(
    metadata_dict, mock_valid_file_validators
):

    data = {
        "filepath": "/valid/path.wav",
        "metadata": metadata_dict,
    }
    write_request = WriteRequest(**data)

    assert isinstance(write_request, WriteRequest)
    assert isinstance(write_request.metadata, Metadata)
    assert write_request.filepath == Path("/valid/path.wav")
    assert write_request.metadata.company == "Transparent Audio"


@pytest.mark.parametrize("missing_field", ["filepath", "metadata"])
def test_write_request_missing_required_fields_raises_validation_error(
    missing_field, metadata_dict, mock_valid_file_validators
):

    data = {
        "filepath": "/valid/path.wav",
        "metadata": metadata_dict,
    }
    del data[missing_field]

    with pytest.raises(ValidationError, match="Field required"):
        WriteRequest(**data)


def test_write_request_raises_with_non_existent_filepath(
    mocker, metadata_dict
):
    mocker.patch(
        "transparentmeta.request.write_request.validate_file_exists",
        side_effect=ValueError("File does not exist"),
    )

    data = {
        "filepath": "/invalid/path.wav",
        "metadata": metadata_dict,
    }

    with pytest.raises(ValidationError, match="File does not exist"):
        WriteRequest(**data)


def test_write_request_can_be_created_without_optional_fields(
    metadata_dict, mock_valid_file_validators
):
    data = {
        "filepath": "/valid/path.wav",
        "metadata": metadata_dict,
    }
    # Remove optional field 'additional_info'
    del metadata_dict["additional_info"]

    write_request = WriteRequest(**data)
    assert write_request.metadata.additional_info is None


def test_write_request_can_be_converted_to_and_from_dictionary(
    metadata_dict, mock_valid_file_validators
):

    data = {
        "filepath": "/valid/path.wav",
        "metadata": metadata_dict,
    }

    write_request = WriteRequest(**data)

    # Convert to dict
    request_dict = write_request.model_dump()
    assert request_dict["metadata"]["company"] == "Transparent Audio"
    assert request_dict["metadata"]["ai_usage_level"] == "ai_assisted"

    # Convert back to object
    new_request = WriteRequest(**request_dict)
    assert new_request.metadata.company == "Transparent Audio"
    assert new_request.metadata.ai_usage_level == AIUsageLevel.AI_ASSISTED
