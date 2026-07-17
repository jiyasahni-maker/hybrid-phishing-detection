import pandas as pd
import streamlit as st


def show_feature_table(features):

    st.subheader("Extracted Features")

    df = pd.DataFrame(
        {
            "Feature": list(features.keys()),
            "Value": list(features.values())
        }
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=500
    )