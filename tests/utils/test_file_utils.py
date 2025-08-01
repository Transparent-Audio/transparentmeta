# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

from pathlib import Path

from transparentmeta.utils.file_utils import get_file_extension, get_file_size


def test_get_file_extension():

    # Test with a standard file
    assert get_file_extension(Path("example.mp3")) == "mp3"

    # Test with a file with multiple dots
    assert get_file_extension(Path("archive.tar.gz")) == "gz"

    # Test with a file without an extension
    assert get_file_extension(Path("README")) == ""

    # Test with a file that has no leading dot in the extension
    assert get_file_extension(Path("data.json")) == "json"


def test_get_file_size_file_exists(tmp_path):
    file_path = tmp_path / "sample.bin"
    content = b"TransparentMeta"
    file_path.write_bytes(content)

    size = get_file_size(file_path)
    assert size == len(content), f"Expected size {len(content)}, got {size}"


def test_get_file_size_file_not_exists(tmp_path):
    missing = tmp_path / "nonexistent.file"
    assert not missing.exists()

    size = get_file_size(missing)
    assert size == 0, f"Expected size 0 for missing file, got {size}"
