#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main_subtract.py

Usage:
  python3.14 ./main_subtract.py <A_path> <B_path>

Reads A and B as UTF-8 text, splits by newline into A', B'.
Outputs, in A' order, only elements not contained in B'.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def read_utf8_text(path_str: str) -> str:
    """
    Read file content as UTF-8 text.
    Raises an exception if unreadable (missing, permission, decode error, etc.).
    """
    p = Path(path_str)
    # Ensure we're reading bytes and decoding as UTF-8 explicitly.
    data = p.read_bytes()
    return data.decode("utf-8")


def split_lines(text: str) -> list[str]:
    """
    Split by newline ('\\n') as specified.
    Note: this preserves an empty last element if the text ends with a newline.
    """
    return text.split("\n")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("A", help="Path to file A")
    parser.add_argument("B", help="Path to file B")
    args = parser.parse_args(argv)

    # Readability checks: if either fails, print an error to stderr.
    try:
        a_text = read_utf8_text(args.A)
    except Exception as ex:
        eprint(f"error: cannot read A '{args.A}': {ex}")
        return 1

    try:
        b_text = read_utf8_text(args.B)
    except Exception as ex:
        eprint(f"error: cannot read B '{args.B}': {ex}")
        return 1

    a_lines = split_lines(a_text)
    b_lines = split_lines(b_text)

    # Use a hash set for O(1) expected membership tests (avoids linear scan).
    b_set = set(b_lines)

    out = sys.stdout
    for line in a_lines:
        if line not in b_set:
            out.write(line)
            out.write("\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
