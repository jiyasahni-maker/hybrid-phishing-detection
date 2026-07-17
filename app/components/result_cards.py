import streamlit as st


def card(title, value, color):
    return f"""
    <div class="dashboard-card">
        <div class="card-title">{title}</div>
        <div class="card-value" style="color:{color};">
            {value}
        </div>
    </div>
    """


def show_result_cards(result):

    prediction = result["label"]
    confidence = result["confidence"]
    threat = result["threat_level"]

    if prediction.lower() == "legitimate":
        prediction_text = " Legitimate"
        prediction_color = "#22C55E"
    else:
        prediction_text = " Phishing"
        prediction_color = "#EF4444"

    if threat.upper() == "LOW":
        threat_color = "#22C55E"
    elif threat.upper() == "MEDIUM":
        threat_color = "#F59E0B"
    else:
        threat_color = "#EF4444"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            card(
                "Prediction",
                prediction_text,
                prediction_color
            ),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            card(
                "Confidence",
                f"{confidence:.2f}%",
                "#38BDF8"
            ),
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            card(
                "Threat Level",
                threat,
                threat_color
            ),
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            card(
                "Model",
                "Soft Voting",
                "#A78BFA"
            ),
            unsafe_allow_html=True
        )