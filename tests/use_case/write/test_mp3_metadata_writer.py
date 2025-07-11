# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

from mutagen.id3 import ID3
from mutagen.mp3 import MP3

from transparentmeta.use_case.write.mp3_metadata_writer import (
    MP3MetadataWriter,
)


def test_write_metadata_to_mp3(temp_mp3):
    writer = MP3MetadataWriter()

    metadata = "time=2024-02-25||company=Google AI"
    signature = "signedhash123456789"

    writer.write(temp_mp3, metadata, signature)

    audio = MP3(temp_mp3, ID3=ID3)

    assert f"TXXX:{writer.transparency_metadata_field}" in audio.tags
    assert f"TXXX:{writer.signature_field}" in audio.tags
    assert (
        audio.tags[f"TXXX:{writer.transparency_metadata_field}"].text[0]
        == metadata
    )
    assert audio.tags[f"TXXX:{writer.signature_field}"].text[0] == signature


def test_write_metadata_to_mp3_with_custom_fields(temp_mp3):
    writer = MP3MetadataWriter("custom_meta", "custom_sig")

    metadata = "project=AI Music||date=2025-03-10"
    signature = "sig_abc123xyz"

    writer.write(temp_mp3, metadata, signature)

    audio = MP3(temp_mp3, ID3=ID3)

    assert "TXXX:custom_meta" in audio.tags
    assert "TXXX:custom_sig" in audio.tags
    assert audio.tags["TXXX:custom_meta"].text[0] == metadata
    assert audio.tags["TXXX:custom_sig"].text[0] == signature


def test_overwrite_existing_metadata_to_mp3(temp_mp3):
    writer = MP3MetadataWriter()

    metadata1 = "field1=value1||field2=value2"
    signature1 = "sig_old123"
    writer.write(temp_mp3, metadata1, signature1)

    # Overwrite metadata
    metadata2 = "new_field=updated_value"
    signature2 = "sig_new456"
    writer.write(temp_mp3, metadata2, signature2)

    audio = MP3(temp_mp3, ID3=ID3)

    assert (
        audio.tags[f"TXXX:{writer.transparency_metadata_field}"].text[0]
        == metadata2
    )
    assert audio.tags[f"TXXX:{writer.signature_field}"].text[0] == signature2
