# Experiment Log
*****************************************************************************************************
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
*****************************************************************************************************
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

*****************************************************************************************************
## Experiment 3 – Hyperparameter Tuning of XGBoost

**Date:** 15 July 2026

### Objective
Optimize the baseline XGBoost classifier using RandomizedSearchCV.

### Search Strategy
- RandomizedSearchCV
- 5-fold Cross Validation
- 20 parameter combinations

### Tuned Parameters
- n_estimators
- max_depth
- learning_rate
- subsample
- colsample_bytree
- min_child_weight
- gamma

### Best Parameters
Best Parameters:
{'colsample_bytree': np.float64(0.9497327922401264), 'gamma': np.float64(0.10616955533913808), 'learning_rate': np.float64(0.04636499344142013), 'max_depth': 7, 'min_child_weight': 1, 'n_estimators': 413, 'subsample': np.float64(0.8574269294896713)}

### Best Cross Validation Score
Best CV Accuracy:
0.9999787951679462

### Output Files
- models/xgboost_tuned.pkl
- results/xgb_tuned_metrics.csv

### Conclusion
The baseline XGBoost classifier already achieved near-perfect performance on the selected feature set. Hyperparameter optimization using RandomizedSearchCV did not yield any measurable improvement, indicating that the default configuration was already sufficient for this dataset.
	Metric	Baseline	Tuned
0	Accuracy	1.0	1.0
1	Precision	1.0	1.0
2	Recall	1.0	1.0
3	F1	1.0	1.0
4	ROC-AUC	1.0	1.0

*****************************************************************************************************
## Experiment 4 – Soft Voting Ensemble

### Objective
Combine Logistic Regression, Random Forest, and the tuned XGBoost classifier using soft voting to evaluate whether an ensemble improves phishing website detection performance.

### Ensemble Members
- Logistic Regression
- Random Forest
- Tuned XGBoost

### Voting Strategy
Soft Voting

### Evaluation Metrics
- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- 5-Fold Cross Validation

### Output Files
- models/ensemble.pkl
- results/ensemble_metrics.csv
- results/model_comparison.csv
- reports/figures/confusion_matrix_ensemble.png
- reports/figures/roc_ensemble.png
********************************************************************************************************