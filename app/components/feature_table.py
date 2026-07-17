import pandas as pd
import streamlit as st


def show_feature_table(features: dict):

    # Convert DataFrame to dictionary if needed
    if hasattr(features, 'iloc'):
        features = features.iloc[0].to_dict()

    df = pd.DataFrame(
        {
            "Feature": features.keys(),
            "Value": features.values(),
        }
    )

    styled = (
        df.style
        .hide(axis="index")
        .format({"Value": "{:.4f}"})
        .set_properties(
            **{
                "background-color": "#111827",
                "color": "white",
                "border-color": "#293548",
                "font-size": "15px",
            }
        )
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("background", "#1E293B"),
                        ("color", "white"),
                        ("font-size", "16px"),
                        ("text-align", "left"),
                    ],
                }
            ]
        )
    )

    st.dataframe(
        styled,
        width="stretch",
        height=470,
    )