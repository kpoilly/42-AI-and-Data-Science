import sys

import pandas as pd

from scipy.stats import pointbiserialr


DATASET_PATH = "../Train_knight.csv"


def correl_factors(df):
    """
    Calulates correlation factor of a given dataset
    """
    features = [col for col in df.columns if col != 'knight']
    mapping = {'Jedi': 1, 'Sith': 0}
    df['knight_nb'] = df['knight'].map(mapping)

    correl_factors = {}
    for feature in features:
        correlation, _ = pointbiserialr(df[feature], df['knight_nb'])
        correl_factors[feature] = abs(correlation)

    correlations = pd.Series(correl_factors).sort_values(key=abs,
                                                         ascending=False)
    return correlations


def main():
    try:
        df = pd.read_csv(DATASET_PATH, sep=',', header=0)
        print(f"\ndataset file '{DATASET_PATH}' loaded successfully.")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit()

    print(correl_factors(df))


if __name__ == "__main__":
    main()
