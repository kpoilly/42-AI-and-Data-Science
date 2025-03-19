import sys
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
from load_csv import load


def predict(path_train, path_val):
    """
    Uses DecisionTreeClassifier
    Prints F1-Score (Needs to be >90%)
    Display the tree in a graph.jpg
    Predictions in tree.txt
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

    # Model training
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)

    # F1 Calculation
    prediction = model.predict(X_val)
    f1 = f1_score(y_val, prediction)
    print(f"F1-score on data_validation : {round(f1, 5) * 100}%")

    # Display tree in a graph
    plt.figure(figsize=(12, 8))
    plot_tree(model, feature_names=X_train.columns,
              class_names=['Sith', 'Jedi'], filled=True)
    plt.savefig("graph.jpg")
    print("Tree displayed in 'graph.jpg'")

    # Tree.txt file
    reverse_mapping = {1: 'Jedi', 0: 'Sith'}
    prediction = [reverse_mapping[pred] for pred in prediction]
    with open("Tree.txt", "w") as f:
        for pred in prediction:
            f.write(f"{pred}\n")
    print("'Tree.txt' created")


def main():
    predict("data_train.csv", "data_validation.csv")


if __name__ == "__main__":
    main()
