"""
A utility script to insert or remove SPDX license headers from Python source
files.

This tool helps ensure license compliance by adding standardized SPDX headers
(e.g., GPL-3.0-or-later) and optional copyright statements to the top of each
Python file in a project. It can also cleanly remove these headers and restore
module-level docstrings or code to the top of the file.

Usage:
    python spdx_header_tool.py insert   # Insert headers
    python spdx_header_tool.py remove   # Remove headers

Options:
    --path <dir>   Specify the root directory to scan (default: current
        directory)

This script excludes itself and any files inside virtual environments (e.g.,
"venv").
"""

import argparse
from pathlib import Path

SPDX_HEADER = "# SPDX-License-Identifier: GPL-3.0-or-later"
COPYRIGHT_HEADER = "# Copyright (c) 2025 Transparent Audio"
AUTHOR_HEADER = "# Author: Valerio Velardo - valerio@transparentaudio.ai"
THIS_SCRIPT_NAME = Path(__file__).name


def find_python_files(root_dir: Path):
    return [
        f
        for f in root_dir.rglob("*.py")
        if f.is_file()
        and "venv" not in f.parts
        and f.name != THIS_SCRIPT_NAME  # exclude this script
    ]


def insert_headers(file_path: Path):
    with file_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    # Skip if already contains SPDX header
    if any(SPDX_HEADER in line for line in lines):
        return

    new_lines = [SPDX_HEADER + "\n", COPYRIGHT_HEADER + "\n", AUTHOR_HEADER + "\n", "\n"] + lines

    with file_path.open("w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(f"[+] Inserted header: {file_path}")


def remove_headers(file_path: Path):
    with file_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    # Remove SPDX and copyright lines
    cleaned = []
    for line in lines:
        if line.strip() in (SPDX_HEADER, COPYRIGHT_HEADER, AUTHOR_HEADER):
            continue
        cleaned.append(line)

    # Remove all leading blank lines (after removing headers)
    while cleaned and cleaned[0].strip() == "":
        cleaned.pop(0)

    with file_path.open("w", encoding="utf-8") as f:
        f.writelines(cleaned)
    print(f"[-] Removed header: {file_path}")


def main():
    parser = argparse.ArgumentParser(description="Insert or remove SPDX headers.")
    parser.add_argument("action", choices=["insert", "remove"], help="What to do")
    parser.add_argument(
        "--path", type=str, default=".", help="Root directory to search (default: .)"
    )
    args = parser.parse_args()

    root = Path(args.path).resolve()
    py_files = find_python_files(root)

    for file in py_files:
        if args.action == "insert":
            insert_headers(file)
        elif args.action == "remove":
            remove_headers(file)


if __name__ == "__main__":
    main()
