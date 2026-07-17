# core/predictor.py

from core.feature_extractor import FeatureExtractor
from core.model_loader import ModelLoader
from urllib.parse import urlparse


class PhishingPredictor:
    """
    Complete phishing prediction pipeline.

    Workflow:
    URL
      ↓
    Check Whitelist (known legitimate domains)
      ↓
    Feature Extraction
      ↓
    Model Prediction
      ↓
    Confidence Calculation
      ↓
    Threat Level
    """

    # Whitelist of known legitimate, high-reputation domains
    # These are verified to prevent false positives
    LEGITIMATE_DOMAINS_WHITELIST = {
        "youtube.com", "www.youtube.com",
        "google.com", "www.google.com",
        "github.com", "www.github.com",
        "wikipedia.org", "www.wikipedia.org",
        "stackoverflow.com", "www.stackoverflow.com",
        "amazon.com", "www.amazon.com",
        "facebook.com", "www.facebook.com",
        "instagram.com", "www.instagram.com",
        "twitter.com", "www.twitter.com",
        "reddit.com", "www.reddit.com",
        "linkedin.com", "www.linkedin.com",
        "microsoft.com", "www.microsoft.com",
        "apple.com", "www.apple.com",
        "mozilla.org", "www.mozilla.org",
        "w3schools.com", "www.w3schools.com",
        "github.io", 
    }

    def __init__(self):
        self.extractor = FeatureExtractor()
        self.model = ModelLoader.load_model()

    def _is_whitelisted(self, url: str) -> bool:
        """Check if URL belongs to a whitelisted domain."""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Check exact match
            if domain in self.LEGITIMATE_DOMAINS_WHITELIST:
                return True
            
            # Check if any whitelisted domain is a suffix (for subdomains)
            for whitelisted in self.LEGITIMATE_DOMAINS_WHITELIST:
                if domain.endswith("." + whitelisted) or domain == whitelisted:
                    return True
            
            return False
        except Exception:
            return False

    def predict(self, url):
        """
        Predict whether a URL is phishing or legitimate.

        Returns
        -------
        dict
            {
                prediction,
                label,
                confidence,
                probability,
                features
            }
        """

        # Always extract features (needed for display)
        features = self.extractor.extract(url)

        # Check whitelist first (but still show features)
        if self._is_whitelisted(url):
            return {
                "prediction": 1,
                "label": "Legitimate Website",
                "confidence": 99.99,
                "phishing_probability": 0.01,
                "legitimate_probability": 99.99,
                "threat": "Low",
                "color": "green",
                "features": features,
            }

        # Remove HTML-based features that cause false positives on modern websites
        # Modern websites load content dynamically, so initial HTML is minimal
        features_for_model = features.drop(columns=["LineOfCode", "LargestLineLength"], errors="ignore")

        # -----------------------------
        # Prediction
        # -----------------------------
        prediction = int(self.model.predict(features_for_model)[0])

        # -----------------------------
        # Probability
        # -----------------------------
        probability = self.model.predict_proba(features_for_model)[0]

        phishing_probability = float(probability[0])
        legitimate_probability = float(probability[1])

        confidence = max(probability) * 100

        # -----------------------------
        # Label Mapping
        # -----------------------------
        if prediction == 1:
            label = "Legitimate Website"
            threat = "Low"
            color = "green"

        else:
            label = "Phishing Website"
            threat = "High"
            color = "red"

        # -----------------------------
        # Return everything
        # -----------------------------
        return {
            "prediction": prediction,
            "label": label,
            "confidence": round(confidence, 2),
            "phishing_probability": round(phishing_probability * 100, 2),
            "legitimate_probability": round(
                legitimate_probability * 100, 2
            ),
            "threat": threat,
            "color": color,
            "features": features,
        }