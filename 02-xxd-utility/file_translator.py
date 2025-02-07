"""
    Script designed to print the contents of a file in either hexadecimal or binary format,
    depending on its extension.

    Usage:
        python file_translator.py --file path/to/file
        (supports text-based files like .txt or .csv for hex viewing, and binary files for binary viewing)
"""
import os
import argparse
import re

import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--file")
args = parser.parse_args()


def to_hex(value: str) -> str:
    hex_val = value.encode().hex()
    formated_val = ' '.join(re.findall('.{2}', hex_val))

    return formated_val


def print_hex(file_path: str, max_rows: int = None) -> None:
    data = np.loadtxt(file_path, delimiter=',', dtype=str, max_rows=max_rows)

    for row in data:
        print(f"{row[0]}  {row[1]}")
        print(f"{to_hex(row[0])}  {to_hex(row[1])}")
        print()


def print_bin(file_path: str) -> None:
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(16)
            if not chunk:
                break

            hex_values = ' '.join(f'{byte:02x}' for byte in chunk)
            hex_display = f'{hex_values:<48}'

            print(f'{hex_display}')


if __name__ == "__main__":
    if os.path.basename(args.file).endswith('.txt') or os.path.basename(args.file).endswith('.csv'):
        print_hex(args.file)
    else:
        print_bin(args.file)