import sys
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, precision_score
from load_csv import load


def predict(path_train, path_val):
    """
    Uses KNN
    Prints F1-Score (Needs to be >92%)
    Display the graph in a graph.jpg
    Predictions in KNN.txt
    """
    try:
        df_train = load(path_train)
        df_val = load(path_val)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        exit()

    # Data prep
    mapping = {'Jedi': 1, 'Sith': 0}
    y_train = df_train['knight'].map(mapping)
    X_train = df_train.drop(columns=['knight'])
    y_val = df_val['knight'].map(mapping)
    X_val = df_val.drop(columns=['knight'])

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)

    # Model training
    precision_scores = {}
    k_values = range(1, 31)

    for k in k_values:
        model = KNeighborsClassifier(n_neighbors=k)
        model.fit(X_train, y_train)
        prediction = model.predict(X_val)
        precision = precision_score(y_val, prediction)
        precision_scores[k] = precision

    best_k = max(precision_scores, key=precision_scores.get)
    model = KNeighborsClassifier(n_neighbors=best_k)
    model.fit(X_train, y_train)

    # F1 Calculation
    prediction = model.predict(X_val)
    f1 = f1_score(y_val, prediction)
    print(f"F1-score on data_validation : {round(f1, 5) * 100}%")

    # Display tree in a graph
    plt.figure(figsize=(10, 6))
    plt.plot(list(precision_scores.keys()),
             list(precision_scores.values()), marker='')
    plt.xlabel('K Values')
    plt.ylabel('Accuracy (%)')
    plt.grid(True)
    plt.savefig("graph.jpg")
    print("Graph displayed in 'graph.jpg'")

    # Tree.txt file
    reverse_mapping = {1: 'Jedi', 0: 'Sith'}
    prediction = [reverse_mapping[pred] for pred in prediction]
    with open("KNN.txt", "w") as f:
        for pred in prediction:
            f.write(f"{pred}\n")
    print("'KNN.txt' created")


def main():
    predict("../data_train.csv", "../data_validation.csv")


if __name__ == "__main__":
    main()
