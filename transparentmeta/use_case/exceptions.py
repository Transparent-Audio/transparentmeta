# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""This module defines custom exceptions for the use case component."""

from pathlib import Path
from typing import Tuple, Union

from transparentmeta.use_case.constants import SUPPORTED_AUDIO_FORMATS
from transparentmeta.utils.file_utils import get_file_extension


class UnsupportedAudioFormatError(Exception):
    """Raised when the audio file format is not supported."""

    def __init__(
        self,
        source: Union[str, Path],
        supported_formats: Tuple[str, ...] = SUPPORTED_AUDIO_FORMATS,
    ) -> None:
        self.supported_formats = supported_formats

        if isinstance(source, Path):
            self.filepath = source
            self.audio_format = get_file_extension(source)
            message = (
                f"Unsupported audio format '{self.audio_format}' for file: {self.filepath}. "
                f"Supported formats are: {', '.join(supported_formats)}."
            )
        else:
            self.audio_format = source
            message = (
                f"Unsupported audio format '{self.audio_format}'. "
                f"Supported formats are: {', '.join(supported_formats)}."
            )

        super().__init__(message)
