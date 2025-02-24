import numpy as np
import matplotlib
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