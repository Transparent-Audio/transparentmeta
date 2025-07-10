# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

"""
Utility functions for file-related operations.

This module provides helper functions to work with files, such as extracting
file extensions in a normalized format.
"""

from pathlib import Path


def get_file_extension(filepath: Path) -> str:
    """Extracts the file extension from a given filepath.

    Args:
        filepath (Path): The path to the file.

    Returns:
        str: The file extension in lowercase without the leading dot.
    """
    return filepath.suffix.lower().lstrip(".")
