import sys
import matplotlib.pyplot as plt

from load_csv import load


def draw_scatter(path, x, y, single=False):
    """
    Draw scatter of a file based on a single class (Knight in our case)
    """
    try:
        df = load(path)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit()

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


def main():
    draw_scatter("../Test_knight.csv", 'Empowered', 'Stims', single=True)
    draw_scatter("../Test_knight.csv", 'Push', 'Deflection', single=True)

    draw_scatter("../Train_knight.csv", 'Empowered', 'Stims')
    draw_scatter("../Train_knight.csv", 'Push', 'Deflection')


if __name__ == "__main__":
    main()
