# core/model_loader.py

import joblib
import streamlit as st
from pathlib import Path


class ModelLoader:
    """
    Loads the trained phishing detection model.
    The model is cached so it is loaded only once.
    """

    MODEL_PATH = (
        Path(__file__).resolve().parent.parent.parent
        / "models"
        / "ensemble.pkl"
    )

    @staticmethod
    @st.cache_resource
    def load_model():
        try:
            model = joblib.load(ModelLoader.MODEL_PATH)
            return model

        except FileNotFoundError:
            raise FileNotFoundError(
                f"Model not found at:\n{ModelLoader.MODEL_PATH}"
            )

        except Exception as e:
            raise RuntimeError(
                f"Failed to load model:\n{e}"
            )