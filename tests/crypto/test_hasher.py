# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2025 Valerio Velardo / Transparent Audio

import hashlib

import pytest

from transparentmeta.crypto.hasher import Hasher


@pytest.mark.parametrize(
    "algorithm, expected_hash",
    [
        ("sha256", hashlib.sha256(b"test").hexdigest()),
        ("sha512", hashlib.sha512(b"test").hexdigest()),
        ("md5", hashlib.md5(b"test").hexdigest()),
        ("blake2b", hashlib.blake2b(b"test").hexdigest()),
        ("blake2s", hashlib.blake2s(b"test").hexdigest()),
    ],
)
def test_hasher_produces_correct_hashes_for_different_algos(
    algorithm, expected_hash
):
    hasher = Hasher(algorithm)
    assert hasher.hash(b"test") == expected_hash


def test_hash_empty_data_matches_hashlib_output():
    hasher = Hasher("sha256")
    expected_hash = hashlib.sha256(b"").hexdigest()
    assert hasher.hash(b"") == expected_hash


@pytest.mark.parametrize(
    "invalid_algorithm", ["fakehash", "sha1024", "notrealhash"]
)
def test_invalid_hash_algorithm_raises_error(invalid_algorithm):
    with pytest.raises(
        ValueError, match=f"Invalid hash algorithm: {invalid_algorithm}"
    ):
        Hasher(invalid_algorithm)


def test_hash_used_multiple_times_produces_same_result():
    hasher = Hasher("sha256")
    data = b"consistent hash"
    assert hasher.hash(data) == hasher.hash(data)


def test_different_data_produce_different_hash():
    hasher = Hasher("sha256")
    hash1 = hasher.hash(b"data1")
    hash2 = hasher.hash(b"data2")
    assert hash1 != hash2


def test_two_hasher_instances_do_not_interfere_with_each_other():
    hasher1 = Hasher("sha256")
    hasher2 = Hasher("sha256")

    hash1 = hasher1.hash(b"instance1")
    hash2 = hasher2.hash(b"instance2")

    assert hash1 != hash2
