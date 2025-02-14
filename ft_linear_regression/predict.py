import sys
from train import estimate_price


def load_thetas(path):
    try:
        with open(path, "r") as thetas:
            theta0 = float(thetas.readline())
            theta1 = float(thetas.readline())
            return theta0, theta1
    except FileNotFoundError:
        print(f"Error.\nFile '{path}' not found. Make sure to train the model first!\n", file=sys.stderr)
        exit()


def main():
    theta0, theta1 = load_thetas("thetas.txt")
    user_input = None
    while (user_input is None):
        user_input = input("Enter mileage: ")
        try:
            mileage = float(user_input)
        except ValueError:
            user_input = None

    print(f"Estimated price:  {estimate_price(mileage, theta0, theta1)}")


if __name__ == "__main__":
    main()
