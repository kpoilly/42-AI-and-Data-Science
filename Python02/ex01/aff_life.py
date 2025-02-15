import matplotlib
import matplotlib.pyplot as plt
from load_csv import load
matplotlib.use('gtk3agg')


def main():
    dataset = load("life_expectancy_years.csv")
    country = "France"

    plt.figure()
    plt.scatter(dataset[:, 1:])
    plt.title(f"{country} Life expectancy Projections")
    plt.xlabel("Life expectancy")
    plt.ylabel("Year")
    plt.legend()
    plt.grid(False)
    # plt.show()
    plt.savefig(f"{country}_life_expectancy.png")


if __name__ == "__main__":
    main()
