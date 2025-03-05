import sys
import numpy as np
from utils import load_data, load_network, normalize_data_spec, get_accuracy, one_hot

def validate(X, network, mean, std_dev):
    validate_X = normalize_data_spec(X[:, 1:].astype(float), mean, std_dev)
    validate_y = X[:, 0].astype(float)
    
    inputs = validate_X
    for layer in network:
        layer.forward(inputs)
        layer.activation.forward(layer.output)
        inputs = layer.activation.output
        
    accuracy = get_accuracy(inputs, validate_y)
    print("Validation complete.")
    print(f"Accuracy: {round(accuracy, 4) * 100}%.")
        

def main():
    X = load_data("data/data_validation.csv")
    if X is None:
        print("Error: Cannot found data_validation.csv\nDid you separate the data file first?", file=sys.stderr)
        return 1
    else:
        print("data/data_validation.csv successfully loaded.\n")
    
    try:
        mean = np.load("save/mean.npy")
        std_dev = np.load("save/std_dev.npy")
        network = load_network()
    except FileNotFoundError:
        print("Model and/or normalization settings not found, be sure to train the model first.", file=sys.stderr)
        return 1
    
    validate(X, network, mean, std_dev)


if __name__ == "__main__":
    main()