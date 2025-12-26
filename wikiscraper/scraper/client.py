from pathlib import Path


class WikiClient:
    def __init__(self, path):
        self.path = Path(path).read_text(encoding="utf-8")

    def load_html(self):
        with open(self.path, "r") as file:
            return file.read()
