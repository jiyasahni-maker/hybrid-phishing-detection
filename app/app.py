import streamlit as st
from pathlib import Path

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Hybrid Phishing Detection",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# LOAD CSS
# -----------------------------

css_path = Path(__file__).parent / "assets" / "styles.css"

with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.markdown("# Hybrid Phishing")

    st.caption("AI Powered Threat Detection")

    st.divider()

    st.markdown(
        """
### Navigation

- Dashboard
- Model
- Research
"""
    )

    st.divider()

    st.info(
        """
Built using

- Streamlit
- Scikit-Learn
- Plotly
- BeautifulSoup
"""
    )

# -----------------------------
# HOME PAGE
# -----------------------------

st.markdown(
    """
<div class="main-title">
 Hybrid Phishing Detection System
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="subtitle">
Detect phishing websites using machine learning and intelligent feature extraction.
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("---")

st.markdown(
    """
### Welcome

Use the navigation panel on the left to access:

- **Dashboard** – Scan URLs for phishing detection
- **Model** – Explore model performance and evaluation metrics
- **Research** – Learn about the methodology, dataset, and implementation
"""
)