import sys
import argparse
import numpy as np
from utils import load_data
from model import


def main():
    X = load_data("data/data_train.csv")
    if X is None:
        print("Error: Cannot found data_train.csv\nDid you separate the data file first?", file=sys.stderr)
        return 1

    parser = argparse.ArgumentParser(description="Model parameters")
    parser.add_argument('--layers', type=int, default=24, choices=range(0, 128), help="Numbers of neurons per layer")
    parser.add_argument('--epochs', type=int, default=100, choices=range(0, 10000), help="Numbers of epochs")
    parser.add_argument('--lr', type=float, default=0.01, choices=range(0, 1), help="Learning rate")
    parser.add_argument('--batch_size', type=int, default=32, choices={12, 24, 32, 64, 128}, help="Batch size")


if __name__ == "__main__":
    main()