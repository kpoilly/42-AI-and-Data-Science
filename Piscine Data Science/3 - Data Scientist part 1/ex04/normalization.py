import sys

import pandas as pd
import matplotlib.pyplot as plt


TEST_SET_PATH = "../Test_knight.csv"
TRAIN_SET_PATH = "../Train_knight.csv"


def draw_scatter(df, x, y, single=False):
    """
    Draw scatter of a file based on a DataFrame
    """
    print(f"Generating {x}x{y}_{'single' if single else ''}.jpg...")
    plt.figure(figsize=(8, 6))

    if single:
        plt.scatter(df[x], df[y], label="Knight", alpha=0.5,
                    edgecolors='green', color='mediumseagreen')
    else:
        jedi_df = df[df['knight'] == 'Jedi']
        sith_df = df[df['knight'] == 'Sith']
        plt.scatter(jedi_df[x], jedi_df[y], label="Jedi", alpha=0.6,
                    edgecolors='blue', color='skyblue')
        plt.scatter(sith_df[x], sith_df[y], label="Sith", alpha=0.6,
                    edgecolors='red', color='salmon')

    plt.xlabel(x)
    plt.ylabel(y)
    plt.legend()
    plt.savefig(f"{x}x{y}_{'single' if single else ''}.jpg")


def normalize(df):
    """
    Normalize a DataFrame using min-max scaling
    """
    min_values = df.min()
    max_values = df.max()
    norm_df = (df - min_values) / (max_values - min_values)
    return norm_df


def main():
    try:
        df = pd.read_csv(TEST_SET_PATH, sep=',', header=0)
        print(f"\ndataset file '{TEST_SET_PATH}' loaded successfully.")

        print(f"Before norm:\n{df.head()}")
        df_norm = normalize(df)
        print(f"After norm:\n{df_norm.head()}")

        draw_scatter(df_norm, 'Empowered', 'Stims', single=True)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)

    try:
        df = pd.read_csv(TRAIN_SET_PATH, sep=',', header=0)
        print(f"\ndataset file '{TRAIN_SET_PATH}' loaded successfully.")

        print(f"Before norm:\n{df.head()}")
        df_norm = normalize(df.drop(columns='knight'))
        df_norm['knight'] = df['knight']
        print(f"After norm:\n{df_norm.head()}")

        draw_scatter(df_norm, 'Empowered', 'Stims')
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)


if __name__ == "__main__":
    main()
