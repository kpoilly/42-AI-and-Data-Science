from utils import load_network, normalize_data_spec
import numpy as np


def validate(X, network):
    validate_X = normalize_data_spec(X[1:].astype(float), network.mean, network.std_dev)
    validate_y = X[0].astype(float)

    inputs = validate_X
    for layer in network.network:
        layer.forward(inputs)
        layer.activation.forward(layer.output)
        inputs = layer.activation.output

    print(f"result have {round(inputs[0][0] * 100, 2)}% chance to be 0 and {round(inputs[0][1] * 100, 2)}% chance to be 1.\nfinal verdict: {np.argmax(inputs)}.")


def main():
	network = load_network()
	# X = np.array([1.0,14.6,23.29,93.97,664.7,0.08682,0.06636,0.0839,0.05271,0.1627,0.05416,0.4157,1.627,2.914,33.01,0.008312,0.01742,0.03389,0.01576,0.0174,0.002871,15.79,31.71,102.2,758.2,0.1312,0.1581,0.2675,0.1359,0.2477,0.06836])
	X = np.array([0.0,11.89,17.36,76.2,435.6,0.1225,0.0721,0.05929,0.07404,0.2015,0.05875,0.6412,2.293,4.021,48.84,0.01418,0.01489,0.01267,0.0191,0.02678,0.003002,12.4,18.99,79.46,472.4,0.1359,0.08368,0.07153,0.08946,0.222,0.06033])
	validate(X, network)


if __name__ == "__main__":
    main()