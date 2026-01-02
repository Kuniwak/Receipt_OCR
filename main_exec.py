#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess


USAGE = """\
Usage:
  cat filelist.txt | ./main_exec.py -exec <cmd...> \\;

Behavior:
  - Read UTF-8 lines from stdin (newline-delimited file paths).
  - For each line, strip the trailing newline and replace occurrences of "{}"
    in the exec-args with that path, then execute the command.
  - Semantics are similar to: find ... -exec ... \\;
"""


def parse_exec_argv(argv: list[str]) -> list[str]:
    """
    Parse command line like: -exec <cmd...> \\;
    Returns the <cmd...> as a list of args.
    """
    if len(argv) < 2 or argv[1] != "-exec":
        raise ValueError("missing -exec")

    # Everything after -exec until "\;" or ";" is the command template
    template = []
    for a in argv[2:]:
        if a in ("\\;", ";"):
            break
        template.append(a)

    if not template:
        raise ValueError("empty exec template")
    # Ensure terminator exists
    if argv[-1] not in ("\\;", ";") and ("\\;" not in argv and ";" not in argv):
        raise ValueError("missing terminator \\; (or ;)")

    return template


def main() -> int:
    try:
        template = parse_exec_argv(sys.argv)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print(USAGE, file=sys.stderr)
        return 2

    any_failed = False

    # Read stdin as UTF-8 text; keep control over newline stripping.
    # Use sys.stdin.buffer for robust handling, then decode per line.
    for raw in sys.stdin.buffer:
        try:
            line = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as e:
            print(f"Error: stdin is not valid UTF-8: {e}", file=sys.stderr)
            return 2

        # Remove trailing newline(s) like find does (newline-delimited input).
        path = line.rstrip("\n")
        if path.endswith("\r"):
            path = path.rstrip("\r")

        # Skip completely empty lines (common in piped lists).
        if path == "":
            continue

        # Replace {} in each argument (token-level, like find -exec)
        argv = [arg.replace("{}", path) for arg in template]

        try:
            # Direct exec (no shell), so spaces in paths are safe.
            r = subprocess.run(argv)
        except FileNotFoundError:
            print(f"Error: command not found: {argv[0]}", file=sys.stderr)
            return 127
        except Exception as e:
            print(f"Error: failed to execute {argv!r}: {e}", file=sys.stderr)
            any_failed = True
            continue

        if r.returncode != 0:
            any_failed = True

    return 1 if any_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
