"""
    Script designed to split larger data files into smaller pieces of 100MB.

    Usage:
        python file_splitter.py --file path/to/file --size 100
        (size is in megabytes; default is 100MB)
"""
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--file")
parser.add_argument("--size", type=int, default=100)
args = parser.parse_args()


def separate_file(file_path: str, size: int) -> None:
    with open(file_path, 'r') as file:
        file_counter = 1
        end_of_file = False

        while not end_of_file:
            with open(f"{file_path.split('.')[0]}-{file_counter}.{file_path.split('.')[1]}", 'w') as output_file:
                current_chunk_size = 0

                while True:
                    line = file.readline()
                    output_file.write(line)

                    if current_chunk_size >= size * 1000:
                        break

                    if '\n' not in line:
                        end_of_file = True
                        break

                    current_chunk_size += len(line)

            file_counter += 1


if __name__ == "__main__":
    separate_file(args.file, args.size)