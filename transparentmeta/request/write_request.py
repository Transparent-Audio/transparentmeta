# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
Defines the Pydantic model for handling metadata write requests.

This model is used to validate user-provided input and structure it for
processing by the metadata write use case. It ensures that:

1. The file path exists,
2. The file is in a supported audio format,
3. The file is a valid, functioning audio file,
4. The file has write permissions,
5. The file is not too large (for WAV files),
6. The metadata conforms to structured validation rules.
"""

from pathlib import Path

from pydantic import BaseModel, field_validator

from transparentmeta.entity.metadata import Metadata
from transparentmeta.request.file_validators import (
    validate_audio_file_is_functioning,
    validate_audio_format_is_supported,
    validate_file_exists,
    validate_file_has_write_permissions,
    validate_wav_file_is_not_too_large,
)


class WriteRequest(BaseModel):
    """Pydantic model representing a request to write metadata to an audio
    file.

    Attributes:
        filepath (Path): Path to the audio file. Validated for existence,
            supported format, integrity, and write permissions.
        metadata (Metadata): Metadata to be written to the audio file.
    """

    filepath: Path
    metadata: Metadata

    @field_validator("filepath")
    @classmethod
    def validate_filepath(cls, value: Path) -> Path:
        """Validates the provided file path using multiple file validation
        functions.

        Ensures that:
        1. The file exists.
        2. The file format is supported.
        3. The file is a valid audio file.
        4. The file has write permissions.
        5. The file is not too large (for WAV files).

        Args:
            value (Path): The path to the file.

        Returns:
            Path: The validated file path.

        Raises:
            FileNotFoundError: If the file does not exist.
            UnsupportedAudioFormatError: If the format is not supported.
            InvalidAudioFileError: If the file is not a functioning audio file.
            FilePermissionError: If the file is not writable.
            WAVTooLargeError: If the WAV file exceeds the maximum size limit.
        """
        value = validate_file_exists(value)
        value = validate_audio_format_is_supported(value)
        value = validate_audio_file_is_functioning(value)
        value = validate_file_has_write_permissions(value)
        value = validate_wav_file_is_not_too_large(value)
        return value
