import sys
import argparse
import numpy as np
from utils import load_data, load_network, load_networks, normalize_data_spec, get_accuracy, one_hot, draw_comparison

def validate(X, network):
    validate_X = normalize_data_spec(X[:, 1:].astype(float), network.mean, network.std_dev)
    validate_y = X[:, 0].astype(float)
    
    inputs = validate_X
    for layer in network.network:
        layer.forward(inputs)
        layer.activation.forward(layer.output)
        inputs = layer.activation.output
        
    network.accuracy = get_accuracy(inputs, validate_y)
    print(f"Accuracy for Model #{network.id}: {round(network.accuracy, 4) * 100}%.")
        

def main():
    X = load_data("data/data_validation.csv")
    if X is None:
        print("Error: Cannot found data_validation.csv\nDid you separate the data file first?", file=sys.stderr)
        return 1
    else:
        print("data/data_validation.csv successfully loaded.\n")
    
    parser = argparse.ArgumentParser(description="Prediction parameters")
    parser.add_argument('--compare', action="store_true", help="Activate comparison between every previously trained models")
    args = parser.parse_args()
    
    if args.compare:
        networks = load_networks()
        print()
        for network in networks:
            validate(X, network)
        draw_comparison(networks, X[:, 0].astype(float).astype(int))
    else:
        network = load_network()
        if not network:
            return 1
        else:
            validate(X, network)

if __name__ == "__main__":
    main()