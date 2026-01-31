from pathlib import Path

import requests


#### Jesli sie pozniej wywali to przywrocic stary konstruktor
class WikiClient:
    """Simple HTTP/file client for retrieving article HTML."""

    def load_html(self, path: str | Path) -> str:
        """Load HTML from a local file path."""
        path = Path(path)
        ### check if file exists
        if not path.exists():
            raise Exception(f"File {path} does not exist")
        return path.read_text(encoding="utf-8")

    def fetch_html(
        self, phrase: str, base: str = "https://bulbapedia.bulbagarden.net/wiki/"
    ) -> str:
        """Fetch HTML for the given phrase from the configured base URL."""
        phrase = "_".join(phrase.split())
        url = base + phrase

        response = requests.get(url)

        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to fetch HTML: {response.status_code} at {url}")
