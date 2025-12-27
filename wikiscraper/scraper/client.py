from pathlib import Path

import requests


class WikiClient:
    def __init__(self):
        self.base = "https://bulbapedia.bulbagarden.net/wiki/"

    def load_html(self, path: str | Path):
        self.path = Path(path)
        return self.path.read_text(encoding="utf-8")

    def fetch_html(self, phrase: str):
        self.phrase = "_".join(phrase.split(" "))
        url = self.base + self.phrase

        response = requests.get(url)

        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to fetch HTML: {response.status_code}")
