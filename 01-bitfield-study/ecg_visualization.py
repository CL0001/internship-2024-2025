"""
    Side script for visualizing a selected .npy or .csv ECG file.
    
    Usage:
        python ecg_visualization.py --file path/to/file
"""

"""
    The only interesting library here is argparse, which enables writing flags  
    and customizing their behavior when used.
"""
import argparse
import os
import numpy as np
import matplotlib.pyplot as plt


def make_graph(data, filename) -> None:
    plt.figure(figsize=(12, 6))
    plt.plot(data)
    plt.title(filename)
    plt.show()


parser = argparse.ArgumentParser()
parser.add_argument("--file", required=True)
args = parser.parse_args()

if not os.path.exists(args.file):
    print(f"can't open file {args.file}")
    os.exit()

if args.file.endswith(".npy"):
    npy_data = np.load(args.file)
    make_graph(npy_data, os.path.basename(args.file))
elif args.file.endswith(".csv"):
    csv_data = np.loadtxt(args.file, delimiter=',', dtype=str).tolist()
    new_data = []

    csv_data.pop(0)
    for i, value in enumerate(csv_data):
        new_data.append(int(csv_data[i][1]))

    make_graph(new_data, os.path.basename(args.file))
else:
    print("extension not supported")