import pandas as pd


def load(path: str) -> pd.array:
    try:
        dataset = pd.read_csv(path)
    except FileNotFoundError:
        raise AssertionError(f"{path} could not be loaded.\
 (is path correct ?)")
    print("Loading dataset of dimensions", dataset.shape)
    return dataset
