import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


# ============================================================
# Threat Gauge
# ============================================================

def threat_gauge(confidence: float, prediction: str):

    value = confidence * 100

    color = "#10B981" if prediction.lower() == "legitimate" else "#EF4444"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": "%"},
            title={"text": "Confidence"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": color},
                "steps": [
                    {"range": [0, 40], "color": "#3B1F1F"},
                    {"range": [40, 70], "color": "#3F3320"},
                    {"range": [70, 100], "color": "#1C3D32"},
                ],
            },
        )
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        height=350,
        margin=dict(l=20, r=20, t=60, b=20),
    )

    return fig


# ============================================================
# Feature Importance Bar
# ============================================================

def feature_chart(features: dict):

    # Convert DataFrame to dictionary if needed
    if hasattr(features, 'iloc'):
        features = features.iloc[0].to_dict()

    df = pd.DataFrame(
        {
            "Feature": list(features.keys()),
            "Value": list(features.values()),
        }
    )

    fig = px.bar(
        df,
        x="Feature",
        y="Value",
        color="Value",
        color_continuous_scale="Blues",
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        xaxis_title="",
        yaxis_title="Feature Value",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    return fig


# ============================================================
# URL Composition Pie Chart
# ============================================================

def url_composition(features):

    # Convert DataFrame to dictionary if needed
    if hasattr(features, 'iloc'):
        features = features.iloc[0].to_dict()

    labels = [
        "Letters",
        "Digits",
        "Special",
    ]

    values = [
        features["LetterRatioInURL"],
        features["DegitRatioInURL"],
        features["SpacialCharRatioInURL"],
    ]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.55,
            )
        ]
    )

    fig.update_layout(
        template="plotly_dark",
        height=350,
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)",
    )

    return fig