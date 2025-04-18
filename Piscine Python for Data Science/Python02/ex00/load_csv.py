import pandas as pd


def load(path: str) -> pd.array:
    """
    Loads a csv file and returns it as a panda DataFrame
    """
    if (".csv" not in path):
        return None
    try:
        dataset = pd.read_csv(path)
    except FileNotFoundError:
        return None
    print("Loading dataset of dimensions", dataset.shape)
    return dataset
