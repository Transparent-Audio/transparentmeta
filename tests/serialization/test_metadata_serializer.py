# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

import json
from datetime import datetime

from transparentmeta.entity.metadata import AIUsageLevel, Metadata
from transparentmeta.serialization.metadata_serializer import (
    MetadataSerializer,
)


def test_metadata_serialized_correctly_to_json_string():
    metadata = Metadata(
        company="Transparent Audio",
        model="v1.0",
        created_at=datetime(2024, 1, 1, 12, 0, 0),
        ai_usage_level=AIUsageLevel.AI_ASSISTED,
        content_id="abc123",
        user_id="user_456",
        private_key_id="key_789",
        additional_info={"genre": "ambient"},
    )

    serializer = MetadataSerializer(indent=None)
    json_string = serializer.serialize(metadata)

    assert isinstance(json_string, str)
    assert "ai_assisted" in json_string

    # Ensure it's valid JSON
    parsed = json.loads(json_string)

    assert parsed["company"] == "Transparent Audio"
    assert parsed["model"] == "v1.0"
    assert parsed["ai_usage_level"] == "ai_assisted"
    assert parsed["content_id"] == "abc123"
    assert parsed["user_id"] == "user_456"
    assert parsed["private_key_id"] == "key_789"
    assert parsed["additional_info"] == {"genre": "ambient"}
    assert "created_at" in parsed


def test_serialize_metadata_with_indent(metadata_dict):
    metadata = Metadata(**metadata_dict)

    serializer = MetadataSerializer(indent=4)
    json_string = serializer.serialize(metadata)

    # Given we passed "indent=4" in the constructor, pretty JSON has newlines
    # and indentation we can check
    assert "\n" in json_string
    assert "    " in json_string  # 4-space indent


def test_deserialize_metadata_json_string_to_metadata_object():
    json_string = (
        '{"company": "Transparent Audio", "model": "v1.0", '
        '"created_at": "2024-01-01T12:00:01", '
        '"ai_usage_level": "ai_assisted", '
        '"content_id": "abc123", '
        '"user_id": "user_456", '
        '"private_key_id": "key_789", '
        '"additional_info": {"genre": "ambient"}}'
    )

    serializer = MetadataSerializer()
    metadata = serializer.deserialize(json_string)

    assert isinstance(metadata, Metadata)
    assert metadata.company == "Transparent Audio"
    assert metadata.model == "v1.0"
    assert metadata.ai_usage_level == AIUsageLevel.AI_ASSISTED
    assert metadata.content_id == "abc123"
    assert metadata.user_id == "user_456"
    assert metadata.private_key_id == "key_789"
    assert metadata.additional_info == {"genre": "ambient"}
    assert metadata.created_at.isoformat() == "2024-01-01T12:00:01"
    assert metadata.created_at.year == 2024
