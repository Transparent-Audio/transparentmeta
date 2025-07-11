# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
Utility functions for adding ID3v2 tags in audio files.

This module provides helpers to create, modify, and check ID3v2 tags in
MP3 and WAV audio files using the `mutagen` library.

These functions are used to embed or validate structured transparency
metadata within audio files.
"""

from mutagen.id3 import ID3, TXXX

from transparentmeta.use_case.types import MutagenID3AudioTypes


def create_id3_tags_in_file_if_none_exists(
    audio: MutagenID3AudioTypes,
) -> MutagenID3AudioTypes:
    """Ensures that the audio file has ID3 tags. If not, it adds empty tags.

    While ID3 tags are native to MP3 files, mutagen also allows adding ID3
    tags to WAV files by squeezing a custom ID3 chunk into the RIFF header
    of the WAV file.

    Args:
        audio (MutagenID3AudioTypes): The audio file object with ID3 support.

    Returns:
        MutagenID3AudioTypes: The audio file object with ID3 tags added if they were
            missing.
    """
    if audio.tags is None:
        audio.add_tags()
    return audio


def set_txxx_id3_tag(
    audio: MutagenID3AudioTypes,
    field: str,
    value: str,
) -> MutagenID3AudioTypes:
    """Sets a specific TXXX id3v2 tag in an audio file. TXXX tags are used for
    custom text information in ID3 tags, defined by users.

    Args:
        audio (MutagenID3AudioTypes): The audio file object.
        field (str): The TXXX field to set.
        value (str): The value to set for the specified field.

    Returns:
        MutagenID3AudioTypes: The modified audio file object with the updated tag.
    """
    assert isinstance(audio.tags, ID3)
    audio.tags.setall(field, [TXXX(encoding=3, desc=field, text=value)])
    return audio


def does_file_contain_any_id3_tags(audio: MutagenID3AudioTypes) -> bool:
    """Checks if the audio file contains any ID3 tags.

    Args:
        audio (MutagenID3AudioTypes): The audio file object with ID3 support.

    Returns:
        bool: True if the audio file contains any tags, False otherwise.
    """
    if audio.tags:
        return True
    return False
