import streamlit as st

from core.feature_extractor import FeatureExtractor
from core.predictor import Predictor

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Hybrid Phishing Detection",
    page_icon="🛡️",
    layout="wide"
)

# -------------------------------------------------
# Load Predictor
# -------------------------------------------------

predictor = Predictor()

# -------------------------------------------------
# Title
# -------------------------------------------------

st.title(" Hybrid Phishing Website Detection")

st.write(
    "Analyze suspicious URLs using our Soft Voting Ensemble Machine Learning model."
)

st.divider()

# -------------------------------------------------
# URL Input
# -------------------------------------------------

url = st.text_input(
    "Enter Website URL",
    placeholder="https://example.com"
)

# -------------------------------------------------
# Prediction
# -------------------------------------------------

if st.button("Analyze URL"):

    if url.strip() == "":

        st.warning("Please enter a URL.")

    else:

        with st.spinner("Extracting Features..."):

            extractor = FeatureExtractor(url)

            features = extractor.extract()

        with st.spinner("Running Ensemble Model..."):

            result = predictor.predict(features)

        st.success("Analysis Complete!")

        st.divider()

        # -----------------------------------------
        # Results
        # -----------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Prediction",
                result["label"]
            )

        with col2:

            st.metric(
                "Confidence",
                f'{result["confidence"]}%'
            )

        with col3:

            st.metric(
                "Threat Level",
                result["threat_level"]
            )

        st.divider()

        st.subheader("Extracted Features")

        st.json(features)