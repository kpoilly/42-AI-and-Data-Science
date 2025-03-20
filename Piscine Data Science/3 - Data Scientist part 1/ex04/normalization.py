import sys
import matplotlib.pyplot as plt

from load_csv import load


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
        df = load("../Test_knight.csv")
        df2 = load("../Train_knight.csv")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit()

    print(f"Before norm:\n{df.head()}")
    df_norm = normalize(df)
    print(f"After norm:\n{df_norm.head()}")
    df2_norm = normalize(df2.drop(columns='knight'))
    df2_norm['knight'] = df2['knight']

    draw_scatter(df_norm, 'Empowered', 'Stims', single=True)
    draw_scatter(df2_norm, 'Empowered', 'Stims')


if __name__ == "__main__":
    main()
