import sys
import numpy as np
import matplotlib.pyplot as plt

from load_csv import load
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def variances(path):
    try:
        df = load(path)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit()

    mapping = {'Jedi': 1, 'Sith': 0}
    df['knight_nb'] = df['knight'].map(mapping)
    df = df.drop(columns='knight')
    df = df.rename(columns={'knight_nb': 'knight'})

    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)

    pca = PCA(n_components=len(df.columns))
    pca.fit(df_scaled)

    var = pca.explained_variance_ratio_
    cumul_var = np.cumsum(var)

    return var, cumul_var * 100


def main():
    var, cumul_var = variances("../Train_knight.csv")
    print(f"\nVariances (Percentage):\n{var}\n")
    print(f"Cumulative Variances (Percentage):\n{cumul_var}")

    plt.figure(figsize=(8, 6))
    plt.plot(range(1, len(cumul_var) + 1), cumul_var, marker='', linestyle='-')
    plt.title("Cumulative Explained Variance")
    plt.ylabel("Explained variance (%)")
    plt.xlabel("Number of components")
    plt.savefig("cumulative_variance.jpg")


if __name__ == "__main__":
    main()
