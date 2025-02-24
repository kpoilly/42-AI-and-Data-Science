import sys
import math
import argparse
import numpy as np
from utils import load_data
from model import DenseLayer


def train(network, lr, batch_size, epochs, X):
    batch_indexes = np.random.permutation(batch_size)
    
    for epoch in range(epochs):
        
        for batch in batch_indexes:
            batch_X = X[batch]
            print(batch_X)


def main():
    X = load_data("data/data_train.csv")
    if X is None:
        print("Error: Cannot found data_train.csv\nDid you separate the data file first?", file=sys.stderr)
        return 1

    parser = argparse.ArgumentParser(description="Training parameters")
    parser.add_argument('--layers', type=int, default=2, choices=range(0, 50), help="Numbers of hidden layers between input and output layer")
    parser.add_argument('--epochs', type=int, default=100, choices=range(0, 10000), help="Numbers of epochs")
    parser.add_argument('--lr', type=float, default=0.01, choices=range(0, 10), help="Learning rate")
    parser.add_argument('--batch_size', type=int, default=32, choices={12, 24, 32, 64, 128}, help="Batch size")
    args = parser.parse_args()
    
    network = [DenseLayer(X.shape[0], 12)] # input layer
    for i in range(0, args.layers):
        network.append(DenseLayer(12, 12))
    network.append(DenseLayer(12, 2)) # output layer
    
    train(network, args.lr, args.batch_size, args.epochs, X)


if __name__ == "__main__":
    main()