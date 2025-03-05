import sys
import time
import argparse
import numpy as np
from utils import load_data, normalize_data, one_hot, save_network
from models import DenseLayer, ReLU, Softmax, CrossEntropy


def train(network, lr, batch_size, epochs, X):
    """
Model training using mini-batchs
    """
    
    print("Beginning training with following setting:")
    print(f"learning_rate: {lr}")
    print(f"batches of size: {batch_size}")
    print(f"number of epochs: {epochs}")
    print(f"loss function: CrossEntropy")
    print("")
    time.sleep(1)
    
    begin = time.time()
    loss_function = CrossEntropy()
    norm_X, mean, std_dev = normalize_data(X[:, 1:].astype(float))
    
    for epoch in range(epochs):
        batch_indexes = np.random.choice(len(norm_X), batch_size, replace=False)

        batch_X = norm_X[batch_indexes]
        batch_y = X[batch_indexes][:, 0].astype(float).astype(int)
        batch_y = one_hot(batch_y, 2)

        inputs = batch_X
        for layer in network:
            layer.forward(inputs)
            layer.activation.forward(layer.output)
            inputs = layer.activation.output

        loss = loss_function.calculate(inputs, batch_y)
        grad = loss_function.backward(inputs, batch_y)
        
        for layer in reversed(network):
            grad = layer.backward(grad, lr)
       
    print(f"Training ended in {time.time() - begin}s.")
    save_network(network)
    np.save("save/mean.npy", mean)
    np.save("save/std_dev.npy", std_dev)
            

def main():
    X = load_data("data/data_train.csv")
    if X is None:
        print("Error: Cannot found data_train.csv\nDid you separate the data file first?", file=sys.stderr)
        return 1
    else:
        print("data/data_train.csv successfully loaded.\n")

    parser = argparse.ArgumentParser(description="Training parameters")
    parser.add_argument('--layers', type=int, default=2, choices=range(0, 50), help="Number of layers between input and output layer")
    parser.add_argument('--layersW', type=int, default=16, choices=range(2, 256), help="Number of neurons per layers")
    parser.add_argument('--epochs', type=int, default=1000, choices=range(0, 10000), help="Number of epochs")
    parser.add_argument('--lr', type=float, default=0.001, choices=range(0, 10), help="Learning rate")
    parser.add_argument('--batch_size', type=int, default=32, choices={12, 24, 32, 64, 128}, help="Batch size")
    args = parser.parse_args()
    
    network = [DenseLayer(n_inputs=len(X[0])-1, n_neurons=args.layersW, activation=ReLU())] # input layer
    for i in range(0, args.layers):
        network.append(DenseLayer(n_inputs=args.layersW, n_neurons=args.layersW, activation=ReLU()))
    network.append(DenseLayer(n_inputs=args.layersW, n_neurons=2, activation=Softmax())) # output layer
    
    print("Network created with following configuration:")
    print(f"Input layer of {args.layersW} neurons, activation function: ReLU")
    print(f"{args.layers} layers of {args.layersW} neurons, activation function: ReLU")
    print(f"Output layer of 2 neurons, activation function: SoftMax")
    print("")
    time.sleep(1)
    
    train(network, args.lr, args.batch_size, args.epochs, X)


if __name__ == "__main__":
    main()