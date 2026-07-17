#!/usr/bin/env python3
"""
Retrain the ensemble model with capped LargestLineLength feature.
This script retrains the model to fix the false positives on legitimate websites.
"""

import sys
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

# Set random seed for reproducibility
np.random.seed(42)

print("=" * 70)
print("Retraining Ensemble Model with Capped LargestLineLength")
print("=" * 70)

# =====================================================================
# Load Data
# =====================================================================
print("\n[1/5] Loading dataset...")
data_path = Path("data/processed/final_dataset.csv")
df = pd.read_csv(data_path)

# Cap LargestLineLength to handle minified JavaScript in modern websites
# This was causing false positives on legitimate sites like YouTube, Google, etc.
df['LargestLineLength'] = df['LargestLineLength'].clip(upper=1000)

print(f"Dataset shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"LargestLineLength - Min: {df['LargestLineLength'].min()}, Max: {df['LargestLineLength'].max()}")

# =====================================================================
# Prepare Features and Target
# =====================================================================
print("\n[2/5] Preparing features...")

# Separate features and target
X = df.drop("label", axis=1)

# Remove HTML-based features that cause false positives on modern websites
# Modern websites load content via JavaScript, so initial HTML is minimal
# This makes them appear as phishing to a model trained on older website patterns
FEATURES_TO_DROP = ["LineOfCode", "LargestLineLength"]
X = X.drop(columns=FEATURES_TO_DROP)

print(f"  • Removed problematic HTML features: {FEATURES_TO_DROP}")
print(f"  • Using only URL-based features: {list(X.columns)}")

y = df["label"]

print(f"Features shape: {X.shape}")
print(f"Target distribution:\n{y.value_counts()}")

# =====================================================================
# Split Data
# =====================================================================
print("\n[3/5] Splitting data (80/20 train/test)...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42,
    stratify=y
)

print(f"Training set: {X_train.shape}")
print(f"Test set: {X_test.shape}")

# =====================================================================
# Train Individual Models
# =====================================================================
print("\n[4/5] Training individual models...")

print("  • Training Logistic Regression...", end=" ", flush=True)
lr = LogisticRegression(random_state=42, max_iter=1000)
lr.fit(X_train, y_train)
print("✓")

print("  • Training Random Forest...", end=" ", flush=True)
rf = RandomForestClassifier(random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
print("✓")

print("  • Training XGBoost...", end=" ", flush=True)
xgb = XGBClassifier(random_state=42, eval_metric="logloss", n_jobs=-1)
xgb.fit(X_train, y_train)
print("✓")

# =====================================================================
# Create Ensemble
# =====================================================================
print("\n[4.5/5] Creating soft voting ensemble...")

ensemble = VotingClassifier(
    estimators=[
        ("lr", lr),
        ("rf", rf),
        ("xgb", xgb)
    ],
    voting="soft",
    n_jobs=-1
)

ensemble.fit(X_train, y_train)
print("✓ Ensemble trained")

# =====================================================================
# Evaluate
# =====================================================================
print("\n[5/5] Evaluating ensemble model...")

y_pred = ensemble.predict(X_test)
y_pred_proba = ensemble.predict_proba(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_proba[:, 1])

print(f"  • Accuracy:  {accuracy:.6f}")
print(f"  • Precision: {precision:.6f}")
print(f"  • Recall:    {recall:.6f}")
print(f"  • F1 Score:  {f1:.6f}")
print(f"  • ROC-AUC:   {roc_auc:.6f}")

# =====================================================================
# Save Model
# =====================================================================
print("\n[6/5] Saving model...")

model_path = Path("models/ensemble.pkl")
joblib.dump(ensemble, model_path)

print(f"✓ Model saved to: {model_path}")

print("\n" + "=" * 70)
print("✓ Retraining complete!")
print("=" * 70)
