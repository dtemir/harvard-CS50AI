import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence, labels = [], []
    import calendar
    month_to_number = {name: num - 1 for num, name in enumerate(calendar.month_abbr) if num}

    with open(filename) as data:
        reader = csv.reader(data)
        next(reader)  # skip the fist line with attributes
        for row in reader:
            evidence.append([
                int(row[0]),    # Administrative
                float(row[1]),  # Administrative_Duration
                int(row[2]),    # Informational
                float(row[3]),  # Informational_Duration
                int(row[4]),    # ProductRelated
                float(row[5]),  # ProductRelated_Duration
                float(row[6]),  # BounceRates
                float(row[7]),  # ExitRates
                float(row[8]),  # PageValues
                float(row[9]),  # SpecialDay
                month_to_number[row[10][:3]],  # Month
                int(row[11]),   # OperatingSystems
                int(row[12]),   # Browser
                int(row[13]),   # Region
                int(row[14]),   # TrafficType
                1 if row[15] == 'Returning_Visitor' else 0,  # VisitorType
                int((row[16]) == 'TRUE'),   # Weekend
            ])

            labels.append(
                int(row[17] == 'TRUE')  # Revenue
            )

    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1) # train model with 1 neighbor
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity, specificity = 0.0, 0.0
    positive, negative = 0.0, 0.0

    for label, prediction in zip(labels, predictions):
        if label == 1:  # if label is positive, then we calculate sensitivity (positive rate)
            positive += 1
            if label == prediction:
                sensitivity += 1

        else:  # if label is negative, then we calculate specificity (negative rate)
            negative += 1
            if label == prediction:
                specificity += 1

    sensitivity /= positive
    specificity /= negative

    return sensitivity, specificity


if __name__ == "__main__":
    main()
