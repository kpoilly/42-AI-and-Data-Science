import sys
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from load_csv import load
matplotlib.use('gtk3agg')


def toNumber(num):
    if num.endswith("k"):
        return float(num[:-1]) * 1000
    elif num.endswith("M"):
        return float(num[:-1]) * 1000000
    elif num.endswith("B"):
        return float(num[:-1]) * 1000000000
    else:
        return float(num)


def main():
    dataset = load("population_total.csv")
    country1 = "France"
    country2 = "Belgium"

    try:
        country1_data = dataset[dataset["country"] == country1].iloc[0, 1:]
        country2_data = dataset[dataset["country"] == country2].iloc[0, 1:]
    except IndexError:
        print("Error.\nOne of the countrys is not in the dataset!",
              file=sys.stderr)
        exit()

    years = country1_data.index.astype(int)
    country1_data = [toNumber(num) for num in country1_data]
    country2_data = [toNumber(num) for num in country2_data]

    plt.figure()
    plt.plot(years, country1_data, linestyle='-', label=country1)
    plt.plot(years, country2_data, linestyle='-', label=country2)

    plt.title("Population Projections")
    plt.xlabel("Year")
    plt.xticks(range(1800, 2050, 40), range(1800, 2050, 40))
    plt.xlim(1790, 2060)
    plt.ylabel("Population")
    formatter = ticker.FuncFormatter(lambda y,
                                     pos: '{:,.0f}M'.format(y / 1000000))
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.grid(False)
    plt.legend()
    # plt.show()
    plt.savefig(f"{country1}_{country2}_population_projections.png")


if __name__ == "__main__":
    main()
