import numpy as np
import matplotlib

def load_data(path):
    """
    Load the dataset into a NumPy array.
    """
    try:
        data = np.genfromtxt(path, delimiter=",", dtype=str)
        results = data[:, 1]
        data = data[:, 2:].astype(float)
        results = np.where(results == "M", 1, 0)
        return data, results
    
    except FileNotFoundError:
        return None, None
    except IsADirectoryError:
        return None, None
    
def normalize_data(data):
    """
    Normalize the dataset
    """
    mean = np.mean(data, axis=0)
    std_dev = np.std(data, axis=0)
    norm_data = (data - mean) / std_dev
    return norm_data, mean, std_dev