def __init__(self, url):

    self.url = url.strip()

    # Automatically prepend https:// if the user didn't enter it
    if not self.url.startswith(("http://", "https://")):
        self.url = "https://" + self.url

    self.html = None
def __init__(self, url):

    self.url = url.strip()

    if not self.url.startswith(("http://", "https://")):
        self.url = "https://" + self.url

    print("Normalized URL:", self.url)

    self.html = None