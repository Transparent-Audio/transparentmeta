# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
This module defines type aliases used across the use_case package.

This includes shared types for ID3-tagged audio files compatible with the
Mutagen library (e.g., MP3 and WAV).
"""

from mutagen.mp3 import MP3
from mutagen.wave import WAVE

MutagenID3AudioTypes = MP3 | WAVE
