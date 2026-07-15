# Experiment Log

## Experiment 1 – Data Cleaning

**Date:** 15 July 2026

### Objective
Prepare the dataset for machine learning by checking its quality and removing inconsistencies.

### Dataset
PhiUSIIL Phishing URL Dataset

### Steps Performed
- Loaded the dataset.
- Examined dataset dimensions and feature information.
- Checked for missing values.
- Checked for duplicate records.
- Verified data types.
- Saved the cleaned dataset.

### Results
- Missing values: 0
- Duplicate rows: 0
- Dataset is suitable for further preprocessing.

### Output Files
- data/processed/clean_dataset.csv

### Conclusion
The dataset required no cleaning and was ready for feature selection.

# Experiment 2 – Baseline XGBoost

## Date
15 July 2026

## Objective
Train a baseline XGBoost classifier using the selected URL-based features.

## Dataset
PhiUSIIL Phishing URL Dataset

## Parameters
- random_state = 42
- eval_metric = logloss
- train/test split = 80/20
- stratified sampling = True

## Results

Accuracy : 1.0000

Precision : 1.0000

Recall : 1.0000

F1 Score : 1.0000

ROC-AUC : 1.0000

## Output Files

- models/xgboost.pkl
- results/xgb_metrics.csv
- reports/figures/confusion_matrix_xgb.png
- reports/figures/roc_xgb.png
- reports/figures/xgb_feature_importance.png

## Observation

The baseline model achieved perfect classification on the current test set.
Further validation and hyperparameter tuning will be performed to verify that this performance is not due to overfitting or data leakage.