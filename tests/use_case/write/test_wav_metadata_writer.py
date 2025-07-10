# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

from mutagen.id3 import TXXX
from mutagen.wave import WAVE

from transparentmeta.use_case.write.wav_metadata_writer import (
    WAVMetadataWriter,
)


def test_write_metadata_to_wav(temp_wav):
    writer = WAVMetadataWriter()
    metadata = "time=2024-02-25||company=Google AI"
    signature = "signedhash123456789"

    writer.write(temp_wav, metadata, signature)

    audio = WAVE(temp_wav)

    # Assertions - Check if TXXX frames exist
    assert f"TXXX:{writer.transparency_metadata_field}" in audio.tags
    assert f"TXXX:{writer.signature_field}" in audio.tags

    # Verify the actual stored metadata inside TXXX frames
    transparency_frame = audio.tags[
        f"TXXX:{writer.transparency_metadata_field}"
    ]
    signature_frame = audio.tags[f"TXXX:{writer.signature_field}"]

    assert isinstance(transparency_frame, TXXX)
    assert isinstance(signature_frame, TXXX)
    assert transparency_frame.text == [metadata]
    assert signature_frame.text == [signature]


def test_write_metadata_preserves_existing_tags_in_wav(temp_wav):
    writer = WAVMetadataWriter()
    initial_metadata = "existing_field=Original Metadata"
    new_metadata = "new_metadata=Updated Data"
    signature = "newsignedhash987"

    audio = WAVE(temp_wav)
    audio.add_tags()
    audio.tags["TXXX:existing_field"] = TXXX(
        encoding=3, desc="existing_field", text=initial_metadata
    )
    audio.save()

    # Write new metadata
    writer.write(temp_wav, new_metadata, signature)

    audio = WAVE(temp_wav)

    # Assertions - Ensure old metadata is preserved
    assert "TXXX:existing_field" in audio.tags
    assert f"TXXX:{writer.transparency_metadata_field}" in audio.tags
    assert f"TXXX:{writer.signature_field}" in audio.tags

    # Check values
    assert audio.tags["TXXX:existing_field"].text == [initial_metadata]
    assert audio.tags[f"TXXX:{writer.transparency_metadata_field}"].text == [
        new_metadata
    ]
    assert audio.tags[f"TXXX:{writer.signature_field}"].text == [signature]
