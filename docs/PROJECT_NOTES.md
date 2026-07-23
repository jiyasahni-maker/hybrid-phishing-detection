# Hybrid Phishing Detection — beginner's project notes

## 1. What this project does

This project is a **binary machine-learning classifier**. Given a website URL, it
tries to decide between two classes:

| Stored numeric label | Meaning in this project |
| --- | --- |
| `0` | Phishing website |
| `1` | Legitimate website |

A phishing website is a deceptive site that attempts to look like a trusted
service in order to collect passwords, banking details, or other sensitive
information. A traditional blacklist can only block sites already known to be
malicious. This project instead learns patterns from labelled examples, so it
can potentially flag previously unseen URLs with similar characteristics.

The word **hybrid** refers to combining several machine-learning models in one
final decision. It does *not* mean that the deployed system performs live
threat-intelligence lookups or antivirus scanning.

## 2. The big picture

```text
Labelled phishing/legitimate URL dataset
                 |
                 v
Data checks and exploration (EDA)
                 |
                 v
Feature selection: choose useful measurable URL/page properties
                 |
                 v
Train and compare LR, Random Forest, and XGBoost
                 |
                 v
Soft-voting ensemble saved as models/ensemble.pkl
                 |
                 v
Streamlit dashboard: URL -> features -> model probability -> result
```

**Training** is the offline learning phase using thousands of labelled rows.
**Inference** (or prediction) is the live phase: the dashboard turns one typed
URL into the same kind of input fields and asks the saved model for a decision.

## 3. Repository map

| Location | Purpose |
| --- | --- |
| `data/processed/clean_dataset.csv` | Full cleaned dataset, 235,795 data rows and 56 columns. |
| `data/processed/selected_features.csv` | The 10 fields selected by the feature-selection notebook, with scores. |
| `data/processed/final_dataset.csv` | The 10 selected fields plus `label`; the original modelling dataset. |
| `notebooks/01_EDA.ipynb` | Exploration and data-quality checks. |
| `notebooks/feature_selection.ipynb` | Mutual-information and decision-tree feature-selection work. |
| `notebooks/final_data.ipynb` | Builds `final_dataset.csv` from the selected columns. |
| `notebooks/logistic_regression.ipynb` | Logistic Regression experiment. |
| `notebooks/random_forest.ipynb` | Random Forest experiment and cross-validation. |
| `notebooks/XGboost.ipynb` | Baseline/tuned XGBoost experiment. |
| `notebooks/Ensemble.ipynb` | Initial soft-voting ensemble experiment. |
| `retrain_model.py` | Current retraining script; creates the deployment ensemble using eight URL-only fields. |
| `models/*.pkl` | Serialized trained models. `ensemble.pkl` is what the app loads. |
| `app/` | Streamlit user interface and live prediction code. |
| `results/` | CSV metrics from model experiments. |
| `reports/figures/` | Confusion-matrix, ROC, and feature-importance images. |
| `experiments/experiment_log.md` | Short record of the experiment sequence. |
| `requirements.txt` | Python packages pinned for the project environment. |

`src/predict.py`, `src/extract_features.py`, and `config/config.py` are empty
placeholders. The working application code is under `app/`, not `src/`.

## 4. The dataset and basic data concepts

The project uses the **PhiUSIIL Phishing URL Dataset** (identified in the
Research page as coming from Kaggle). Each row represents a URL and related
measurements. The full processed file has a URL, domain/text fields, 53-ish
measurements, and the target `label`.

Important terms:

- A **row** is one example website.
- A **column** or **feature** is one measurable characteristic, such as URL
  length.
- The **target** is the answer the model is supposed to learn: `label`.
- A **numeric feature** is already a number and can be passed to these models.
- A **categorical/text field** (for example `URL` or `Domain`) needs special
  encoding before many models can use it; the selection notebook excludes
  those fields.

The EDA notebook checks shape, data types, descriptive statistics, missing
values, duplicate rows, class balance, correlations, distributions, and
outliers. The experiment log records zero missing values and zero duplicates,
so it saves the data as `clean_dataset.csv` without imputation or deduplication.

## 5. Feature engineering and selection

**Feature engineering** means representing a real-world object in numbers a
model can learn from. A model cannot understand a URL as a person does, but it
can compare numerical patterns such as its length or digit ratio.

The original selection process keeps fields that appear in both of these top-25
lists:

1. **Mutual information (MI):** measures how much knowing a feature reduces
   uncertainty about the label. It can capture non-linear relationships.
2. **Information gain (IG):** here approximated by the feature importance of
   a decision tree trained with entropy. A feature is useful when splitting on
   it makes child groups more pure (more often one class).

This intersection produces ten fields in `final_dataset.csv`:

| Feature (spelling retained from dataset) | Plain-English meaning | How the app calculates it live |
| --- | --- | --- |
| `LineOfCode` | Number of lines in downloaded HTML. | `html.splitlines()` count. |
| `IsHTTPS` | Whether the URL starts with `https://`. | `1` for HTTPS, otherwise `0`. |
| `URLLength` | Total characters in the normalized URL. | `len(url)`. |
| `CharContinuationRate` | Length of the longest uninterrupted letters/digits run, divided by URL length. | Regex finds `[A-Za-z0-9]+` runs. |
| `LetterRatioInURL` | Fraction of URL characters that are letters. | letters / URL length. |
| `NoOfDegitsInURL` | Count of digits in URL. (`Degits` is a dataset typo.) | `c.isdigit()` count. |
| `DegitRatioInURL` | Fraction of URL characters that are digits. | digits / URL length. |
| `NoOfOtherSpecialCharsInURL` | Count of non-letter/non-digit characters. | count of `not c.isalnum()`. |
| `SpacialCharRatioInURL` | Fraction of non-alphanumeric URL characters. (`Spacial` is a dataset typo.) | special chars / URL length. |
| `LargestLineLength` | Character count of the longest HTML line. | maximum line length, capped at 1,000. |

The ratios let the model compare short and long URLs fairly. For example, five
digits mean something different in a 12-character URL than in a 200-character
URL. HTTPS is useful context but is not proof of safety: phishing sites can
also obtain HTTPS certificates.

## 6. Why the final deployed model uses only eight fields

The original notebooks train on all ten selected features. The later
`retrain_model.py` deliberately removes `LineOfCode` and `LargestLineLength`.
Modern websites often send a very small initial HTML page and load the page
through JavaScript; minified JavaScript can also create extremely long lines.
Those page-structure signals caused false positives on legitimate modern sites.

The saved `models/ensemble.pkl` confirms that it expects these eight columns,
in this exact order:

```text
IsHTTPS, URLLength, CharContinuationRate, LetterRatioInURL,
NoOfDegitsInURL, DegitRatioInURL, NoOfOtherSpecialCharsInURL,
SpacialCharRatioInURL
```

The app still downloads HTML and displays the two omitted HTML features, but
drops them before model prediction. This is an important distinction between
**features displayed to the user** and **features actually used by the model**.

## 7. Train/test split and reproducibility

The experiments use `train_test_split(..., test_size=0.20, random_state=42,
stratify=y)`.

- **80% training set:** examples used to fit a model's parameters.
- **20% test set:** held-out examples used for the final reported evaluation.
- **Stratification:** keeps the phishing/legitimate class proportions similar
  in both parts.
- **`random_state=42`:** fixes the random split so another run can reproduce
  the same partition and results.

The Random Forest experiment also uses **5-fold cross-validation**: it divides
the training data into five parts, trains on four and validates on one,
repeating until every part has been the validation part. The XGBoost tuning
step uses the same five-fold idea inside `RandomizedSearchCV`.

## 8. Models used

### Logistic Regression

Despite its name, Logistic Regression is a classification model. It forms a
weighted sum of the features, applies an S-shaped logistic function, and
returns a class probability. It is a fast, interpretable **baseline**: a simple
model against which more complex models can be compared.

### Random Forest

A decision tree repeatedly asks threshold questions such as “is the URL longer
than this value?” A Random Forest trains many trees on varied samples/features
and averages their votes. This reduces the tendency of a single tree to
memorize training data. The notebook configures 100 trees.

### XGBoost

XGBoost is **gradient boosting**: it builds small decision trees one after
another, with each new tree focusing on mistakes made by the earlier ensemble.
It is especially strong on structured/tabular numerical data. The baseline
uses default-style settings with `eval_metric='logloss'`; the tuning notebook
tries 20 random parameter combinations across settings such as number/depth of
trees, learning rate, row/column sampling, and split constraints.

### Soft Voting Ensemble (the deployment model)

The final model contains Logistic Regression, Random Forest, and XGBoost.
With **hard voting**, each model would merely choose a class and the majority
would win. With **soft voting**, each gives a probability for each class and
the ensemble averages those probabilities before selecting the largest one.

For example, if models assign legitimate probabilities of 0.70, 0.90, and
0.80, the soft-voting result is roughly 0.80. Using confidence rather than
only yes/no votes can make a combined decision more stable.

## 9. Evaluation metrics

For this security task, a **positive class** in scikit-learn's default metrics
is label `1`, which this project treats as legitimate. That is easy to miss:
the reported precision/recall describe identifying legitimate sites unless
the `pos_label` is changed. Security-focused reporting should additionally
show phishing-class recall (how many phishing sites were caught).

| Metric | Beginner explanation |
| --- | --- |
| Accuracy | Fraction of all predictions that were correct. |
| Precision | Of the items predicted as the positive class, how many truly were positive? |
| Recall | Of all truly positive items, how many did the model find? |
| F1 score | Harmonic mean of precision and recall; penalizes a model when one is much lower. |
| ROC-AUC | How well probability scores rank the two classes across many possible thresholds; 1.0 is ideal, 0.5 is random ranking. |
| Confusion matrix | Table of actual vs predicted class counts, showing each type of mistake. |

The recorded held-out results are extremely high: the final ensemble reports
accuracy `0.99978795` (about 99.98%) and ROC-AUC `0.99999610`. This is a
promising experiment result, not a guarantee of real-world protection. Scores
this close to perfect deserve additional checks for source overlap, duplicate
or related URLs crossing the split, feature leakage, a newer external test
set, and phishing-class error analysis.

## 10. Live dashboard prediction flow

When a user opens the app and presses **Analyze URL**, this is the intended
flow:

1. `app/pages/1_Dashboard.py` collects the URL and creates `PhishingPredictor`.
2. `FeatureExtractor.normalize_url()` trims whitespace and adds `https://` if
   the scheme is missing.
3. `requests.get()` tries to download HTML with a browser-like User-Agent and
   a five-second timeout. A failure becomes an empty HTML string rather than
   crashing the page.
4. `FeatureExtractor` calculates the ten displayed fields and builds a
   one-row pandas `DataFrame` in its fixed `FEATURE_ORDER`.
5. `PhishingPredictor` checks a small hard-coded list of well-known domains.
   A whitelisted domain gets a “Legitimate Website” result without relying on
   the model.
6. For other URLs it removes the two HTML fields, then asks the joblib-loaded
   soft-voting model for `predict()` and `predict_proba()`.
7. The dashboard presents the label, confidence, feature table, a URL
   composition doughnut, and feature-value bars.

`ModelLoader.load_model()` uses Streamlit's `@st.cache_resource`, which means
the pickle file is loaded once per app process rather than on every scan.
`joblib` is the library used to save/load Python model objects efficiently.

## 11. Presentation and libraries

- **Streamlit:** turns Python calls such as `st.text_input`, `st.button`, and
  `st.dataframe` into a web dashboard.
- **pandas:** represents tabular data; a one-row DataFrame is the model input.
- **scikit-learn:** splitting, Logistic Regression, Random Forest, voting,
  feature selection/search utilities, and metrics.
- **XGBoost:** gradient-boosted decision-tree classifier.
- **requests:** HTTP download of a scanned page.
- **regular expressions (`re`):** locates alphanumeric runs in a URL.
- **Plotly:** interactive gauge, bar, and pie/doughnut charts.
- **Matplotlib and Seaborn:** notebook/report visualizations such as ROC and
  confusion-matrix images.

To run the UI from the project root in its configured virtual environment:

```bash
.venv/bin/streamlit run app/app.py
```

The pages import modules as `core...` and `components...`; running via
Streamlit from the repository root preserves the expected app import path.

## 12. Important implementation notes and limitations

These are observations from the current files, not changes made by this note.

1. **Dashboard confidence is formatted incorrectly.** `predictor.py` returns
   confidence on a 0–100 scale (for example `99.99`), but
   `1_Dashboard.py`/`result_cards.py` render it with `:.2%`, which assumes a
   0–1 fraction. That can display `9999.00%`. The gauge also multiplies by 100
   a second time. Use either fractions everywhere or percentage values
   everywhere, but not both.
2. **Gauge colour condition does not match the label.** `threat_gauge()` checks
   whether the prediction text equals `"legitimate"`, but it receives
   `"Legitimate Website"`; the strict comparison is false, so it selects the
   red bar colour even for legitimate results.
3. **Whitelist can be skipped for scheme-less input.** The extractor normalizes
   `youtube.com` to `https://youtube.com`, but `_is_whitelisted()` parses the
   original input. Without a scheme, `urlparse('youtube.com').netloc` is empty.
   Normalize before the whitelist check to make both steps agree.
4. **The whitelist is a product rule, not machine learning.** It can reduce
   false positives for listed domains, but it is manual, incomplete, and trust
   in a base domain does not itself validate every possible subdomain/path.
5. **Downloading an untrusted URL has operational risk.** The server running
   the dashboard makes the network request. In a production scanner, restrict
   outbound destinations, block private/internal IP ranges, control redirects,
   and isolate the fetcher to reduce SSRF and malicious-content exposure.
6. **Only URL-shape features are deployed.** This is quick and privacy-light,
   but cannot inspect page text, forms, certificates, domain age, reputation,
   screenshots, or brand impersonation. It should be a warning signal, not the
   sole basis for a high-stakes security decision.
7. **Training/deployment history has two configurations.** Old result CSVs and
   the research page describe ten selected features. The current saved model
   uses eight URL-only features after retraining. Keep versioned data/model/
   metric records so reported results can always be matched to the deployed
   model.
8. **Some Research-page documentation is stale.** It mentions
   `URLSimilarityIndex` and `TLDLegitimateProb`, which are not in either the
   selected ten-feature dataset or the eight-feature deployment model.

## 13. A sensible next learning path

If you are learning from this project, study it in this order:

1. Open `01_EDA.ipynb` to understand rows, labels, class balance, and data
   quality.
2. Read `feature_selection.ipynb` and compare its chosen columns with
   `final_dataset.csv`.
3. Compare the three individual model notebooks and their metric CSVs.
4. Read `Ensemble.ipynb` to understand why probabilities are combined.
5. Read `retrain_model.py` next, because it creates the actual `ensemble.pkl`
   loaded by the UI.
6. Finally trace `app/pages/1_Dashboard.py` -> `app/core/predictor.py` ->
   `app/core/feature_extractor.py` for the live path.

The key lesson is that a good ML application is more than a high score: the
training features, live feature calculations, model version, display logic,
and security boundaries all need to stay consistent.
