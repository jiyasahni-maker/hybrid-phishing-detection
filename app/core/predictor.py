"""
predictor.py
-------------
Loads the trained ensemble model and performs phishing prediction
using extracted URL and HTML features.
"""

from pathlib import Path
import joblib
import pandas as pd
from .model_loader import MODEL

class Predictor:
    """
    Loads the trained ensemble model and predicts
    whether a URL is phishing or legitimate.
    """

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self):

        # Project root directory
        self.base_dir = Path(__file__).resolve().parents[2]

        # Model location
        self.model_path = self.base_dir / "models" / "ensemble.pkl"

        # Load model only once
        self.model = MODEL

        # IMPORTANT:
        # Feature order MUST match the training dataset exactly.
        self.feature_order = [

            "URLSimilarityIndex",

            "LineOfCode",

            "IsHTTPS",

            "URLLength",

            "TLDLegitimateProb",

            "CharContinuationRate",

            "LetterRatioInURL",

            "NoOfDegitsInURL",

            "DegitRatioInURL",

            "NoOfOtherSpecialCharsInURL",

            "SpacialCharRatioInURL",

            "LargestLineLength"

        ]

    # ==========================================================
    # PRIVATE HELPER
    # ==========================================================

    def _prepare_dataframe(self, features: dict) -> pd.DataFrame:
        """
        Converts extracted feature dictionary into a
        DataFrame with the correct column order.
        """

        df = pd.DataFrame([features])

        df = df[self.feature_order]

        return df

    # ==========================================================
    # PREDICTION
    # ==========================================================

    def predict(self, features: dict):
        """
        Predict phishing or legitimate.

        Parameters
        ----------
        features : dict
            Feature dictionary returned by FeatureExtractor.

        Returns
        -------
        dict
        """

        df = self._prepare_dataframe(features)

        prediction = self.model.predict(df)[0]

        probabilities = self.model.predict_proba(df)[0]

        confidence = float(max(probabilities))

        phishing_probability = float(probabilities[0])

        legitimate_probability = float(probabilities[1])

        if prediction == 1:

            label = "Legitimate"

        else:

            label = "Phishing"

        # Threat Level
        if confidence >= 0.99:

            threat = "Very Low"

        elif confidence >= 0.95:

            threat = "Low"

        elif confidence >= 0.85:

            threat = "Medium"

        elif confidence >= 0.70:

            threat = "High"

        else:

            threat = "Very High"

        return {

            "prediction": int(prediction),

            "label": label,

            "confidence": round(confidence * 100, 2),

            "threat_level": threat,

            "phishing_probability": round(phishing_probability * 100, 2),

            "legitimate_probability": round(legitimate_probability * 100, 2)

        }


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    sample_features = {

        "URLSimilarityIndex": 100,

        "LineOfCode": 400,

        "IsHTTPS": 1,

        "URLLength": 28,

        "TLDLegitimateProb": 0.52,

        "CharContinuationRate": 0.91,

        "LetterRatioInURL": 0.61,

        "NoOfDegitsInURL": 1,

        "DegitRatioInURL": 0.03,

        "NoOfOtherSpecialCharsInURL": 2,

        "SpacialCharRatioInURL": 0.07,

        "LargestLineLength": 900

    }

    predictor = Predictor()

    result = predictor.predict(sample_features)

    print("\nPrediction Result\n")

    for key, value in result.items():
        print(f"{key}: {value}")