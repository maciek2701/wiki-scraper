from wikiscraper.analysis.words import WordCounter
from wikiscraper.scraper.client import WikiClient
from wikiscraper.scraper.parser import ArticleParser


class WikiScraperApp:
    def __init__(self, **kwargs):
        self.path = kwargs.get("path")

    def _load_html(self) -> str:
        if self.path is not None:
            return WikiClient().load_html(self.path)
        return WikiClient().fetch_html(self.phrase)

    def summary(self, phrase) -> str:
        self.phrase = phrase
        html = self._load_html()
        return ArticleParser(html).extract_summary()

    def count_words(self, phrase) -> None:
        self.phrase = phrase
        html = self._load_html()
        text = ArticleParser(html).extract_article_text()
        WordCounter().run(text)
