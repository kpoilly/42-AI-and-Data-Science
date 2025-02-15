import matplotlib
import matplotlib.pyplot as plt
from load_csv import load
matplotlib.use('gtk3agg')


def main():
    dataset1 = load("life_expectancy_years.csv")
    dataset2 = load("income_per_person_gdppercapita_ppp\
_inflation_adjusted.csv")

    data1 = dataset1["1900"]
    data2 = dataset2["1900"]

    plt.figure()
    plt.scatter(data2, data1)

    plt.title("1900")
    plt.xlabel("Gross domestic product")
    plt.xscale("log")
    plt.xticks(ticks=[300, 1000, 10000], labels=['300', '1k', '10k'])
    plt.ylabel("Life Expectancy")
    plt.grid(False)
    # plt.show()
    plt.savefig("1900_projection_life.png")


if __name__ == "__main__":
    main()
