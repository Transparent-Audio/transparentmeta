# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
Defines the Pydantic model for handling metadata read requests.

This model is used to validate user-provided input and structure it for
processing by the metadata read use case. It ensures that the given file path:

1. Exists on disk,
2. Is in a supported audio format,
3. Is a valid, functioning audio file,
4. Is not too large (for WAV files).
"""

from pathlib import Path

from pydantic import BaseModel, field_validator

from transparentmeta.request.file_validators import (
    validate_audio_file_is_functioning,
    validate_audio_format_is_supported,
    validate_file_exists,
    validate_wav_file_is_not_too_large,
)


class ReadRequest(BaseModel):
    """Pydantic model representing a request to read metadata from an audio
    file.

    Attributes:
        filepath (Path): Path to the audio file. Validated for existence,
        supported format, and file integrity.
    """

    filepath: Path

    @field_validator("filepath")
    @classmethod
    def validate_filepath(cls, value: Path) -> Path:
        """Validates the provided filepath using multiple file validation
        functions.

        Ensures that:
        1. The file exists.
        2. The file format is supported.
        3. The file is a valid audio file.
        4. The file is not too large (for WAV files).


        Args:
            value (Path): The path to the file.

        Returns:
            Path: The validated filepath.

        Raises:
            FileNotFoundError: If the file does not exist.
            UnsupportedAudioFormatError: If the file format is not supported.
            InvalidAudioFileError: If the file is not a functioning audio file.
            WAVTooLargeError: If the WAV file exceeds the maximum size limit.
        """
        value = validate_file_exists(value)
        value = validate_audio_format_is_supported(value)
        value = validate_audio_file_is_functioning(value)
        value = validate_wav_file_is_not_too_large(value)
        return value
