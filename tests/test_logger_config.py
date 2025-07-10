# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

import logging

import pytest

from transparentmeta.logger_config import configure_logging


@pytest.fixture
def reset_logger():
    logger = logging.getLogger("transparentmeta")
    logger.handlers.clear()
    yield
    logger.handlers.clear()


def test_configure_logging_adds_handler_and_sets_level(reset_logger):
    configure_logging(level=logging.DEBUG)
    logger = logging.getLogger("transparentmeta")

    assert logger.level == logging.DEBUG
    assert len(logger.handlers) == 1
    handler = logger.handlers[0]
    assert isinstance(handler, logging.StreamHandler)
    assert isinstance(handler.formatter, logging.Formatter)
    assert handler.formatter._fmt.startswith("%(asctime)s [%(levelname)s]")


def test_configure_logging_does_not_duplicate_handlers(reset_logger):
    configure_logging()
    logger = logging.getLogger("transparentmeta")
    initial_handler_count = len(logger.handlers)

    configure_logging()  # Should not add another handler
    assert len(logger.handlers) == initial_handler_count
