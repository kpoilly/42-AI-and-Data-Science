import sys

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression


TRAIN_SET_PATH = "../Train_knight.csv"


def variance_inflation_factor(df, index):
    """
    Our own variance_inflation_factor calculator
    based on a Linear Regression model
    """
    feature = df.columns[index]
    y = df[feature]
    X = df.drop(columns=[feature])

    if X.shape[1] < 1:
        return 1

    model = LinearRegression().fit(X, y)
    r_sq = model.score(X, y)

    return np.inf if r_sq == 1 else 1 / (1 - r_sq)


def calculate_VIF(df):
    """
    Calulates VIF and Tolerance of a given dataset
    """

    mapping = {'Jedi': 1, 'Sith': 0}
    df['knight_nb'] = df['knight'].map(mapping)
    X = df.drop(columns=['knight', 'knight_nb'])
    features = X.columns

    vif_data = pd.DataFrame()
    vif_data['Feature'] = X.columns
    vif_data['VIF'] = [variance_inflation_factor(X, i)
                       for i in range(len(features))]
    vif_data['Tolerance'] = 1 / vif_data['VIF']
    return vif_data


def main():
    try:
        df = pd.read_csv(TRAIN_SET_PATH, sep=',', header=0)
        print(f"\ndataset file '{TRAIN_SET_PATH}' loaded successfully.")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit()

    vifs = calculate_VIF(df)
    vifs = vifs.set_index("Feature")
    print(vifs)

    caped_vifs = vifs[vifs['VIF'] < 5].index.tolist()
    print("\nFeatures that the VIF goes under 5:\n", caped_vifs)


if __name__ == "__main__":
    main()
