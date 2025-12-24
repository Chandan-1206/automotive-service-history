import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import hamming_loss, classification_report
import numpy as np

print("=" * 60)
print("VEHICLE SERVICE RECOMMENDATION SYSTEM - MODEL EVALUATION")
print("=" * 60)

# ---------------- LOAD DATA ----------------
print("\n[1/5] Loading dataset...")
df = pd.read_csv("vehicle_service_history.csv")
print(f"✅ Loaded {len(df)} records")

# ---------------- LOAD ENCODERS ----------------
print("\n[2/5] Loading encoders and model...")
model = joblib.load("service_recommendation_model.pkl")
mlb = joblib.load("mlb_encoder.pkl")
company_encoder = joblib.load("company_encoder.pkl")
model_encoder = joblib.load("model_encoder.pkl")

# ---------------- PREPROCESS TARGET ----------------
print("\n[3/5] Preparing target labels...")
df["service_issues_list"] = df["service_issues"].apply(
    lambda x: [issue.strip() for issue in x.split(",")]
)
y = mlb.transform(df["service_issues_list"])

# ---------------- PREPROCESS FEATURES ----------------
print("\n[4/5] Preparing feature matrix...")
df["company_encoded"] = company_encoder.transform(df["company"])
df["model_encoded"] = model_encoder.transform(df["model"])

X = df[
    ["company_encoded", "model_encoded", "year", "vehicle_age", "mileage"]
].values

print(f"✅ Feature matrix shape: {X.shape}")
print(f"✅ Target matrix shape : {y.shape}")

# ---------------- TRAIN / TEST SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------- PREDICTIONS ----------------
print("\n[5/5] Evaluating model...")
y_pred = model.predict(X_test)

# ---------------- METRICS ----------------
hamming = hamming_loss(y_test, y_pred)
accuracy = 1 - hamming

print("\n📊 MODEL PERFORMANCE")
print("-" * 30)
print(f"Accuracy (1 - Hamming Loss): {accuracy:.2%}")
print(f"Hamming Loss              : {hamming:.4f}")

print("\n📋 CLASSIFICATION REPORT (per service issue)")
print("-" * 30)
print(
    classification_report(
        y_test,
        y_pred,
        target_names=mlb.classes_,
        zero_division=0
    )
)

# ---------------- SAMPLE PREDICTIONS ----------------
print("\n🔍 SAMPLE PREDICTIONS")
print("-" * 30)

for i in range(min(3, len(X_test))):
    actual = mlb.inverse_transform(y_test[i:i+1])[0]
    predicted = mlb.inverse_transform(y_pred[i:i+1])[0]

    print(f"\nSample {i+1}:")
    print(f"  Vehicle -> Year: {int(X_test[i][2])}, "
          f"Age: {int(X_test[i][3])}, "
          f"Mileage: {int(X_test[i][4])} km")
    print(f"  Actual Issues   : {', '.join(actual) if actual else 'None'}")
    print(f"  Predicted Issues: {', '.join(predicted) if predicted else 'None'}")

print("\n" + "=" * 60)
print("✅ MODEL EVALUATION COMPLETED")
print("=" * 60)
