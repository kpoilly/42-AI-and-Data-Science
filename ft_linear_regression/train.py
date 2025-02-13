import numpy as np
from sklearn.preprocessing import MinMaxScaler

def load_data(path):
	data = np.genfromtxt(path, delimiter=",", skip_header=1)
	return data

def estimate_price(mileage, theta0, theta1):
	return theta0 + (theta1 * mileage)

def train(data, learning_rate, iterations):
	m = len(data)
	theta0 = 0
	theta1 = 0

	scaler_x = MinMaxScaler()
	scaler_y = MinMaxScaler()
	norm_data = data.copy()
	norm_data[:, 0] = scaler_x.fit_transform(norm_data[:, 0].reshape(-1, 1)).flatten()
	norm_data[:, 1] = scaler_y.fit_transform(norm_data[:, 1].reshape(-1, 1)).flatten()

	for i in range(iterations):
		predictions = estimate_price(norm_data[:, 0], theta0, theta1)
		errors = predictions - norm_data[:, 1]

		err_theta0 = np.sum(errors)
		err_theta1 = np.sum(errors * norm_data[:, 0])

		theta0 = theta0 - learning_rate * (1/m) * err_theta0
		theta1 = theta1 - learning_rate * (1/m) * err_theta1

		print(f"\niter #{i}:\n\ntheta0: {theta0}\ntheta1: {theta1}")

	precision = get_precision(data, norm_data, theta0, theta1)
	theta0 = scaler_y.inverse_transform([[theta0]])[0][0]
	theta1 = theta1 * (scaler_y.scale_[0] / scaler_x.scale_[0])


	return theta0, theta1, norm_data, precision

def get_precision(data, norm_data, theta0, theta1):
	"""
	Calcul du R²
	"""

	predictions = estimate_price(norm_data[:, 0], theta0, theta1)
	squared_sum = np.sum((data[:, 1] - np.mean(data[:, 1]))**2)
	resid_sum =	np.sum((norm_data[:, 1] - predictions)**2)

	return 1 - (resid_sum / squared_sum)


def main():
	data = load_data("data.csv")

	learning_rate = 0.001
	iterations = 100

	theta0, theta1, norm_data, precision = train(data, learning_rate, iterations)

	with open("thetas.txt", "w") as thetas:
		thetas.write(f"{theta0}\n{theta1}")

	print(f"Model trained (lr: {learning_rate}, it: {iterations}).\nPrecision: {precision * 100}%")

if __name__ == "__main__":
    main()