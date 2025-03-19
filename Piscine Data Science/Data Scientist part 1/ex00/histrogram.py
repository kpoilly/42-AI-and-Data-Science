import sys
import matplotlib.pyplot as plt

from load_csv import load


def draw_single(path):
    """
    Draw histogram of a file based on a single class (Knight in our case)
    """
    try:
        df = load(path)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit()

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


def draw_double(path):
    """
    Draw histogram of a file based on 2 classes (Jedi and Sith in our case)
    """
    try:
        df = load(path)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit()

    graphs_name = [col for col in df.columns if col != 'knight']
    nb_cols = len(graphs_name)
    nb_rows = (nb_cols) // 5

    fig, axes = plt.subplots(nrows=nb_rows, ncols=min(nb_cols, 5),
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


def main():
    draw_single("Test_knight.csv")
    draw_double("Train_knight.csv")


if __name__ == "__main__":
    main()
