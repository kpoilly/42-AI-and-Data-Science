import sys

import pandas as pd

from sklearn.model_selection import train_test_split


TRAIN_SET_PATH = "../Train_knight.csv"


def main():
    try:
        if float(sys.argv[1]) < 0 or float(sys.argv[1]) > 100:
            raise AssertionError("Invalid train_size argument.")
        train_size = float(sys.argv[1]) / 100
        df = pd.read_csv(TRAIN_SET_PATH, sep=",", header=0)
        print(f"\ndataset file '{TRAIN_SET_PATH}' loaded successfully.")

        X_train, X_validation = train_test_split(
            df, train_size=train_size, random_state=42
        )
        X_train.to_csv("Training_knight.csv", sep=",")
        print(
            f"{train_size * 100}% of the dataset has been saved at\
 Training_knight.csv."
        )
        X_validation.to_csv("Validation_knight.csv", sep=",")
        print(
            f"{100 - train_size * 100}% of the dataset has been saved at\
 Validation_knight.csv."
        )
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit()


if __name__ == "__main__":
    main()
