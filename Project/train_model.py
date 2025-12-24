import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import accuracy_score, classification_report, hamming_loss
import joblib
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("VEHICLE SERVICE RECOMMENDATION SYSTEM - MODEL TRAINING")
print("=" * 60)

# Load dataset
print("\n[1/6] Loading dataset...")
df = pd.read_csv('vehicle_service_history.csv')
print(f"✅ Loaded {len(df)} records")
print(f"Columns: {df.columns.tolist()}")

# Preprocess service issues
print("\n[2/6] Preprocessing service issues...")
df['service_issues_list'] = df['service_issues'].apply(lambda x: [issue.strip() for issue in x.split(',')])

# Get all unique issues
all_issues = set()
for issues in df['service_issues_list']:
    all_issues.update(issues)
all_issues = sorted(list(all_issues))
print(f"✅ Found {len(all_issues)} unique service issues")
print(f"Issues: {all_issues[:5]}... (showing first 5)")

# Create multi-label binarizer
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(df['service_issues_list'])
print(f"✅ Created binary labels with shape: {y.shape}")

# Feature Engineering
print("\n[3/6] Engineering features...")

# Encode company
company_encoder = LabelEncoder()
df['company_encoded'] = company_encoder.fit_transform(df['company'])

# Encode model
model_encoder = LabelEncoder()
df['model_encoded'] = model_encoder.fit_transform(df['model'])

# Create feature matrix
X = df[['company_encoded', 'model_encoded', 'year', 'vehicle_age', 'mileage']].values
print(f"✅ Feature matrix shape: {X.shape}")
print(f"Features: company, model, year, vehicle_age, mileage")

# Split data
print("\n[4/6] Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"✅ Training set: {X_train.shape[0]} samples")
print(f"✅ Test set: {X_test.shape[0]} samples")

# Train model
print("\n[5/6] Training Random Forest model...")
print("This may take a few minutes...")

# Use MultiOutputClassifier with RandomForest
base_classifier = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model = MultiOutputClassifier(base_classifier, n_jobs=-1)
model.fit(X_train, y_train)
print("✅ Model training completed!")

# Evaluate model
print("\n[6/6] Evaluating model...")
y_pred = model.predict(X_test)

# Calculate metrics
hamming = hamming_loss(y_test, y_pred)
accuracy = 1 - hamming

print(f"\n📊 Model Performance:")
print(f"  - Accuracy (1 - Hamming Loss): {accuracy:.2%}")
print(f"  - Hamming Loss: {hamming:.4f}")

# Sample predictions
print(f"\n🔍 Sample Predictions on Test Set:")
for i in range(min(3, len(X_test))):
    actual_issues = mlb.inverse_transform(y_test[i:i+1])[0]
    predicted_issues = mlb.inverse_transform(y_pred[i:i+1])[0]
    
    print(f"\nSample {i+1}:")
    print(f"  Vehicle: Year {int(X_test[i][2])}, Age {int(X_test[i][3])}, Mileage {int(X_test[i][4])} km")
    print(f"  Actual issues: {', '.join(actual_issues) if actual_issues else 'None'}")
    print(f"  Predicted issues: {', '.join(predicted_issues) if predicted_issues else 'None'}")

# Save model and encoders
print("\n💾 Saving model and encoders...")
joblib.dump(model, 'service_recommendation_model.pkl')
joblib.dump(mlb, 'mlb_encoder.pkl')
joblib.dump(company_encoder, 'company_encoder.pkl')
joblib.dump(model_encoder, 'model_encoder.pkl')

# Save feature info
feature_info = {
    'companies': company_encoder.classes_.tolist(),
    'models': model_encoder.classes_.tolist(),
    'service_issues': mlb.classes_.tolist()
}
joblib.dump(feature_info, 'feature_info.pkl')

print("✅ Saved the following files:")
print("  - service_recommendation_model.pkl")
print("  - mlb_encoder.pkl")
print("  - company_encoder.pkl")
print("  - model_encoder.pkl")
print("  - feature_info.pkl")

print("\n" + "=" * 60)
print("✅ MODEL TRAINING COMPLETED SUCCESSFULLY!")
print("=" * 60)
print("\nYou can now use this model in your Flask application")
print("to predict service issues for new vehicles.")