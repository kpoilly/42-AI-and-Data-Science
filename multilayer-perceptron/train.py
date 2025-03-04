import sys
import argparse
import numpy as np
from utils import load_data
from models import DenseLayer, ReLU, Softmax, BinaryCrossEntropy


def train(network, lr, batch_size, epochs, X):
    """
Model training using mini-batchs
    """
    
    loss_function = BinaryCrossEntropy()
    
    for epoch in range(epochs):
        batch_indexes = np.random.choice(len(X), batch_size, replace=False)
        batch = X[batch_indexes]
        
        inputs = batch[:, 1:].astype(float)
        labels = batch[:, 0].astype(float).astype(int)

        for layer in network:
            layer.forward(inputs)
            layer.activation.forward(layer.output)
            inputs = layer.output
        
        loss = loss_function.calculate(inputs, labels)
            

def main():
    X = load_data("data/data_train.csv")
    if X is None:
        print("Error: Cannot found data_train.csv\nDid you separate the data file first?", file=sys.stderr)
        return 1

    parser = argparse.ArgumentParser(description="Training parameters")
    parser.add_argument('--layers', type=int, default=2, choices=range(0, 50), help="Number of layers between input and output layer")
    parser.add_argument('--layersW', type=int, default=16, choices=range(2, 256), help="Number of neurons per layers")
    parser.add_argument('--epochs', type=int, default=1000, choices=range(0, 10000), help="Number of epochs")
    parser.add_argument('--lr', type=float, default=0.01, choices=range(0, 10), help="Learning rate")
    parser.add_argument('--batch_size', type=int, default=32, choices={12, 24, 32, 64, 128}, help="Batch size")
    args = parser.parse_args()
    
    network = [DenseLayer(n_inputs=len(X[0])-1, n_neurons=args.layersW, activation=ReLU())] # input layer
    for i in range(0, args.layers):
        network.append(DenseLayer(n_inputs=args.layersW, n_neurons=args.layersW, activation=ReLU()))
    network.append(DenseLayer(n_inputs=args.layersW, n_neurons=1, activation=Softmax())) # output layer
    
    train(network, args.lr, args.batch_size, args.epochs, X)


if __name__ == "__main__":
    main()