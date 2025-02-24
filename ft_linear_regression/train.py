import numpy as np
from utils import estimate_price, plot_prediction


def load_data(path):
    """
    Load the dataset
    """
    try:
        data = np.genfromtxt(path, delimiter=",", skip_header=1)
        return data
    except FileNotFoundError:
        return None


def normalize_data(data):
    """
    Normalize the dataset
    """
    mean = np.mean(data, axis=0)
    std_dev = np.std(data, axis=0)
    norm_data = (data - mean) / std_dev
    return norm_data, mean, std_dev


def train(data, learning_rate, iterations):
    """
    Train the model on a normalized dataset
    using the formulas given by the subject
    """
    m = len(data)
    theta0 = 0
    theta1 = 0
    norm_data, mean_data, std_dev_data = normalize_data(data)

    for i in range(iterations):
        predictions = estimate_price(norm_data[:, 0], theta0, theta1)
        errors = predictions - norm_data[:, 1]

        err_theta0 = np.sum(errors)
        err_theta1 = np.sum(errors * norm_data[:, 0])

        theta0 = theta0 - learning_rate * err_theta0 / m
        theta1 = theta1 - learning_rate * err_theta1 / m

        if (i % (iterations / 10) == 0):
            print(f"iter #{i}:\ntheta0: {theta0}\ntheta1: {theta1}\n")

    accuracy = get_accuracy(data, norm_data, theta0, theta1)
    theta0 = theta0 * std_dev_data[1] + mean_data[1] \
        - (theta1 * mean_data[0] * std_dev_data[1]) / std_dev_data[0]
    theta1 = theta1 * (std_dev_data[1] / std_dev_data[0])

    return theta0, theta1, accuracy


def get_accuracy(data, norm_data, theta0, theta1):
    """
    Calcul du R²
    """
    predictions = estimate_price(norm_data[:, 0], theta0, theta1)
    squared_sum = np.sum((data[:, 1] - np.mean(data[:, 1]))**2)
    resid_sum = np.sum((norm_data[:, 1] - predictions)**2)

    return 1 - (resid_sum / squared_sum)


def main():
    data = load_data("data.csv")
    if data is None:
        print("Error: dataset not found.")
        return 1

    learning_rate = 0.01
    iterations = 1000

    theta0, theta1, accuracy = train(data, learning_rate, iterations)

    with open("thetas.txt", "w") as thetas:
        thetas.write(f"{theta0}\n{theta1}")

    print(f"Model trained (lr: {learning_rate}, it: {iterations}).\
          \naccuracy: {accuracy * 100}%")
    plot_prediction(data, theta0, theta1)


if __name__ == "__main__":
    main()
