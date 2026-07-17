import streamlit as st
import pandas as pd
from pathlib import Path

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Model Evaluation",
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
        unsafe_allow_html=True,
    )

# ==========================================================
# METRICS
# ==========================================================

metrics = {
    "Logistic Regression": {
        "Accuracy": 99.7922,
        "Precision": 99.7445,
        "Recall": 99.8925,
        "F1": 99.8185,
        "ROC": 99.9759
    },
    "Random Forest": {
        "Accuracy": 99.9724,
        "Precision": 99.9852,
        "Recall": 99.9852,
        "F1": 99.9666,
        "ROC": 99.9759
    },
    "XGBoost": {
        "Accuracy": 99.9788,
        "Precision": 99.9778,
        "Recall": 99.9852,
        "F1": 99.9815,
        "ROC": 99.9996
    },
    "Soft Voting Ensemble": {
        "Accuracy": 99.9788,
        "Precision": 99.9815,
        "Recall": 99.9815,
        "F1": 99.9815,
        "ROC": 99.9996
    }
}

# ==========================================================
# HERO
# ==========================================================

st.markdown(
"""
<div class="main-title">
Model Evaluation
</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div class="subtitle">
Performance comparison of multiple machine learning algorithms used for phishing website detection.
</div>
""",
unsafe_allow_html=True
)

st.write("")

# ==========================================================
# SELECTED MODEL
# ==========================================================

st.markdown(
"""
<div class="section-title">
Final Selected Model
</div>
""",
unsafe_allow_html=True
)

st.success(
"""
### Soft Voting Ensemble

The Soft Voting Ensemble was selected as the final deployment model because it
achieved the best overall balance of Accuracy, Precision, Recall, F1 Score,
and ROC-AUC while combining the strengths of multiple classifiers.
"""
)

st.write("")

# ==========================================================
# METRIC CARDS
# ==========================================================

ensemble = metrics["Soft Voting Ensemble"]

c1, c2, c3, c4, c5 = st.columns(5)

cards = [
    ("Accuracy", ensemble["Accuracy"]),
    ("Precision", ensemble["Precision"]),
    ("Recall", ensemble["Recall"]),
    ("F1 Score", ensemble["F1"]),
    ("ROC-AUC", ensemble["ROC"])
]

for col, (title, value) in zip([c1, c2, c3, c4, c5], cards):

    with col:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-title">
                    {title}
                </div>

                <div class="metric-value">
                    {value:.2f}%
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

st.write("")
st.write("")

# ==========================================================
# MODEL COMPARISON TABLE
# ==========================================================

st.markdown(
"""
<div class="section-title">
Model Comparison
</div>
""",
unsafe_allow_html=True
)

comparison_df = pd.DataFrame(
    {
        "Model": [
            "Logistic Regression",
            "Random Forest",
            "XGBoost",
            "Soft Voting Ensemble"
        ],
        "Accuracy (%)": [
            99.7922,
            99.9724,
            99.9788,
            99.9788
        ],
        "Precision (%)": [
            99.7445,
            99.9852,
            99.9778,
            99.9815
        ],
        "Recall (%)": [
            99.8925,
            99.9852,
            99.9852,
            99.9815
        ],
        "F1 Score (%)": [
            99.8185,
            99.9666,
            99.9815,
            99.9815
        ],
        "ROC-AUC (%)": [
            99.9759,
            99.9759,
            99.9996,
            99.9996
        ]
    }
)

st.dataframe(
    comparison_df,
    use_container_width=True,
    hide_index=True
)

st.write("")
st.write("")

# ==========================================================
# MODEL ANALYSIS
# ==========================================================

st.markdown(
"""
<div class="section-title">
Individual Model Analysis
</div>
""",
unsafe_allow_html=True
)

tabs = st.tabs(
    [
        "Logistic Regression",
        "Random Forest",
        "XGBoost",
        "Soft Voting Ensemble"
    ]
)
# ==========================================================
# LOGISTIC REGRESSION
# ==========================================================

with tabs[0]:

    st.subheader("Logistic Regression")

    st.write(
        """
        Logistic Regression serves as a strong baseline classifier. It estimates
        the probability of a website being legitimate or phishing using a
        linear decision boundary over the extracted URL and webpage features.
        """
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Accuracy", "99.79%")
    c2.metric("Precision", "99.74%")
    c3.metric("Recall", "99.89%")
    c4.metric("F1 Score", "99.82%")
    c5.metric("ROC-AUC", "99.98%")

    st.divider()

    img1, img2 = st.columns(2)

    with img1:
        st.markdown("#### Confusion Matrix")
        st.image(
            "app/assets/figures/confusion_matrix_lr.png",
            use_container_width=True
        )

    with img2:
        st.markdown("#### ROC Curve")
        st.image(
            "app/assets/figures/roc_lr.png",
            use_container_width=True
        )


# ==========================================================
# RANDOM FOREST
# ==========================================================

with tabs[1]:

    st.subheader("Random Forest")

    st.write(
        """
        Random Forest combines multiple decision trees to reduce variance and
        improve prediction stability. It performed exceptionally well on the
        phishing detection dataset and served as one of the strongest
        individual classifiers.
        """
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Accuracy", "99.97%")
    c2.metric("Precision", "99.99%")
    c3.metric("Recall", "99.99%")
    c4.metric("F1 Score", "99.97%")
    c5.metric("ROC-AUC", "99.98%")

    st.divider()

    img1, img2 = st.columns(2)

    with img1:

        st.markdown("#### Confusion Matrix")

        st.image(
            "app/assets/figures/confusion_matrix_random_forest.png",
            use_container_width=True
        )

    with img2:

        st.markdown("#### ROC Curve")

        st.image(
            "app/assets/figures/roc_rf.png",
            use_container_width=True
        )


# ==========================================================
# XGBOOST
# ==========================================================

with tabs[2]:

    st.subheader("XGBoost")

    st.write(
        """
        XGBoost is a gradient boosting algorithm that builds trees
        sequentially while correcting previous errors. It achieved one of the
        highest overall performances among all evaluated models.
        """
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Accuracy", "99.98%")
    c2.metric("Precision", "99.98%")
    c3.metric("Recall", "99.99%")
    c4.metric("F1 Score", "99.98%")
    c5.metric("ROC-AUC", "100.00%")

    st.divider()

    img1, img2 = st.columns(2)

    with img1:

        st.markdown("#### Confusion Matrix")

        st.image(
            "app/assets/figures/confusion_matrix_xgb.png",
            use_container_width=True
        )

    with img2:

        st.markdown("#### ROC Curve")

        st.image(
            "app/assets/figures/roc_xgb.png",
            use_container_width=True
        )


# ==========================================================
# SOFT VOTING ENSEMBLE
# ==========================================================

with tabs[3]:

    st.subheader("Soft Voting Ensemble")

    st.success(
        """
        **Selected Deployment Model**

        The Soft Voting Ensemble combines the prediction probabilities from
        Logistic Regression, Random Forest, and XGBoost to produce a more
        robust final prediction. By leveraging the strengths of multiple
        classifiers, it achieved the best balance across all evaluation
        metrics and was selected for deployment in the phishing detection
        application.
        """
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Accuracy", "99.98%")
    c2.metric("Precision", "99.98%")
    c3.metric("Recall", "99.98%")
    c4.metric("F1 Score", "99.98%")
    c5.metric("ROC-AUC", "100.00%")

    st.divider()

    img1, img2 = st.columns(2)

    with img1:

        st.markdown("#### Confusion Matrix")

        st.image(
            "app/assets/figures/confusion_matrix_ensemble.png",
            use_container_width=True
        )

    with img2:

        st.markdown("#### ROC Curve")

        st.image(
            "app/assets/figures/roc_ensemble.png",
            use_container_width=True
        )
# ==========================================================
# SUMMARY
# ==========================================================

st.write("")
st.write("")

st.markdown(
    """
<div class="section-title">
Key Findings
</div>
""",
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:

    st.info(
        """
### Model Performance Summary

- Logistic Regression established a strong baseline with excellent classification performance.

- Random Forest significantly improved prediction stability by leveraging multiple decision trees.

- XGBoost achieved the highest individual model performance, demonstrating exceptional discriminative capability.

- The Soft Voting Ensemble combined the strengths of all individual classifiers, resulting in the most balanced and reliable performance across every evaluation metric.
"""
    )

with col2:

    st.success(
        """
### Deployment Decision

The **Soft Voting Ensemble** was selected as the production model because it offers:

- Highest overall Accuracy
- Excellent Precision
- Excellent Recall
- Outstanding F1 Score
- Near-perfect ROC-AUC

By combining predictions from Logistic Regression, Random Forest, and XGBoost, the ensemble minimizes individual model weaknesses while improving overall robustness.
"""
    )

st.write("")
st.write("")

# ==========================================================
# TECHNICAL OVERVIEW
# ==========================================================

st.markdown(
    """
<div class="section-title">
Technical Overview
</div>
""",
    unsafe_allow_html=True,
)

tech_col1, tech_col2 = st.columns(2)

with tech_col1:

    st.markdown(
        """
### Models Evaluated

- Logistic Regression
- Random Forest
- XGBoost
- Soft Voting Ensemble
"""
    )

with tech_col2:

    st.markdown(
        """
### Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- Confusion Matrix
"""
    )

st.write("")
st.write("")

# ==========================================================
# PROJECT HIGHLIGHTS
# ==========================================================

st.markdown(
    """
<div class="section-title">
Project Highlights
</div>
""",
    unsafe_allow_html=True,
)

highlight1, highlight2, highlight3 = st.columns(3)

with highlight1:

    st.markdown(
        """
<div class="metric-card">

<div class="metric-title">
Models Tested
</div>

<div class="metric-value">
4
</div>

</div>
""",
        unsafe_allow_html=True,
    )

with highlight2:

    st.markdown(
        """
<div class="metric-card">

<div class="metric-title">
Features Used
</div>

<div class="metric-value">
11
</div>

</div>
""",
        unsafe_allow_html=True,
    )

with highlight3:

    st.markdown(
        """
<div class="metric-card">

<div class="metric-title">
Final Model
</div>

<div class="metric-value">
Ensemble
</div>

</div>
""",
        unsafe_allow_html=True,
    )

st.write("")
st.write("")

# ==========================================================
# CONCLUSION
# ==========================================================

st.markdown(
    """
<div class="section-title">
Conclusion
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
The evaluation demonstrates that all implemented machine learning models achieved exceptional performance in detecting phishing websites. Among them, the **Soft Voting Ensemble** delivered the most consistent results by combining the predictive strengths of Logistic Regression, Random Forest, and XGBoost.

Its superior Accuracy, Precision, Recall, F1 Score, and ROC-AUC make it the most suitable choice for deployment within the Hybrid Phishing Detection System.
"""
)

st.write("")
st.divider()

st.caption(
    "Hybrid Phishing Detection System - Model Evaluation Dashboard - Built with Streamlit, Scikit-learn and Plotly"
)