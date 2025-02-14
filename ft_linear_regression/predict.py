import sys
from train import estimate_price


def load_thetas(path):
    """
    Load the file containing the thetas after training
    and use them to predict prices
    """
    try:
        with open(path, "r") as thetas:
            theta0 = float(thetas.readline())
            theta1 = float(thetas.readline())
            return theta0, theta1
    except FileNotFoundError:
        print(f"Error.\nFile '{path}' not found.\
 Make sure to train the model first!", file=sys.stderr)
        exit()


def main():
    theta0, theta1 = load_thetas("thetas.txt")
    user_input = None
    while (user_input is None):
        user_input = input("Enter mileage: ")
        if (user_input == "q"):
            break
        try:
            mileage = float(user_input)
            print(f"Estimated price: \
{estimate_price(mileage, theta0, theta1)}")
            user_input = None
        except ValueError:
            user_input = None


if __name__ == "__main__":
    main()
