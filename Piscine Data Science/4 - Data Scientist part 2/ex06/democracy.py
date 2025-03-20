import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score
from load_csv import load


def predict(path_train, path_val):
    """
    Uses VotingClassifier
    Voters:
        RandomForestClassifier
        KNeighborsClassifier
        LogisticRegression
    Prints F1-Score (Needs to be >94%)
    Predictions in Voting.txt
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
    LOG = LogisticRegression(random_state=42)
    RFC = RandomForestClassifier(random_state=42)
    KNN = KNeighborsClassifier(n_neighbors=2)

    LOG.fit(X_train, y_train)
    RFC.fit(X_train, y_train)
    KNN.fit(X_train, y_train)

    model = VotingClassifier(estimators=[('lr', LOG), ('rf', RFC),
                                         ('knn', KNN)], voting='hard')
    model.fit(X_train, y_train)

    # F1 Calculation
    prediction = model.predict(X_val)
    f1 = f1_score(y_val, prediction)
    print(f"F1-score on data_validation : {round(f1, 5) * 100}%")

    # Tree.txt file
    reverse_mapping = {1: 'Jedi', 0: 'Sith'}
    prediction = [reverse_mapping[pred] for pred in prediction]
    with open("Voting.txt", "w") as f:
        for pred in prediction:
            f.write(f"{pred}\n")
    print("'Voting.txt' created")


def main():
    predict("../data_train.csv", "../data_validation.csv")


if __name__ == "__main__":
    main()
