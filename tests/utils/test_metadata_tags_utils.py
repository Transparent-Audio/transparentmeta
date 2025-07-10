# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from mutagen.wave import WAVE

from transparentmeta.use_case.constants import TRANSPARENCY_METADATA_FIELD
from transparentmeta.utils.metadata_tags_utils import (
    create_id3_tags_in_file_if_none_exists,
    does_file_contain_any_id3_tags,
    set_txxx_id3_tag,
)


def test_create_id3_tags_in_file_if_none_exists(temp_wav):
    audio = WAVE(temp_wav)
    # Remove tags if any exist
    audio.delete()
    audio.save()

    audio = WAVE(temp_wav)
    assert audio.tags is None

    updated_audio = create_id3_tags_in_file_if_none_exists(audio)
    assert isinstance(updated_audio.tags, ID3)


def test_audio_file_is_returned_if_id3_tags_already_exist(
    temp_mp3_file_with_metadata,
):
    audio = MP3(temp_mp3_file_with_metadata)
    assert isinstance(audio.tags, ID3)

    updated_audio = create_id3_tags_in_file_if_none_exists(audio)
    assert updated_audio is audio


def test_txxx_id3_tag_is_set_correctly(temp_mp3):
    audio = MP3(temp_mp3)
    audio = create_id3_tags_in_file_if_none_exists(audio)

    field = "test-field"
    value = "test-value"
    audio = set_txxx_id3_tag(audio, field, value)

    assert audio.tags["TXXX:test-field"].text[0] == "test-value"


def test_txxx_audio_tag_is_reset_when_it_already_exists(
    temp_mp3_file_with_metadata,
):
    audio = MP3(temp_mp3_file_with_metadata)
    audio = create_id3_tags_in_file_if_none_exists(audio)

    field = TRANSPARENCY_METADATA_FIELD
    value = "new-test-value"
    audio = set_txxx_id3_tag(audio, field, value)

    assert audio.tags[f"TXXX:{field}"].text[0] == "new-test-value"


def test_does_file_contain_any_tags_return_false_when_tags_not_exist(temp_mp3):
    audio = MP3(temp_mp3)
    audio.delete()
    audio.save()
    assert does_file_contain_any_id3_tags(audio) is False


def test_does_file_contain_any_tags_return_true_when_tags_exist(
    temp_mp3_file_with_metadata,
):
    audio = MP3(temp_mp3_file_with_metadata)
    assert does_file_contain_any_id3_tags(audio) is True
