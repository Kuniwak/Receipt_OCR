#!/usr/bin/env python3
"""
Replace placeholders in a template file with stdin content.

Usage:
    ./main_stdinsubst.py -t tmpl.md -r %%EXAMPLE%% < ./example.txt
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        description='Replace placeholders in a template file with stdin content'
    )
    parser.add_argument(
        '-t',
        '--template',
        required=True,
        help='Template file path'
    )
    parser.add_argument(
        '-r',
        '--replace',
        required=True,
        help='Placeholder string to replace'
    )

    args = parser.parse_args()

    # Read template file
    try:
        with open(args.template, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        print(f"Error: Template file '{args.template}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading template file: {e}", file=sys.stderr)
        sys.exit(1)

    # Read stdin
    try:
        stdin_content = sys.stdin.read()
    except Exception as e:
        print(f"Error reading stdin: {e}", file=sys.stderr)
        sys.exit(1)

    # Replace placeholder with stdin content
    result = template_content.replace(args.replace, stdin_content)

    # Output result
    print(result, end='')


if __name__ == '__main__':
    main()
