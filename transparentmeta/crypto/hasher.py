# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Transparent Audio
# Author: Valerio Velardo - valerio@transparentaudio.ai

"""
This module provides a simple wrapper around Python's hashlib library to
compute cryptographic hash digests using various algorithms such as SHA-256,
SHA-512, and MD5.
"""

import hashlib
import logging

logger = logging.getLogger(__name__)


class Hasher:
    """A utility class for computing hash digests using various cryptographic
    algorithms.

    Attributes:
        hash_algorithm_name (str): The name of the hashing algorithm (e.g.,
            "sha256").
    """

    def __init__(self, hash_algorithm_name: str = "sha256") -> None:
        """Initializes the Hasher with the specified hashing algorithm.

        Args:
            hash_algorithm_name (str, optional): The name of the hash algorithm
                to use. Defaults to "sha256".

        Raises:
            ValueError: If the specified algorithm is not supported by hashlib.
        """
        self.hash_algorithm_name = hash_algorithm_name
        self._raise_value_error_if_hash_algorithm_is_not_available()

    def hash(self, data: bytes) -> str:
        """Computes the hash digest of the given data using the specified
        algorithm.

        Args:
            data (bytes): The input data to be hashed.

        Returns:
            hexadecimal_hash_digest (str): The hexadecimal digest of the
                hashed data.
        """
        hash_algorithm = hashlib.new(self.hash_algorithm_name)
        hash_algorithm.update(data)
        hexadecimal_hash_digest = hash_algorithm.hexdigest()

        logger.debug(
            "Computed %s hexadecimal hash: %s",
            self.hash_algorithm_name,
            hexadecimal_hash_digest,
        )

        return hexadecimal_hash_digest

    def _raise_value_error_if_hash_algorithm_is_not_available(self) -> None:
        if self.hash_algorithm_name not in hashlib.algorithms_available:
            raise ValueError(
                f"Invalid hash algorithm: {self.hash_algorithm_name}"
            )
