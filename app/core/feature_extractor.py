import requests


class FeatureExtractor:
    """
    Extract phishing-related URL and HTML features
    from a given website.
    """

    SPECIAL_CHARS = "!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/~`"

    def __init__(self, url):
        self.url = url.strip()
        self.html = None  # Cache HTML after first download

    # ==========================================================
    # URL FEATURES
    # ==========================================================

    def url_length(self):
        return len(self.url)

    def is_https(self):
        return int(self.url.startswith("https"))

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

        try:

            response = requests.get(
                self.url,
                timeout=10,
                headers={
                    "User-Agent":
                    "Mozilla/5.0"
                }
            )

            response.raise_for_status()

            self.html = response.text

        except requests.RequestException:

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
        """
        TODO:
        Replace placeholder with real implementation.
        """
        return 0

    def tld_legitimate_prob(self):
        """
        TODO:
        Replace placeholder with real implementation.
        """
        return 0

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