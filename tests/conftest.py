# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

import logging
import shutil
from datetime import datetime
from pathlib import Path

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from mutagen.id3 import ID3, TXXX
from mutagen.mp3 import MP3
from mutagen.wave import WAVE

from transparentmeta.entity.metadata import AIUsageLevel, Metadata
from transparentmeta.logger_config import configure_logging
from transparentmeta.use_case.constants import (
    SIGNATURE_FIELD,
    TRANSPARENCY_METADATA_FIELD,
)


@pytest.fixture(autouse=True, scope="session")
def configure_library_logging():
    """Automatically configure logging once for all tests."""
    configure_logging(logging.DEBUG)


@pytest.fixture
def metadata_dict():
    return {
        "company": "Transparent Audio",
        "model": "v2.1",
        "created_at": datetime.utcnow(),
        "ai_usage_level": AIUsageLevel.AI_ASSISTED,
        "content_id": "12345",
        "user_id": "user_67890",
        "private_key_id": "dummy_private_key_id",
        "additional_info": {
            "attribution": {"lyrics": "John Doe", "composer": "Jane Smith"}
        },
    }


@pytest.fixture
def metadata(metadata_dict):
    return Metadata(**metadata_dict)


@pytest.fixture
def keys():
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    return {
        "private_key": private_key,
        "public_key": public_key,
    }


@pytest.fixture
def temp_mp3(tmp_path):
    """Creates a temporary copy of a valid MP3 file for testing."""
    test_dir = Path(__file__).parent
    original_mp3 = test_dir / "test_data" / "test.mp3"
    mp3_file = tmp_path / "test.mp3"
    shutil.copy(original_mp3, mp3_file)  # Copy MP3 file to temp directory
    return mp3_file


@pytest.fixture
def temp_wav(tmp_path):
    """Creates a temporary WAV file for testing."""
    wav_file = tmp_path / "test.wav"
    with open(wav_file, "wb") as f:
        f.write(
            b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00"
            b"\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00"
        )
    return wav_file


@pytest.fixture
def temp_mp3_file_with_metadata(temp_mp3):
    audio = MP3(temp_mp3, ID3=ID3)
    audio.add_tags()
    audio.tags.add(
        TXXX(
            encoding=3, desc=TRANSPARENCY_METADATA_FIELD, text="some_metadata"
        )
    )
    audio.tags.add(
        TXXX(encoding=3, desc=SIGNATURE_FIELD, text="some_signature")
    )
    audio.save()
    yield temp_mp3


@pytest.fixture
def temp_wav_file_with_metadata(temp_wav):
    audio = WAVE(temp_wav)
    audio.add_tags()
    audio.tags.add(
        TXXX(
            encoding=3, desc=TRANSPARENCY_METADATA_FIELD, text="some_metadata"
        )
    )
    audio.tags.add(
        TXXX(encoding=3, desc=SIGNATURE_FIELD, text="some_signature")
    )
    audio.save()
    yield temp_wav


@pytest.fixture
def temp_corrupt_mp3(tmp_path):
    """Creates a temporary corrupt MP3 file for testing."""
    mp3_file = tmp_path / "test.mp3"
    with open(mp3_file, "wb") as f:
        f.write(b"corrupt mp3 file")
    return mp3_file


@pytest.fixture
def temp_corrupt_wav(tmp_path):
    """Creates a temporary corrupt WAV file for testing."""
    wav_file = tmp_path / "test.wav"
    with open(wav_file, "wb") as f:
        f.write(b"corrupt wav file")
    return wav_file
