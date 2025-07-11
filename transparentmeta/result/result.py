# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
Defines result classes representing the outcomes of use cases in
transparentmeta.

Use cases implement the core business logic, and each result class captures
the success status and any associated data or errors.
"""

from dataclasses import dataclass
from typing import Optional

from transparentmeta.entity.metadata import Metadata


@dataclass(frozen=True)
class Result:
    """Base class for representing the outcome of a use case.

    Attributes:
        is_success (bool): True if the use case completed successfully; False
            otherwise.
        error (Optional[str]): An optional error message if the use case failed.
    """

    is_success: bool
    error: Optional[str] = None


@dataclass(frozen=True)
class ReadResult(Result):
    """Represents the result of a metadata read use case.

    Extends `Result` by including a deserialized Metadata object, if available.

    Attributes:
        metadata (Optional[Metadata]): The deserialized metadata object, or
            None if unavailable.
    """

    metadata: Optional[Metadata] = None
