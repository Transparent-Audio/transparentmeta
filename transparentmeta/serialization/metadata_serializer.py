# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
Provides the `MetadataSerializer` class for converting Metadata objects
to and from JSON strings.
"""

import logging
from typing import Optional

from transparentmeta.entity.metadata import Metadata

logger = logging.getLogger(__name__)


class MetadataSerializer:
    """Handles serialization and deserialization of Metadata objects to and
    from JSON strings.

    Args:
        indent (Optional[int]): Number of spaces to use for indentation in the
            JSON output. If None, the JSON will be compact (no
            pretty-printing).
    """

    def __init__(self, indent: Optional[int] = None):
        self.indent = indent

    def serialize(self, metadata: Metadata) -> str:
        """Serialize the given Metadata object to a JSON string.

        Args:
            metadata (Metadata): The metadata object to serialize.

        Returns:
            metadata_string (str): A JSON-formatted string representation of
                the metadata.
        """
        metadata_string = metadata.model_dump_json(indent=self.indent)

        logger.debug(
            "Serialized Metadata object to JSON string: '%.40s'",
            metadata_string,
        )

        return metadata_string

    def deserialize(self, json_str: str) -> Metadata:
        """Deserialize a JSON string back into a Metadata object.

        Args:
            json_str (str): The JSON string to deserialize.

        Returns:
            metadata_obj (Metadata): A Metadata object created from the JSON
                string.
        """
        metadata_obj = Metadata.model_validate_json(json_str)

        logger.debug(
            "Deserialized JSON string to Metadata object '%.40s'",
            metadata_obj.model_dump(),
        )

        return metadata_obj
