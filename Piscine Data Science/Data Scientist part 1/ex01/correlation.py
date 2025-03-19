import sys
import pandas as pd
from load_csv import load
from scipy.stats import pointbiserialr


def correl_factors(path):
    try:
        df = load(path)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit()

    features = [col for col in df.columns if col != 'knight']
    mapping = {'Jedi': 1, 'Sith': 0}
    df['knight_nb'] = df['knight'].map(mapping)

    correl_factors = {}
    for feature in features:
        correlation, _ = pointbiserialr(df['knight_nb'], df[feature])
        correl_factors[feature] = correlation

    correlations = pd.Series(correl_factors).sort_values(key=abs,
                                                         ascending=False)
    return correlations


def main():
    print(correl_factors("Train_knight.csv"))


if __name__ == "__main__":
    main()
