import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


# ============================================================
# 1. LOAD DATASET
# ============================================================

df = pd.read_csv("backend/data/ai4i2020.csv")

print("Dataset shape:", df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())


# ============================================================
# 2. TARGET DISTRIBUTION
# ============================================================

print("\nMachine failure distribution:")
print(df["Machine failure"].value_counts())

print("\nMachine failure percentage:")
print(df["Machine failure"].value_counts(normalize=True) * 100)


# ============================================================
# 3. SELECT FEATURES AND TARGET
# ============================================================

feature_columns = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]

X = df[feature_columns]

y = df["Machine failure"]

print("\nSelected features:")
print(X.columns.tolist())

print("\nFeature shape:", X.shape)
print("Target shape:", y.shape)


# ============================================================
# 4. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining feature shape:", X_train.shape)
print("Testing feature shape:", X_test.shape)

print("\nTraining target distribution:")
print(y_train.value_counts())

print("\nTesting target distribution:")
print(y_test.value_counts())


# ============================================================
# 5. SCALE FEATURES FOR LOGISTIC REGRESSION
# ============================================================

logistic_pipeline = Pipeline([
    ("scaler", StandardScaler())
])

# Fit scaler only on training data
X_train_scaled = logistic_pipeline.fit_transform(X_train)

# Transform test data using the same fitted scaler
X_test_scaled = logistic_pipeline.transform(X_test)

print("\nScaled training shape:", X_train_scaled.shape)
print("Scaled testing shape:", X_test_scaled.shape)


# ============================================================
# 6. TRAIN LOGISTIC REGRESSION
# ============================================================

logistic_model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

logistic_model.fit(X_train_scaled, y_train)


# ============================================================
# 7. TRAIN DECISION TREE
# ============================================================

decision_tree_model = DecisionTreeClassifier(
    random_state=42
)

decision_tree_model.fit(X_train, y_train)


# ============================================================
# 8. TRAIN RANDOM FOREST
# ============================================================

random_forest_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

random_forest_model.fit(X_train, y_train)


# ============================================================
# 9. TRAIN BALANCED RANDOM FOREST
# ============================================================

balanced_random_forest_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

balanced_random_forest_model.fit(X_train, y_train)

print("\nAll models trained successfully.")


# ============================================================
# 10. GENERATE PREDICTIONS
# ============================================================

logistic_predictions = logistic_model.predict(X_test_scaled)

decision_tree_predictions = decision_tree_model.predict(X_test)

random_forest_predictions = random_forest_model.predict(X_test)

balanced_random_forest_predictions = (
    balanced_random_forest_model.predict(X_test)
)


# ============================================================
# 11. MODEL EVALUATION FUNCTION
# ============================================================

def evaluate_model(name, y_true, y_pred):

    print(f"\n{name}")
    print("-" * len(name))

    accuracy = accuracy_score(y_true, y_pred)

    precision = precision_score(
        y_true,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_true,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_true,
        y_pred,
        zero_division=0
    )

    print("Accuracy :", accuracy)
    print("Precision:", precision)
    print("Recall   :", recall)
    print("F1-score :", f1)

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_true, y_pred))

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


# ============================================================
# 12. EVALUATE ALL MODELS
# ============================================================

logistic_results = evaluate_model(
    "Logistic Regression",
    y_test,
    logistic_predictions
)

decision_tree_results = evaluate_model(
    "Decision Tree",
    y_test,
    decision_tree_predictions
)

random_forest_results = evaluate_model(
    "Random Forest",
    y_test,
    random_forest_predictions
)

balanced_random_forest_results = evaluate_model(
    "Balanced Random Forest",
    y_test,
    balanced_random_forest_predictions
)


# ============================================================
# 13. RANDOM FOREST FAILURE PROBABILITY
# ============================================================

random_forest_probabilities = (
    random_forest_model.predict_proba(X_test)[:, 1]
)

print("\nRandom Forest failure probability examples:")
print(random_forest_probabilities[:10])


# ============================================================
# 14. RANDOM FOREST THRESHOLD ANALYSIS
# ============================================================

thresholds = [0.10, 0.20, 0.30, 0.40, 0.50]

print("\nRandom Forest threshold analysis:")

for threshold in thresholds:

    threshold_predictions = (
        random_forest_probabilities >= threshold
    ).astype(int)

    precision = precision_score(
        y_test,
        threshold_predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        threshold_predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        threshold_predictions,
        zero_division=0
    )

    print(
        f"Threshold: {threshold:.2f} | "
        f"Precision: {precision:.3f} | "
        f"Recall: {recall:.3f} | "
        f"F1: {f1:.3f}"
    )


# ============================================================
# 15. SELECT PRODUCTION MODEL
# ============================================================

# Random Forest achieved the best F1-score among our
# tested production candidates, so we select it.

selected_model = random_forest_model

selected_model_name = "Random Forest"

# Classification threshold selected from threshold analysis.
# At 0.40 we achieved the highest F1-score in our test.
selected_threshold = 0.40

print("\nSelected production model:")
print(selected_model_name)

print("\nSelected classification threshold:")
print(selected_threshold)


# ============================================================
# 16. CREATE MODEL DIRECTORY
# ============================================================

model_directory = "backend/app/ml/model"

os.makedirs(
    model_directory,
    exist_ok=True
)


# ============================================================
# 17. SAVE RANDOM FOREST MODEL
# ============================================================

model_path = os.path.join(
    model_directory,
    "random_forest.pkl"
)

joblib.dump(
    selected_model,
    model_path
)

print("\nModel saved successfully:")
print(model_path)


# ============================================================
# 18. SAVE MODEL METADATA
# ============================================================

metadata = {
    "model_name": selected_model_name,
    "model_type": "RandomForestClassifier",
    "features": feature_columns,
    "classification_threshold": selected_threshold,
    "n_estimators": 100,
    "random_state": 42
}

metadata_path = os.path.join(
    model_directory,
    "model_metadata.pkl"
)

joblib.dump(
    metadata,
    metadata_path
)

print("\nModel metadata saved successfully:")
print(metadata_path)


# ============================================================
# 19. LOAD SAVED MODEL
# ============================================================

loaded_model = joblib.load(model_path)

print("\nSaved model loaded successfully.")


# ============================================================
# 20. VERIFY LOADED MODEL
# ============================================================

sample_data = X_test.iloc[:5]

sample_predictions = loaded_model.predict(
    sample_data
)

sample_probabilities = (
    loaded_model.predict_proba(sample_data)[:, 1]
)

print("\nLoaded model sample predictions:")
print(sample_predictions)

print("\nLoaded model sample failure probabilities:")
print(sample_probabilities)


# ============================================================
# 21. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("PHASE 2 - ML TRAINING PIPELINE COMPLETED")
print("=" * 60)

print("\nProduction model:")
print(selected_model_name)

print("\nModel file:")
print(model_path)

print("\nMetadata file:")
print(metadata_path)

print("\nClassification threshold:")
print(selected_threshold)

print("\nThe trained model is ready for the FastAPI inference layer.")