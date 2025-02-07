"""
    A fun script for searching for a word in a file system.
    Not intended for production use.

    Usage:
        python file_searcher.py --dir path/to/search --word search_term
        (optional flags: --verbose for detailed output, --casesen for case-sensitive search)
"""
import os
import argparse

args = argparse.ArgumentParser()
args.add_argument("--dir", type=str, default=".")
args.add_argument("--word", type=str, required=True)
args.add_argument("--verbose", action="store_true")
args.add_argument("--casesen", action="store_true")
args = args.parse_args()

file_matches = []


def finder(path):
    if args.verbose:
        print(f"-\nEntering {path}")
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            finder(full_path)
        elif os.path.isfile(full_path):
            enter_file(full_path)
        else:
            if args.verbose:
                print(f"  Unknown file type: {item}")
    return


def enter_file(file_path):
    if args.verbose:
        print(f"  Opening {file_path}")

    global file_matches

    with open(file_path, "r") as file:
        for line in file:
            if args.casesen:
                if args.word in line:
                    if args.verbose:
                        print("  | Match found!")
                    file_matches.append(file_path)
                    break
            else:
                if args.word.lower() in line.lower():
                    if args.verbose:
                        print("  | Match found!")
                    file_matches.append(file_path)
                    break
    file.close()
    return


def print_matches():
    global file_matches
    for match in file_matches:
        print(match)
    return


def main():
    if args.verbose:
        print(f"Searching for \"{args.word}\" in \"{args.dir}\"")
    finder(args.dir)
    print_matches()


if __name__ == "__main__":
    main()