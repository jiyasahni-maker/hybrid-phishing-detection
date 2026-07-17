"""
predictor.py
-------------
Loads the trained ensemble model and performs phishing prediction
using extracted URL and HTML features.
"""

from pathlib import Path
import pandas as pd
from .model_loader import MODEL
def predict(self, features):

    print("\n\n========== PREDICT FUNCTION CALLED ==========\n")

    df = self._prepare_dataframe(features)

    print(df)

class Predictor:
    """
    Loads the trained ensemble model and predicts
    whether a URL is phishing or legitimate.
    """

    def __init__(self):

        self.base_dir = Path(__file__).resolve().parents[2]

        self.model_path = self.base_dir / "models" / "ensemble.pkl"

        self.model = MODEL

        # Feature order MUST match training
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
            "LargestLineLength",
        ]

    # ==========================================================
    # PRIVATE HELPER
    # ==========================================================

    def _prepare_dataframe(self, features):

        df = pd.DataFrame([features])

        df = df[self.feature_order]

        return df

    # ==========================================================
    # PREDICTION
    # ==========================================================

    def predict(self, features):

        df = self._prepare_dataframe(features)

        # ---------------- DEBUG ----------------

        print("\n" + "=" * 70)
        print("INPUT FEATURES")
        print("=" * 70)
        print(df.T)

        # ---------------------------------------

        prediction = self.model.predict(df)[0]

        probabilities = self.model.predict_proba(df)[0]

        print("\n" + "=" * 70)
        print("MODEL OUTPUT")
        print("=" * 70)
        print("Prediction Class :", prediction)
        print("Model Classes    :", self.model.classes_)
        print("Probabilities    :", probabilities)
        print("=" * 70 + "\n")

        confidence = float(max(probabilities))

        phishing_probability = float(probabilities[0])

        legitimate_probability = float(probabilities[1])

        # DO NOT CHANGE YET
        # We'll verify this after seeing the debug output.

        if prediction == 1:
            label = "Legitimate"
        else:
            label = "Phishing"

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
            "legitimate_probability": round(legitimate_probability * 100, 2),
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
        "LargestLineLength": 900,
    }

    predictor = Predictor()

    result = predictor.predict(sample_features)

    print("\nPrediction Result\n")

    for key, value in result.items():
        print(f"{key}: {value}")