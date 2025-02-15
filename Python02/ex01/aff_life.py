import sys
import matplotlib
import matplotlib.pyplot as plt
from load_csv import load
matplotlib.use('gtk3agg')


def main():
    dataset = load("life_expectancy_years.csv")
    country = "France"

    try:
        country_data = dataset[dataset["country"] == country].iloc[0, 2:]
    except IndexError:
        print(f"Error.\n{country} is not in the dataset!",
              file=sys.stderr)
        exit()
    years = country_data.index.astype(int)
    life_expectancy = country_data.values.astype(float)

    plt.figure()
    plt.plot(years, life_expectancy, linestyle='-')

    plt.title(f"{country} Life expectancy Projections")
    plt.xlabel("Life expectancy")
    plt.ylabel("Year")
    plt.grid(False)
    # plt.show()
    plt.savefig(f"{country}_life_expectancy.png")


if __name__ == "__main__":
    main()
