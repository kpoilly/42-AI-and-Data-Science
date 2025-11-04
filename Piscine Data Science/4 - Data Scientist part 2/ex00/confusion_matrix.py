import sys

import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt


def main():
    with open('../predictions.txt', 'r') as f:
        predictions = [line.strip() for line in f.readlines()]
    with open('../truth.txt', 'r') as f:
        truths = [line.strip() for line in f.readlines()]

    if len(predictions) != len(truths):
        print("Error: predictions length and truths length mismatch",
              file=sys.stderr)
        return

    TP, TN, FP, FN = 0, 0, 0, 0

    for i in range(len(truths)):
        pred = predictions[i]
        truth = truths[i]

        if truth == 'Jedi' and pred == truth:
            TP += 1
        elif truth == 'Sith' and pred == truth:
            TN += 1
        elif truth == 'Jedi' and pred != truth:
            FN += 1
        elif truth == 'Sith' and pred != truth:
            FP += 1

    precision_jedi = TP / (TP + FP)
    precision_sith = TN / (TN + FN)

    recall_jedi = TP / (TP + FN)
    recall_sith = TN / (TN + FP)

    f1_jedi = 2 * (precision_jedi * recall_jedi) / \
        (precision_jedi + recall_jedi)
    f1_sith = 2 * (precision_sith * recall_sith) / \
        (precision_sith + recall_sith)

    total_jedi = sum(1 for truth in truths if truth == 'Jedi')
    total_sith = sum(1 for truth in truths if truth == 'Sith')

    accuracy = (TP + TN) / len(truths)

    print(f"{'':<5} {'precision':<13} {'recall':<8} \
{'f1-score':<11} {'total'}\n")
    print(f"{'Jedi':<10} {precision_jedi:<10.2f} \
{recall_jedi:<10.2f} {f1_jedi:<10.2f} {total_jedi}")
    print(f"{'Sith':<10} {precision_sith:<10.2f} \
{recall_sith:<10.2f} {f1_sith:<10.2f} {total_sith}")
    print(f"\n{'accuracy':<10} {'':<10} {'':<10} {accuracy:<10.2f} 100\n")

    conf_matrix = np.array([[TP, FN], [FP, TN]])
    print(conf_matrix)

    plt.figure(figsize=(6, 4))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='viridis',
                xticklabels=['Jedi', 'Sith'], yticklabels=['Jedi', 'Sith'],
                annot_kws={"size": 20})
    plt.title('Confusion Matrix')
    plt.ylabel('Truth')
    plt.xlabel('Prediction')
    plt.tight_layout()
    plt.savefig('confusion_matrix.jpg')
    print("Confusion matrix saved as 'confusion_matrix.jpg'")


if __name__ == "__main__":
    main()
