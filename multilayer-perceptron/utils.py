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