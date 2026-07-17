import streamlit as st

from core.feature_extractor import FeatureExtractor
from core.predictor import Predictor

from components.result_cards import show_result_cards
from components.feature_table import show_feature_table

from pathlib import Path

def load_css():
    css_file = Path(__file__).parent / "assets" / "styles.css"

    with open(css_file) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )

load_css()
# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="PHANTOM",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------------

@st.cache_resource
def load_predictor():
    return Predictor()


predictor = load_predictor()


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown("""
#  PHANTOM

### Hybrid Ensemble-Based Phishing Website Detection
""")

st.markdown("""
Analyze suspicious URLs using a machine learning ensemble consisting of **Logistic Regression**, **Random Forest**, and **XGBoost** classifiers.

Enter a URL below to generate a phishing prediction and inspect the extracted security features.
""")

st.divider()

st.caption("Hybrid Ensemble-Based Phishing Website Detection")

st.write(
    """
Analyze suspicious websites using a **Soft Voting Ensemble Machine Learning Model**
built with **Logistic Regression**, **Random Forest**, and **XGBoost** classifiers.

Enter any website URL below to generate a phishing prediction along with the
extracted URL and webpage features.
"""
)

st.divider()


# ---------------------------------------------------------
# URL INPUT
# ---------------------------------------------------------

left, right = st.columns([6, 1])

with left:

    url = st.text_input(
        label="Website URL",
        placeholder="https://example.com",
        label_visibility="collapsed"
    )

with right:

    analyze = st.button(
        "Analyze",
        use_container_width=True
    )


# ---------------------------------------------------------
# PREDICTION
# ---------------------------------------------------------

if analyze:

    if not url.strip():

        st.warning("Please enter a valid URL.")

    else:

        progress = st.progress(
            0,
            text="Starting analysis..."
        )

        try:

            progress.progress(
                20,
                text="Extracting URL features..."
            )

            extractor = FeatureExtractor(url)

            features = extractor.extract()

            progress.progress(
                60,
                text="Running ensemble model..."
            )

            result = predictor.predict(features)

            progress.progress(
                100,
                text="Generating report..."
            )

            progress.empty()

            st.success("Analysis Complete")

            st.divider()

            # --------------------------------------------
            # RESULT CARDS
            # --------------------------------------------

            show_result_cards(result)

            st.divider()

            # --------------------------------------------
            # FEATURE TABLE
            # --------------------------------------------

            show_feature_table(features)

        except Exception as e:

            progress.empty()

            st.error("Unable to analyze the provided URL.")

            with st.expander("Error Details"):

                st.code(str(e))


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.title(" PHANTOM")

    st.markdown("---")

    st.markdown(
        """
### Hybrid Ensemble

This application detects phishing websites using:

- Logistic Regression
- Random Forest
- XGBoost
- Soft Voting Ensemble

---

Navigate using the pages above.
"""
    )

    st.markdown("---")

    st.caption("Version 1.0")
