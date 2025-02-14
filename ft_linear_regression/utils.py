import matplotlib.pyplot as plt
import numpy as np


def estimate_price(mileage, theta0, theta1):
    return theta0 + (theta1 * mileage)


def plot_prediction(data, theta0, theta1):
    plt.figure()

    plt.scatter(data[:, 0], data[:, 1], label="Original data")

    x_min = np.min(data[:, 0])
    x_max = np.max(data[:, 0])
    y_pred = estimate_price(np.array([x_min, x_max]), theta0, theta1)
    plt.plot([x_min, x_max], y_pred, color='red', label="Regression line")

    plt.title("Linear regression")
    plt.xlabel("Mileage")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    # plt.show() # Ne marche pas sur WSL, changer ça à l'ecole
    plt.savefig("plot_predict.png")
