# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
This module hosts function validators that can be used to validate
requests with audio files using Pydantic models.
"""

import os
from pathlib import Path

from mutagen.mp3 import MP3
from mutagen.wave import WAVE

from transparentmeta.request.exceptions import (
    InvalidAudioFileError,
    NoWritePermissionsError,
)
from transparentmeta.use_case.constants import SUPPORTED_AUDIO_FORMATS
from transparentmeta.use_case.exceptions import UnsupportedAudioFormatError
from transparentmeta.utils.file_utils import get_file_extension


def validate_file_exists(filepath: Path) -> Path:
    """Validates that a file exists at the given path.

    Args:
        filepath (Path): The path to the file.

    Raises:
        FileNotFoundError: If the file does not exist.

    Returns:
        filepath (Path): The validated filepath.
    """
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    return filepath


def validate_audio_format_is_supported(filepath: Path) -> Path:
    """Validates that the file at the given path is an audio file.

    Args:
        filepath (Path): The path to the file.

    Raises:
        UnsupportedAudioFormatError: If the file is not an audio file.

    Returns:
        filepath (Path): The validated filepath.
    """
    extension = get_file_extension(filepath)
    if extension not in SUPPORTED_AUDIO_FORMATS:
        raise UnsupportedAudioFormatError(filepath, SUPPORTED_AUDIO_FORMATS)
    return filepath


def validate_audio_file_is_functioning(filepath: Path) -> Path:
    """Validates that the audio file is a supported and correctly functioning
    audio file.

    Args:
        filepath (Path): The path to the file.

    Raises:
        InvalidAudioFileError: If the file is not a valid supported audio file.

    Returns:
        filepath (Path): The validated filepath.
    """
    extension = get_file_extension(filepath)
    try:
        if extension == "mp3":
            MP3(filepath)
        elif extension in ["wav", "wave"]:
            WAVE(filepath)
    except Exception as err:
        raise InvalidAudioFileError(filepath, str(err)) from err
    return filepath


def validate_file_has_write_permissions(filepath: Path) -> Path:
    """
    Validates that the file at the given path has write permissions.

    Args:
        filepath (Path): The path to the file.

    Raises:
        NoWritePermissionsError: If the file does not have write permissions.

    Returns:
        filepath (Path): The validated filepath.
    """
    if not os.access(filepath, os.W_OK):
        raise NoWritePermissionsError(filepath)
    return filepath
