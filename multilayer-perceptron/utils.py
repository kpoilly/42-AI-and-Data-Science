import numpy as np
import matplotlib
import pickle
from sklearn.model_selection import train_test_split


def load_data(path):
    """
    Load the dataset into a NumPy array.
    """
    try:
        data = np.genfromtxt(path, delimiter=",", dtype=str)
        return data
    
    except FileNotFoundError:
        return None
    except IsADirectoryError:
        return None
    
def normalize_data(data):
    """
    Normalize the dataset
    """
    mean = np.mean(data, axis=0)
    std_dev = np.std(data, axis=0)
    norm_data = (data - mean) / std_dev
    return norm_data, mean, std_dev

def normalize_data_spec(data, mean, std_dev):
    """
    Normalize the dataset
    """
    norm_data = (data - mean) / std_dev
    return norm_data

def one_hot(y_true, n_outputs):
    one_hot = np.zeros((len(y_true), n_outputs))
    one_hot[np.arange(len(y_true)), y_true] = 1
    return one_hot

def save_network(network):
    with open("save/model.pkl", "wb") as f:
        pickle.dump(network, f)
    print("Network successfully saved in save/model.pkl.")
    
def load_network():
    with open("save/model.pkl", "rb") as f:
        network = pickle.load(f)
    print("Network successfully loaded.")
    return network

def get_accuracy(predictions, y_true):
    """
    Calculate the accuracy of the model.

    Args:
        predictions (np.array): predictions done by the model.
        y_true (np.array): "true" value, what the model is supposed to predict.

    Returns:
        float: accuracy of the model
    """
    predicted_classes = np.argmax(predictions, axis=1)
    correct_predictions = np.sum(predicted_classes == y_true)
    accuracy = correct_predictions / len(y_true)
    return accuracy

def get_val_loss(network, val_X, val_y, loss_function):
    val_y = one_hot(val_y, 2)
    
    inputs = val_X
    for layer in network:
        layer.forward(inputs)
        layer.activation.forward(layer.output)
        inputs = layer.activation.output
    
    val_loss = loss_function.calculate(inputs, val_y)
    return np.mean(val_loss)
    