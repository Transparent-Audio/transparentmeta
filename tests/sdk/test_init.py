# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

import transparentmeta.sdk as sdk


def test_sdk_public_api():
    expected_exports = {
        "TransparentMetadataWriter",
        "TransparentMetadataReader",
        "build_transparent_metadata_writer",
        "build_transparent_metadata_reader",
    }
    actual_exports = set(sdk.__all__)

    assert actual_exports == expected_exports
