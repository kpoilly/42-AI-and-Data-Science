from utils import load_data


def main():
    X, res = load_data("data_validation.csv")
    if X is None:
        print("Error: Cannot found data_validation.csv\nDid you separate the data file first?", file=sys.stderr)
        return 1


if __name__ == "__main__":
    main()