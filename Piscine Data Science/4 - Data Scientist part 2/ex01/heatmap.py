import sys
import seaborn as sns
import matplotlib.pyplot as plt
from load_csv import load


def main():
    try:
        df = load("../Train_knight.csv")
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


if __name__ == "__main__":
    main()
