import sys
import time
import argparse
import numpy as np
from utils import load_data, normalize_data, normalize_data_spec, one_hot, save_network, get_val_loss
from models import DenseLayer, ReLU, Softmax, CrossEntropy


def train(network, lr, batch_size, epochs, X, val_X, patience):
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
    
    val_y = val_X[:, 0].astype(float).astype(int)
    val_X = normalize_data_spec(val_X[:, 1:].astype(float), mean, std_dev)
    best_val_loss = float('inf')
    epochs_without_impr = 0
    
    for epoch in range(epochs):
        batch_indexes = np.random.choice(len(norm_X), batch_size, replace=False)

        batch_X = norm_X[batch_indexes]
        batch_y = X[batch_indexes][:, 0].astype(float).astype(int)
        batch_y = one_hot(batch_y, 2)

        #Forwardpropagation
        inputs = batch_X
        for layer in network:
            layer.forward(inputs)
            layer.activation.forward(layer.output)
            inputs = layer.activation.output
            
        #Backpropagation
        loss = loss_function.calculate(inputs, batch_y)
        grad = loss_function.backward(inputs, batch_y)
        
        for layer in reversed(network):
            grad = layer.backward(grad, lr)
            
        #Validation
        val_loss = get_val_loss(network, val_X, val_y, loss_function)
        
        if round(val_loss, 5) < best_val_loss:
            best_val_loss = round(val_loss, 5)
            epochs_without_impr = 0
        else:
            epochs_without_impr += 1
            
        if epochs_without_impr >= patience:
            print(f"Early stopping after {epoch + 1} epochs. ({time.time() - begin}s.)")
            break
        
        print(f"epoch {epoch + 1}/{epochs} - loss: {loss} - val_loss: {val_loss}")
       
    print(f"\nTraining ended in {time.time() - begin}s.")
    save_network(network)
    np.save("save/mean.npy", mean)
    np.save("save/std_dev.npy", std_dev)
            

def main():
    X = load_data("data/data_train.csv")
    if X is None:
        print("Error: Cannot found data/data_train.csv\nDid you separate the data file first?", file=sys.stderr)
        return 1
    else:
        print("data/data_train.csv successfully loaded.\n")
        
    val_X = load_data("data/data_validation.csv")
    if val_X is None:
        print("Error: Cannot found data/data_validation.csv\nDid you separate the data file first?", file=sys.stderr)
        return 1
    else:
        print("data/data_validation.csv successfully loaded.\n")

    parser = argparse.ArgumentParser(description="Training parameters")
    parser.add_argument('--layers', type=int, default=2, choices=range(0, 128), help="Number of layers between input and output layer")
    parser.add_argument('--layersW', type=int, default=16, choices=range(2, 256), help="Number of neurons per layers")
    parser.add_argument('--epochs', type=int, default=1000, choices=range(0, 100001), help="Number of epochs")
    parser.add_argument('--lr', type=float, default=0.001, choices=range(0, 10), help="Learning rate")
    parser.add_argument('--batch_size', type=int, default=32, choices={12, 24, 32, 64, 128}, help="Batch size")
    parser.add_argument('--patience', type=int, default=5, choices=range(0, 100), help="Number of epochs without improvement tolerated (early stopping)")
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
    
    train(network, args.lr, args.batch_size, args.epochs, X, val_X, args.patience)


if __name__ == "__main__":
    main()