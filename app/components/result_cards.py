import streamlit as st


def show_result_card(prediction: str, confidence: float):

    safe = "legitimate" in prediction.lower()

    card_class = "success-box" if safe else "danger-box"
    result_class = "result-safe" if safe else "result-danger"

    icon = "Safe" if safe else "Phishing"

    subtitle = (
        "The website appears to be safe."
        if safe
        else "This website exhibits phishing characteristics."
    )

    st.markdown(
        f"""
        <div class="{card_class}">
            <div class="{result_class}">
                {icon} {prediction}
            </div>

            <br>

            <b>Confidence</b>

            <h2>{confidence:.2%}</h2>

            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )