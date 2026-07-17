import streamlit as st
import time

from core.predictor import PhishingPredictor 
from components.feature_table import show_feature_table
from components.result_cards import show_result_card
from core.visualizer import (
    threat_gauge,
    feature_chart,
    url_composition,
)

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
    page_title="Dashboard",
    page_icon=None,
    layout="wide"
)

# -------------------------------------------------------
# LOAD CSS
# -------------------------------------------------------

with open("app/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -------------------------------------------------------
# HERO
# -------------------------------------------------------

st.markdown(
    """
    <div class="main-title">
         Hybrid Phishing Detection
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        AI Powered Website Threat Intelligence
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# -------------------------------------------------------
# INPUT CARD
# -------------------------------------------------------

st.markdown('<div class="glass-card">', unsafe_allow_html=True)

url = st.text_input(
    "Enter URL",
    placeholder="https://example.com",
    label_visibility="collapsed"
)

scan = st.button("Analyze URL")

st.markdown("</div>", unsafe_allow_html=True)

st.write("")
st.write("")

# -------------------------------------------------------
# SCAN
# -------------------------------------------------------

if scan:

    if url == "":
        st.warning("Please enter a URL.")
        st.stop()

    with st.spinner("Analyzing website..."):

        predictor = PhishingPredictor()

        result = predictor.predict(url)

        time.sleep(0.5)

    prediction = result["prediction"]
    label = result["label"]
    confidence = result["confidence"]
    features = result["features"]

    # ---------------------------------------------------
    # RESULT
    # ---------------------------------------------------

    show_result_card(label, confidence)

    st.write("")

    # ---------------------------------------------------
    # METRICS
    # ---------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Confidence</div>
                <div class="metric-value">{confidence:.2%}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        https = "Yes" if features["IsHTTPS"].iloc[0] else "No"

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">HTTPS</div>
                <div class="metric-value">{https}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">URL Length</div>
                <div class="metric-value">
                    {features["URLLength"].iloc[0]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Special Chars</div>
                <div class="metric-value">
                    {features["NoOfOtherSpecialCharsInURL"].iloc[0]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    st.write("")

    # ---------------------------------------------------
    # FEATURE TABLE
    # ---------------------------------------------------

    st.markdown(
        """
        <div class="section-title">
            Feature Analysis
        </div>
        """,
        unsafe_allow_html=True
    )

    show_feature_table(features)

    st.markdown(
        """
        <div class="section-title">
            Threat Visualization
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            threat_gauge(confidence, label),
            width="stretch",
        )

    with col2:
        st.plotly_chart(
            url_composition(features),
            width="stretch",
        )

    st.plotly_chart(
        feature_chart(features),
        width="stretch",
    )

    st.write("")