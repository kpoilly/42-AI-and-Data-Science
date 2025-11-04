import sys

import pandas as pd
import matplotlib.pyplot as plt


DATASET_PATH = "../Train_knight.csv"


def draw_single(df):
    """
    Draw histogram of a file based on a single class (Knight in our case)
    """
    print("Generating Histrogram_single.jpg...")

    nb_cols = len(df.columns)
    nb_rows = (nb_cols) // 5

    fig, axes = plt.subplots(nrows=nb_rows, ncols=min(nb_cols, 5),
                             figsize=(15, 2.5 * nb_rows))
    axes = axes.flatten()

    for i, column in enumerate(df.columns):
        if i < len(axes):
            axes[i].hist(df[column], bins=40, color='darkseagreen',
                         label='Knight')
            axes[i].set_title(column)
            axes[i].legend(loc='upper right')

    plt.tight_layout()
    plt.savefig("Histrogram_single.jpg")
    print("Histrogram_single.jpg generated.")
    plt.close()


def draw_double(df):
    """
    Draw histogram of a file based on 2 classes (Jedi and Sith in our case)
    """
    print("Generating Histrogram_double.jpg...")

    graphs_name = [col for col in df.columns if col != 'knight']
    nb_cols = len(graphs_name)
    nb_rows = (nb_cols) // 5

    _, axes = plt.subplots(nrows=nb_rows, ncols=min(nb_cols, 5),
                             figsize=(15, 2.5 * nb_rows))
    axes = axes.flatten()

    for i, column in enumerate(df.columns):
        if i < len(axes):
            subset_jedi = df[df['knight'] == 'Jedi'][column]
            axes[i].hist(subset_jedi, bins=40, color='blue', alpha=0.5,
                         label='Jedi')

            subset_sith = df[df['knight'] == 'Sith'][column]
            axes[i].hist(subset_sith, bins=40, color='tomato', alpha=0.5,
                         label='Sith')

            axes[i].set_title(column)
            axes[i].legend()

    plt.tight_layout()
    plt.savefig("Histrogram_double.jpg")
    print("Histrogram_double.jpg generated.")
    plt.close()


def main():
    try:
        df = pd.read_csv(DATASET_PATH, sep=',', header=0)
        print(f"dataset file '{DATASET_PATH}' loaded successfully.")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit()

    draw_single(df)
    draw_double(df)


if __name__ == "__main__":
    main()
