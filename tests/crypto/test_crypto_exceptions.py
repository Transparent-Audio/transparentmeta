# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

from transparentmeta.crypto.exceptions import NotEd25519KeyError


def test_not_ed25519_key_error():
    error = NotEd25519KeyError()
    assert isinstance(error, NotEd25519KeyError)
    assert str(error) == "Loaded key is not an Ed25519 key"
