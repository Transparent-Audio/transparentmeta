# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""This module defines custom exceptions for the request component."""

from pathlib import Path


class InvalidAudioFileError(Exception):
    """Raised when an audio file is invalid or corrupted."""

    def __init__(self, filepath: Path, error_message: str) -> None:
        self.filepath = filepath
        self.error_message = error_message
        super().__init__(
            f"Invalid audio file: {filepath}. Error: {error_message}"
        )


class NoWritePermissionsError(Exception):
    """Raised when a file does not have write permissions."""

    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath
        super().__init__(f"File is not writable: {filepath}")


class WAVTooLargeError(Exception):
    """Raised when a WAV file exceeds the maximum size limit."""

    def __init__(self, filepath: Path, max_size: int, file_size: int) -> None:
        self.filepath = filepath
        self.max_size = max_size
        self.file_size = file_size
        super().__init__(
            f"WAV file {filepath} exceeds the maximum size of {max_size} "
            f"bytes. File size: {file_size} bytes. Please reduce the file "
            f"size or try using MP3 instead."
        )
