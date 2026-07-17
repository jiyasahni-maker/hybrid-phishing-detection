# core/feature_extractor.py

import re
import requests
import pandas as pd


class FeatureExtractor:
    """
    Extracts the 10 features required by the phishing detection model.
    """

    FEATURE_ORDER = [
        "LineOfCode",
        "IsHTTPS",
        "URLLength",
        "CharContinuationRate",
        "LetterRatioInURL",
        "NoOfDegitsInURL",
        "DegitRatioInURL",
        "NoOfOtherSpecialCharsInURL",
        "SpacialCharRatioInURL",
        "LargestLineLength",
    ]

    def __init__(self, timeout=5):
        self.timeout = timeout

    # -----------------------------------------------------
    # URL Validation
    # -----------------------------------------------------

    def normalize_url(self, url: str) -> str:
        url = url.strip()

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        return url

    # -----------------------------------------------------
    # Download HTML
    # -----------------------------------------------------

    def download_html(self, url):
        try:
            response = requests.get(
                url,
                timeout=self.timeout,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 "
                        "(Windows NT 10.0; Win64; x64)"
                    )
                },
            )

            return response.text

        except Exception:
            return ""

    # -----------------------------------------------------
    # HTML Features
    # -----------------------------------------------------

    def html_features(self, html):

        if not html:
            return 0, 0

        lines = html.splitlines()

        line_count = len(lines)

        largest_line = max((len(line) for line in lines), default=0)
        
        # Cap largest_line at 1000 to avoid false positives from minified JS
        # Modern websites often have extremely long lines due to minification
        largest_line = min(largest_line, 1000)

        return line_count, largest_line

    # -----------------------------------------------------
    # URL Features
    # -----------------------------------------------------

    def url_features(self, url):

        url_length = len(url)

        is_https = 1 if url.lower().startswith("https://") else 0

        letters = sum(c.isalpha() for c in url)

        digits = sum(c.isdigit() for c in url)

        special = sum(not c.isalnum() for c in url)

        letter_ratio = letters / url_length if url_length else 0

        digit_ratio = digits / url_length if url_length else 0

        special_ratio = special / url_length if url_length else 0

        # --------------------------------------------
        # CharContinuationRate
        # Longest contiguous sequence of alphanumeric
        # characters divided by total URL length
        # --------------------------------------------

        sequences = re.findall(r"[A-Za-z0-9]+", url)

        if sequences:
            longest = max(len(seq) for seq in sequences)
        else:
            longest = 0

        continuation_rate = longest / url_length if url_length else 0

        return {
            "URLLength": url_length,
            "IsHTTPS": is_https,
            "CharContinuationRate": continuation_rate,
            "LetterRatioInURL": letter_ratio,
            "NoOfDegitsInURL": digits,
            "DegitRatioInURL": digit_ratio,
            "NoOfOtherSpecialCharsInURL": special,
            "SpacialCharRatioInURL": special_ratio,
        }

    # -----------------------------------------------------
    # Main Extraction Function
    # -----------------------------------------------------

    def extract(self, url):

        url = self.normalize_url(url)

        html = self.download_html(url)

        line_count, largest_line = self.html_features(html)

        features = self.url_features(url)

        features["LineOfCode"] = line_count
        features["LargestLineLength"] = largest_line

        feature_vector = pd.DataFrame(
            [[features[col] for col in self.FEATURE_ORDER]],
            columns=self.FEATURE_ORDER,
        )

        return feature_vector