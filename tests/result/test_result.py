# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

import dataclasses

import pytest

from transparentmeta.entity.metadata import Metadata
from transparentmeta.result.result import ReadResult, Result


def test_result_success():
    result = Result(is_success=True)
    assert result.is_success is True
    assert result.error is None


def test_result_failure_with_error():
    result = Result(is_success=False, error="Something went wrong")
    assert result.is_success is False
    assert result.error == "Something went wrong"


def test_read_use_case_result_with_metadata(mocker):
    metadata = mocker.Mock(spec=Metadata)
    result = ReadResult(is_success=True, metadata=metadata)
    assert result.is_success is True
    assert result.metadata == metadata
    assert result.error is None


def test_read_use_case_result_failure():
    result = ReadResult(is_success=False, error="Read error")
    assert result.is_success is False
    assert result.metadata is None
    assert result.error == "Read error"


def test_result_immutable():
    result = Result(is_success=True)
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.is_success = False
