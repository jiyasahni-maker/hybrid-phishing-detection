import re
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# URL parsing and HTML parsing imports are available for future feature
# extraction improvements such as domain analysis, TLD checks, and page
# content parsing.

class FeatureExtractor:
    """Class for extracting phishing-relevant features from a given URL."""

    def __init__(self, url):
        # Store the URL to analyze.
        self.url = url

    def extract(self):
        # Placeholder method for class-based extraction. This currently returns
        # an empty dict but can be extended to call the helper functions below.
        features = {}
        return features

# ---------------------------------------------------------------------------
# URL feature helper functions
# These functions are defined at module level and are designed to operate on
# objects that expose a .url attribute (for example, a FeatureExtractor
# instance).
# ---------------------------------------------------------------------------

def url_length(self):
    """Return the total number of characters in the URL."""
    return len(self.url)


def is_https(self):
    """Return 1 if the URL begins with HTTPS, otherwise return 0."""
    return int(self.url.startswith("https"))


def digit_count(self):
    """Return the number of numeric digits contained in the URL."""
    return sum(c.isdigit() for c in self.url)


def digit_ratio(self):
    """Return the ratio of digits to total URL length."""
    digits = self.digit_count()
    length = len(self.url)
    if length == 0:
        return 0
    return digits / length


def letter_ratio(self):
    """Return the ratio of alphabetic characters to total URL length."""
    letters = sum(c.isalpha() for c in self.url)
    return letters / len(self.url)

# Characters considered as special characters for the URL features.
SPECIAL = r"!@#$%^&*()_+-={}[]|\\:;\"'<>,.?/~`"

def special_char_count(self):
    """Return the number of special characters in the URL."""
    return sum(c in SPECIAL for c in self.url)


def special_char_ratio(self):
    """Return the ratio of special characters to total URL length."""
    return self.special_char_count() / len(self.url)


def char_continuation_rate(self):
    """Return the longest contiguous same-type character run rate in the URL."""
    longest = 1
    current = 1

    for i in range(1, len(self.url)):
        if self.url[i].isalnum() == self.url[i - 1].isalnum():
            current += 1
            longest = max(longest, current)
        else:
            current = 1

    return longest / len(self.url)


def get_html(self):
    """Download the HTML content for the URL, returning an empty string on error."""
    try:
        response = requests.get(
            self.url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        return response.text
    except:
        return ""


def line_count(self):
    """Return the number of lines in the downloaded HTML content."""
    html = self.get_html()
    return len(html.splitlines())


def largest_line(self):
    """Return the length of the longest line in the downloaded HTML."""
    html = self.get_html()
    lines = html.splitlines()
    if len(lines) == 0:
        return 0
    return max(len(line) for line in lines)


def extract(self):
    """Return a dictionary of extracted URL features for phishing detection."""
    return {
        "URLLength": self.url_length(),
        "IsHTTPS": self.is_https(),
        "NoOfDegitsInURL": self.digit_count(),
        "DegitRatioInURL": self.digit_ratio(),
        "LetterRatioInURL": self.letter_ratio(),
        "NoOfOtherSpecialCharsInURL": self.special_char_count(),
        "SpacialCharRatioInURL": self.special_char_ratio(),
        "CharContinuationRate": self.char_continuation_rate(),
        "LineOfCode": self.line_count(),
        "LargestLineLength": self.largest_line(),
        "URLSimilarityIndex": 0,
        "TLDLegitimateProb": 0,
    }
