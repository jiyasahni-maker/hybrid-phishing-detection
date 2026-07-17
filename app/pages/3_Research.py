import streamlit as st
import pandas as pd
from pathlib import Path

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Research & Documentation",
    page_icon=None,
    layout="wide"
)

# ==========================================================
# LOAD CSS
# ==========================================================

css_path = Path(__file__).parent.parent / "assets" / "styles.css"

with open(css_path) as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ==========================================================
# HERO
# ==========================================================

st.markdown(
"""
<div class="main-title">
Research & Documentation
</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div class="subtitle">
Documentation of the Hybrid Phishing Detection System, including the dataset,
feature engineering process, machine learning models, and technologies used
during development.
</div>
""",
unsafe_allow_html=True
)

st.write("")

# ==========================================================
# PROJECT OVERVIEW
# ==========================================================

st.markdown(
"""
<div class="section-title">
Project Overview
</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div class="glass-card">

The Hybrid Phishing Detection System is a machine learning application
designed to identify whether a website URL is **Legitimate** or **Phishing**.

The project evaluates multiple machine learning algorithms and compares their
performance using standard evaluation metrics such as Accuracy, Precision,
Recall, F1 Score, and ROC-AUC. A Soft Voting Ensemble model was selected as
the final deployment model because it provided the most reliable and
consistent performance.

The application is built using Streamlit to provide an interactive dashboard
for real-time phishing detection.

</div>
""",
unsafe_allow_html=True
)

st.write("")

# ==========================================================
# PROBLEM STATEMENT
# ==========================================================

st.markdown(
"""
<div class="section-title">
Problem Statement
</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div class="glass-card">

Phishing websites are designed to imitate legitimate websites in order to
steal sensitive information such as usernames, passwords, banking details,
and personal data.

Traditional blacklist-based approaches cannot always detect newly created
phishing websites. This project explores the use of machine learning to
classify URLs based on their characteristics, enabling faster and more
accurate phishing detection.

</div>
""",
unsafe_allow_html=True
)

st.write("")

# ==========================================================
# DATASET
# ==========================================================

st.markdown(
"""
<div class="section-title">
Dataset
</div>
""",
unsafe_allow_html=True
)

dataset = pd.DataFrame({
    "Property": [
        "Dataset Name",
        "Source",
        "Total URLs",
        "Training Split",
        "Testing Split",
        "Classification"
    ],
    "Value": [
        "PhiUSIIL Phishing URL Dataset",
        "Kaggle",
        "235,795 URLs",
        "80%",
        "20%",
        "Legitimate / Phishing"
    ]
})

st.dataframe(
    dataset,
    hide_index=True,
    use_container_width=True
)

st.write("")

st.info(
"""
The PhiUSIIL Phishing URL Dataset contains both legitimate and phishing URLs
along with numerous URL-based and webpage-based features. It provides a
realistic benchmark for evaluating phishing detection models.
"""
)

st.write("")

# ==========================================================
# FEATURE ENGINEERING
# ==========================================================

st.markdown(
"""
<div class="section-title">
Feature Engineering
</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
The deployed model uses the following engineered features extracted from
each URL.
"""
)

left, right = st.columns(2)

with left:

    st.markdown("""
- URLSimilarityIndex
- URLLength
- IsHTTPS
- LineOfCode
- TLDLegitimateProb
- CharContinuationRate
""")

with right:

    st.markdown("""
- LetterRatioInURL
- NoOfDegitsInURL
- DegitRatioInURL
- NoOfOtherSpecialCharsInURL
- SpacialCharRatioInURL
- LargestLineLength
""")
# ==========================================================
# MODELS USED
# ==========================================================

st.markdown(
"""
<div class="section-title">
Machine Learning Models
</div>
""",
unsafe_allow_html=True
)

models = pd.DataFrame(
    {
        "Model": [
            "Logistic Regression",
            "Random Forest",
            "XGBoost",
            "Soft Voting Ensemble"
        ],
        "Description": [
            "Baseline linear classification model.",
            "Ensemble of decision trees for improved prediction.",
            "Gradient boosting algorithm with excellent performance.",
            "Final deployed model combining all classifiers."
        ]
    }
)

st.dataframe(
    models,
    hide_index=True,
    use_container_width=True
)

st.write("")

st.success(
"""
After evaluating all four models, the **Soft Voting Ensemble** was selected
for deployment because it achieved the best overall balance of Accuracy,
Precision, Recall, F1 Score, and ROC-AUC.
"""
)

st.write("")


# ==========================================================
# TECHNOLOGY STACK
# ==========================================================

st.markdown(
"""
<div class="section-title">
Technology Stack
</div>
""",
unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    st.markdown(
"""
### Programming & Framework

- Python
- Streamlit

### Data Processing

- Pandas
- NumPy
"""
    )

with col2:

    st.markdown(
"""
### Machine Learning

- Scikit-learn
- XGBoost

### Visualization

- Plotly
"""
    )

st.write("")


# ==========================================================
# FUTURE SCOPE
# ==========================================================

st.markdown(
"""
<div class="section-title">
Future Scope
</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
Future improvements that can enhance this project include:

- Integration with real-time URL reputation services.
- Browser extension for instant phishing detection.
- WHOIS and DNS information analysis.
- Explainable AI for prediction interpretation.
- Continuous model retraining using updated datasets.
"""
)

st.write("")


# ==========================================================
# DEVELOPERS
# ==========================================================

st.markdown(
"""
<div class="section-title">
Developers
</div>
""",
unsafe_allow_html=True
)

dev1, dev2 = st.columns(2)

with dev1:

    st.markdown(
"""
### Jiya Sahni

- Frontend Development
- Streamlit Application
- Dashboard Design
"""
    )

with dev2:

    st.markdown(
"""
### Pratishtha

- Dataset Processing
- Machine Learning Models
- Model Evaluation
"""
    )

st.write("")

st.info(
"""
This project was developed as an academic project to demonstrate the use of
machine learning techniques for phishing website detection using URL-based
features and ensemble learning.
"""
)

st.write("")


# ==========================================================
# REFERENCES
# ==========================================================

st.markdown(
"""
<div class="section-title">
References
</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
- **Dataset:** PhiUSIIL Phishing URL Dataset (Kaggle)

- Scikit-learn Documentation

- XGBoost Documentation

- Streamlit Documentation
"""
)

st.write("")
st.divider()

st.caption(
    "Hybrid Phishing Detection System © 2026 | Developed by Jiya Sahni & Pratishtha"
)