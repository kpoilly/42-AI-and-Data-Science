import pandas as pd


def load(path: str) -> pd.array:
    if (".csv" not in path):
        return None
    try:
        dataset = pd.read_csv(path)
    except FileNotFoundError:
        return None
    print("Loading dataset of dimensions", dataset.shape)
    return dataset
