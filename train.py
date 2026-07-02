# ==========================================================
# Credit Card Approval Prediction System
# train.py (Part 1)
# ==========================================================

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

import joblib

# ==========================================================
# LOAD DATASETS
# ==========================================================

print("=" * 60)
print("Loading datasets...")
print("=" * 60)

application_df = pd.read_csv("dataset/application_record.csv")
credit_df = pd.read_csv("dataset/credit_record.csv")

print("Application Dataset :", application_df.shape)
print("Credit Dataset      :", credit_df.shape)

# ==========================================================
# CREATE TARGET VARIABLE
# ==========================================================

print("\nCreating Target Labels...")

bad_status = ['1', '2', '3', '4', '5']

credit_df["TARGET"] = credit_df["STATUS"].apply(
    lambda x: 0 if x in bad_status else 1
)

credit_target = (
    credit_df.groupby("ID")["TARGET"]
    .min()
    .reset_index()
)

print("Target labels created.")

# ==========================================================
# MERGE DATASETS
# ==========================================================

print("\nMerging datasets...")

df = application_df.merge(
    credit_target,
    on="ID",
    how="inner"
)

print("Merged Dataset Shape :", df.shape)

# ==========================================================
# REMOVE DUPLICATES
# ==========================================================

df.drop_duplicates(inplace=True)

# ==========================================================
# HANDLE MISSING VALUES
# ==========================================================

for column in df.columns:

    if pd.api.types.is_numeric_dtype(df[column]):
        df[column].fillna(df[column].median(), inplace=True)

    else:
        df[column].fillna(df[column].mode()[0], inplace=True)

print("Missing values handled.")

# ==========================================================
# FEATURE ENGINEERING
# ==========================================================

df["AGE"] = (-df["DAYS_BIRTH"] / 365).astype(int)

df["YEARS_EMPLOYED"] = (
    abs(df["DAYS_EMPLOYED"]) / 365
)

df["YEARS_EMPLOYED"] = df["YEARS_EMPLOYED"].replace(
    1000,
    df["YEARS_EMPLOYED"].median()
)

# ==========================================================
# DROP UNNECESSARY COLUMNS
# ==========================================================

drop_columns = [

    "ID",
    "DAYS_BIRTH",
    "DAYS_EMPLOYED",
    "FLAG_MOBIL"

]

df.drop(columns=drop_columns, inplace=True)

print("Feature engineering completed.")

# ==========================================================
# ENCODE CATEGORICAL COLUMNS
# ==========================================================

encoders = {}

for column in df.columns:

    if column != "TARGET" and not pd.api.types.is_numeric_dtype(df[column]):

        encoder = LabelEncoder()

        df[column] = encoder.fit_transform(df[column].astype(str))

        encoders[column] = encoder

print("Categorical columns encoded.")
# ==========================================================
# SPLIT FEATURES & TARGET
# ==========================================================

X = df.drop("TARGET", axis=1)

y = df["TARGET"]

print("\nDataset Ready for Training")

print("Features :", X.shape)

print("Target   :", y.shape)

print("=" * 60)


# ==========================================================
# TRAIN TEST SPLIT
# ==========================================================

print("\nSplitting Dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training Samples :", X_train.shape[0])
print("Testing Samples  :", X_test.shape[0])

# ==========================================================
# MACHINE LEARNING MODELS
# ==========================================================

models = {

    "Logistic Regression": LogisticRegression(
        max_iter=1000
    ),

    "Decision Tree": DecisionTreeClassifier(
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        max_depth=15,
        random_state=42
    ),

    "XGBoost": XGBClassifier(
        use_label_encoder=False,
        n_estimators=200,
        learning_rate=0.1,
        max_depth=6,
        random_state=42,
        eval_metric="logloss"
    )

}


results = []

best_model = None
best_model_name = ""
best_accuracy = 0

print("\n")
print("=" * 60)
print("TRAINING MODELS")
print("=" * 60)

# ==========================================================
# TRAIN & EVALUATE
# ==========================================================

for name, model in models.items():

    print(f"\nTraining {name}...")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    results.append({

        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1

    })

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")

    if accuracy > best_accuracy:

        best_accuracy = accuracy
        best_model = model
        best_model_name = name

print("\n")
print("=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

results_df = pd.DataFrame(results)

print(results_df)

print("\nBest Model :", best_model_name)
print("Best Accuracy :", round(best_accuracy, 4))


# ==========================================================
# CONFUSION MATRIX & CLASSIFICATION REPORT
# ==========================================================

print("\n")
print("=" * 60)
print("BEST MODEL EVALUATION")
print("=" * 60)

best_predictions = best_model.predict(X_test)

print("\nConfusion Matrix\n")

cm = confusion_matrix(y_test, best_predictions)

print(cm)

print("\nClassification Report\n")

print(classification_report(y_test, best_predictions))


# ==========================================================
# SAVE FORM OPTIONS
# ==========================================================

form_options = {}

for column in encoders:
    form_options[column] = list(encoders[column].classes_)

joblib.dump(form_options, "model/form_options.pkl")
# ==========================================================
# SAVE MODEL
# ==========================================================

print("\nSaving model...")

joblib.dump(best_model, "model/credit_card_model.pkl")

joblib.dump(encoders, "model/encoders.pkl")
print("Model Saved Successfully.")

# ==========================================================
# SAVE FEATURES
# ==========================================================

feature_columns = X.columns.tolist()

joblib.dump(list(X.columns), "model/features.pkl")
print("Feature List Saved.")

# ==========================================================
# SAVE CLEAN DATASET
# ==========================================================

df.to_csv(
    "dataset/final_dataset.csv",
    index=False
)

print("Final Dataset Saved.")

# ==========================================================
# PROJECT COMPLETED
# ==========================================================

print("\n")
print("=" * 60)
print("PROJECT TRAINING COMPLETED SUCCESSFULLY")
print("=" * 60)

print(f"Best Model : {best_model_name}")
print(f"Accuracy   : {best_accuracy:.4f}")

print("\nGenerated Files:")

print("✔ model/credit_card_model.pkl")
print("✔ model/encoders.pkl")
print("✔ model/features.pkl")
print("✔ dataset/final_dataset.csv")

print("\nReady for Flask Deployment.")
print("=" * 60)