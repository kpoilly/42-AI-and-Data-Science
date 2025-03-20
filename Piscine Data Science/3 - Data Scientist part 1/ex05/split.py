import sys
from load_csv import load
from sklearn.model_selection import train_test_split


def main():
    try:
        if float(sys.argv[2]) < 0 or float(sys.argv[2]) > 100:
            raise AssertionError("Invalid train_size argument.")
        train_size = float(sys.argv[2]) / 100
        df = load(sys.argv[1])
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit()

    X_train, X_validation = train_test_split(df, train_size=train_size,
                                             random_state=42)
    X_train.to_csv("Training_knight.csv", sep=',')
    print(f"{train_size * 100}% of the dataset has been saved at\
 Training_knight.csv.")
    X_validation.to_csv("Validation_knight.csv", sep=',')
    print(f"{100 - train_size * 100}% of the dataset has been saved at\
 Validation_knight.csv.")


if __name__ == "__main__":
    main()
