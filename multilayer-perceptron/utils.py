import os
import re
import numpy as np
import matplotlib.pyplot as plt
import pickle
import datetime
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
    files = os.listdir("models")
    model_files = [f for f in files if re.match(r"model#\d+\.pkl", f)]
    network.id = len(model_files) + 1
    
    with open(f"models/model#{network.id}.pkl", "wb") as f:
        pickle.dump(network, f)
    print(f"Network successfully saved in models/model#{network.id}.pkl.")
    
def load_network():
    nb_model = None
    while (nb_model is None):
        nb_model = input("Model number: ")
        if (nb_model == "q"):
            return None
        try:
            print(f"Loading model#{nb_model}...")
            with open(f"models/model#{nb_model}.pkl", "rb") as f:
                network = pickle.load(f)
            print(f"model#{nb_model} successfully loaded.\n")
        except FileNotFoundError:
            print(f"Error: Couldn't load model#{nb_model}.\n")
            nb_model = None
    
    return network

def load_networks():
    networks = []
    
    files = os.listdir("models")
    model_files = [f for f in files if re.match(r"model#\d+\.pkl", f)]
    for model in model_files:
        with open(f"models/{model}", "rb") as f:
            networks.append(pickle.load(f))
            print(f"{model} successfully loaded.")
    
    return networks
        

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
    oh_val_y = one_hot(val_y, 2)
    
    inputs = val_X
    for layer in network:
        layer.forward(inputs)
        layer.activation.forward(layer.output)
        inputs = layer.activation.output
    
    val_loss = loss_function.calculate(inputs, oh_val_y)
    return np.mean(val_loss), get_accuracy(inputs, val_y)

def draw_loss(network):
    plt.clf()
    plt.plot(network.train_losses, label="Training loss")
    plt.plot(network.val_losses, label="Validation loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.title("Training and Validation loss")
    plt.legend()
    plt.text(0.05, 0.05, network.params, transform=plt.gca().transAxes, fontsize=10, verticalalignment='bottom')
    plt.savefig(f"visuals/model#{network.id}_loss.png")
    
def draw_accu(network):
    plt.clf()
    plt.plot(network.train_accu, label="Training accuracy")
    plt.plot(network.val_accu, label="Validation accuracy")
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.title("Training and Validation accuracy")
    plt.legend()
    plt.text(0.05, 0.05, network.params, transform=plt.gca().transAxes, fontsize=10, verticalalignment='bottom')
    plt.savefig(f"visuals/model#{network.id}_accuracy.png")
    