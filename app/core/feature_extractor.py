import requests
from difflib import SequenceMatcher
from urllib.parse import urlparse
print("✅ Loaded FeatureExtractor from:", __file__)

class FeatureExtractor:
    """
    Extract phishing-related URL and HTML features
    from a given website.
    """

    SPECIAL_CHARS = "!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/~`"

    def __init__(self, url):
     self.url = url.strip()

    # Automatically prepend https:// if missing
     if not self.url.startswith(("http://", "https://")):
        self.url = "https://" + self.url

     print("Normalized URL:", self.url)

     self.html = None  # Cache HTML after first download

    # ==========================================================
    # URL FEATURES
    # ==========================================================

    def url_length(self):
        return len(self.url)

    def is_https(self):
      return int(urlparse(self.url).scheme.lower() == "https")

    def digit_count(self):
        return sum(c.isdigit() for c in self.url)

    def digit_ratio(self):
        length = len(self.url)
        if length == 0:
            return 0
        return self.digit_count() / length

    def letter_ratio(self):
        length = len(self.url)
        if length == 0:
            return 0

        letters = sum(c.isalpha() for c in self.url)
        return letters / length

    def special_char_count(self):
        return sum(c in self.SPECIAL_CHARS for c in self.url)

    def special_char_ratio(self):
        length = len(self.url)
        if length == 0:
            return 0

        return self.special_char_count() / length

    def char_continuation_rate(self):
        """
        Approximation of CharContinuationRate.
        """

        length = len(self.url)

        if length == 0:
            return 0

        longest = 1
        current = 1

        for i in range(1, length):

            if self.url[i].isalnum() == self.url[i - 1].isalnum():

                current += 1
                longest = max(longest, current)

            else:

                current = 1

        return longest / length

    # ==========================================================
    # HTML FEATURES
    # ==========================================================

    def get_html(self):
        """
        Downloads webpage once and caches it.
        """

        if self.html is not None:
            return self.html

        print(f"\nFetching URL: {self.url}")

        try:
            response = requests.get(
                self.url,
                timeout=10,
                allow_redirects=True,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/126.0 Safari/537.36"
                    )
                }
            )

            print("Status Code:", response.status_code)
            print("Final URL :", response.url)

            response.raise_for_status()
            self.html = response.text

        except requests.RequestException as e:
            print("Request Failed:", e)
            self.html = ""

        return self.html

    def line_count(self):
        html = self.get_html()
        return len(html.splitlines())

    def largest_line(self):

        html = self.get_html()

        lines = html.splitlines()

        if not lines:
            return 0

        return max(len(line) for line in lines)

    # ==========================================================
    # FUTURE FEATURES
    # ==========================================================

    def url_similarity_index(self):
        host = (urlparse(self.url).hostname or "").lower()

        legitimate_domains = [
            "google.com",
            "youtube.com",
            "facebook.com",
            "instagram.com",
            "amazon.com",
            "microsoft.com",
            "apple.com",
            "github.com",
            "linkedin.com",
            "wikipedia.org",
            "netflix.com",
        ]

        best = 0

        for domain in legitimate_domains:
            score = SequenceMatcher(None, host, domain).ratio()

            if score > best:
                best = score

        return round(best * 100, 2)

    def tld_legitimate_prob(self):
        TLD_SCORES = {
            "com": 0.99,
            "org": 0.95,
            "edu": 0.99,
            "gov": 0.99,
            "net": 0.90,
            "io": 0.85,
            "co": 0.80,
            "in": 0.80,
            "xyz": 0.20,
            "top": 0.10,
            "tk": 0.05,
            "ml": 0.05,
            "cf": 0.05,
        }

        host = urlparse(self.url).hostname or ""

        if "." not in host:
            return 0.50

        tld = host.split(".")[-1].lower()
        return TLD_SCORES.get(tld, 0.50)

    # ==========================================================
    # MAIN EXTRACTION
    # ==========================================================

    def extract(self):

        features = {

            "URLSimilarityIndex":
                self.url_similarity_index(),

            "LineOfCode":
                self.line_count(),

            "IsHTTPS":
                self.is_https(),

            "URLLength":
                self.url_length(),

            "TLDLegitimateProb":
                self.tld_legitimate_prob(),

            "CharContinuationRate":
                self.char_continuation_rate(),

            "LetterRatioInURL":
                self.letter_ratio(),

            "NoOfDegitsInURL":
                self.digit_count(),

            "DegitRatioInURL":
                self.digit_ratio(),

            "NoOfOtherSpecialCharsInURL":
                self.special_char_count(),

            "SpacialCharRatioInURL":
                self.special_char_ratio(),

            "LargestLineLength":
                self.largest_line()

        }

        return features


if __name__ == "__main__":

    url = input("Enter URL: ")

    extractor = FeatureExtractor(url)

    features = extractor.extract()

    print("\nExtracted Features:\n")

    for key, value in features.items():
        print(f"{key}: {value}")
