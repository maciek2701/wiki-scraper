import re

from bs4 import BeautifulSoup


class ArticleParser:
    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, "html.parser")

    def get_main_content(self):
        root = self.soup.find("div", id="mw-content-text")
        if root is None:
            raise ValueError("Main content root (#mw-content-text) not found")

        content = root.find("div", class_="mw-parser-output")
        if content is None:
            raise ValueError("Main content (.mw-parser-output) not found")

        return content

    def extract_summary(self):
        container = self.get_main_content()

        for p in container.find_all("p"):
            text = p.get_text("", strip=False).strip()

            if text:
                return text

        raise Exception("Summary not found")
