# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from transparentmeta.entity.metadata import AIUsageLevel, Metadata


def test_that_metadata_object_with_valid_args_is_created_successfully():
    metadata = Metadata(
        company="Transparent Audio",
        model="v2.1",
        created_at=datetime.now(timezone.utc),
        ai_usage_level=AIUsageLevel.AI_ASSISTED,
        content_id="12345",
        user_id="user_67890",
        private_key_id="dummy_private_key_id",
        additional_info={
            "attribution": {"lyrics": "John Doe", "composer": "Jane Smith"}
        },
    )
    assert metadata.company == "Transparent Audio"
    assert metadata.ai_usage_level == AIUsageLevel.AI_ASSISTED
    assert isinstance(metadata.created_at, datetime)


@pytest.mark.parametrize(
    "missing_field",
    [
        "company",
        "model",
        "created_at",
        "ai_usage_level",
        "content_id",
        "user_id",
        "private_key_id",
    ],
)
def test_that_missing_required_field_raises_validation_error(
    missing_field, metadata_dict
):
    del metadata_dict[missing_field]

    with pytest.raises(ValidationError, match="Field required"):
        Metadata(**metadata_dict)


@pytest.mark.parametrize(
    "field, value",
    [
        ("company", "A"),  # Too short
        ("company", "A" * 51),  # Too long
        ("model", "X" * 51),  # Too long
        ("content_id", ""),  # Too short
        ("content_id", "X" * 51),  # Too long
        ("private_key_id", ""),  # Too short
        ("private_key_id", "X" * 51),  # Too long
        ("user_id", "X"),  # Too short
        ("user_id", "X" * 51),  # Too long
    ],
)
def test_that_string_lenght_constraints_are_enforced_in_metadata_creation(
    field, value, metadata_dict
):
    metadata_dict[field] = value

    with pytest.raises(ValidationError):
        Metadata(**metadata_dict)


def test_metadata_optional_fields_omitted_without_error():
    metadata = Metadata(
        company="Transparent Audio",
        model="v2.1",
        created_at=datetime.now(timezone.utc),
        ai_usage_level=AIUsageLevel.AI_GENERATED,
        content_id="12345",
        user_id="user_67890",
        private_key_id="dummy_private_key_id",
    )
    assert metadata.additional_info is None


@pytest.mark.parametrize(
    "valid_usage_level",
    [
        AIUsageLevel.AI_GENERATED,
        AIUsageLevel.AI_ASSISTED,
        AIUsageLevel.HUMAN_CREATED,
    ],
)
def test_metadata_ai_usage_level_accepts_valid_enum(valid_usage_level):
    metadata = Metadata(
        company="Transparent Audio",
        model="v2.1",
        created_at=datetime.now(timezone.utc),
        ai_usage_level=valid_usage_level,
        content_id="12345",
        user_id="user_67890",
        private_key_id="dummy_private_key_id",
    )
    assert metadata.ai_usage_level == valid_usage_level


def test_metadata_invalid_ai_usage_level_enum_raises_validation_error():
    with pytest.raises(ValidationError):
        Metadata(
            company="Transparent Audio",
            model="v2.1",
            created_at=datetime.now(timezone.utc),
            ai_usage_level="unsupported_ai_level",  # Invalid value
            content_id="12345",
            user_id="user_67890",
            private_key_id="dummy_private_key_id",
        )
