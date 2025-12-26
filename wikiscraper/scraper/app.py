from pathlib import Path

from wikiscraper.scraper.client import WikiClient
from wikiscraper.scraper.parser import ArticleParser


class WikiScraperApp:
    def summary_from_local_html(self, path: str | Path) -> str:
        html = WikiClient().load_html(path)
        return ArticleParser(html).extract_summary()

    def summary_from_phrase(self, phrase: str) -> str:
        pass
