import sys

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


TRAIN_SET_PATH = "../Train_knight.csv"


def main():
    try:
        df = pd.read_csv(TRAIN_SET_PATH, sep=',', header=0)
        print(f"\ndataset file '{TRAIN_SET_PATH}' loaded successfully.")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit()

    mapping = {'Jedi': 1, 'Sith': 0}
    df['knight_nb'] = df['knight'].map(mapping)
    df = df.drop(columns='knight')
    df = df.rename(columns={'knight_nb': 'knight'})

    correlations = df.corr()

    plt.figure(figsize=(12, 10))
    sns.heatmap(correlations, xticklabels=correlations.columns,
                yticklabels=correlations.columns)
    plt.tight_layout()
    plt.savefig("Heatmap.jpg")
    print("Heatmap saved as 'Heatmap.jpg'")


if __name__ == "__main__":
    main()
