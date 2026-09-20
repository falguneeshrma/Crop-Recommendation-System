import json
import os

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "Crop_recommendation.csv")
MODEL_DIR = os.path.join(HERE, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]


def main():
    df = pd.read_csv(CSV_PATH)
    X = df[FEATURES]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=0, shuffle=True, stratify=y
    )

    clf = DecisionTreeClassifier(criterion="entropy", random_state=0)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"test accuracy: {acc:.4f}")
    print(classification_report(y_test, preds))

    model_path = os.path.join(MODEL_DIR, "crop_model.joblib")
    joblib.dump(clf, model_path)

    with open(os.path.join(MODEL_DIR, "metadata.json"), "w") as f:
        json.dump(
            {"features": FEATURES, "accuracy": round(acc, 4), "classes": sorted(df["label"].unique().tolist())},
            f,
            indent=2,
        )

    print(f"saved model to {model_path}")


if __name__ == "__main__":
    main()
