from typing import Optional

import pandas as pd

from wikiscraper.analysis.table import save_table_csv, value_freqs
from wikiscraper.analysis.words import RelativeFrequencyAnalyzer, WordCounter
from wikiscraper.scraper.client import WikiClient
from wikiscraper.scraper.crawler import AutoCrawler
from wikiscraper.scraper.parser import ArticleParser


class WikiScraperApp:
    """High-level convenience interface for scraping and analysis workflows."""

    def __init__(self, **kwargs) -> None:
        """Initialize the app with optional configuration.

        Args:
            **kwargs: Optional settings. Currently supports `path` for local HTML.
        """
        self.path: Optional[str] = kwargs.get("path")
        self.phrase: Optional[str] = None

    def _load_html(self) -> str:
        """Load HTML either from a local path or by fetching a phrase."""
        if self.path is not None:
            return WikiClient().load_html(self.path)
        return WikiClient().fetch_html(self.phrase)

    def summary(self, phrase: str) -> str:
        """Fetch an article summary for the given phrase."""
        self.phrase = phrase
        html = self._load_html()
        return ArticleParser(html).extract_summary()

    def count_words(self, phrase: str) -> dict[str, int]:
        """Count word frequencies in the article text and persist totals."""
        self.phrase = phrase
        html = self._load_html()
        text = ArticleParser(html).extract_article_text()
        return WordCounter().run(text)

    def run_table(
        self,
        phrase: str,
        nr: int,
        first_row_as_header: bool = False,
        display: bool = True,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Extract a table and optionally print and persist its summary."""
        self.phrase = phrase
        html = self._load_html()
        parser = ArticleParser(html)
        df = parser.extract_table_with_pandas(
            nr, first_row_is_header=first_row_as_header
        )

        if display:
            print("=== TABLE ===")
            print(df)
            save_table_csv(df, phrase)
            print("\n=== VALUE FREQUENCIES ===")
            print(value_freqs(df))
        return df, value_freqs(df)

    def analyze_relative_frequencies(
        self, mode: str, count: int, chart: bool
    ) -> pd.DataFrame:
        """Analyze relative word frequencies versus language statistics."""
        count_dict = WordCounter("./word-counts.json").load_counts()
        analyser = RelativeFrequencyAnalyzer(count_dict, count, mode)
        df = analyser.analyze_frequency()

        print(df)

        if chart:
            analyser.freqs_bar_chart(
                df,
                out_path="./chart.png",
                title="Relative word frequency: article vs language",
            )

        return df

    def auto_count_words(
        self,
        start_phrase: str,
        depth: int,
        wait: float,
        max_links_per_page: int,
        cnt_path: str = "./word-counts.json",
    ) -> None:
        """Crawl linked pages and update word counts across articles."""
        counter = WordCounter(counts_path=cnt_path)
        callback = counter.run
        self.phrase = start_phrase  ### _load_html needs it
        crawler = AutoCrawler(
            wait_time=wait,
            depth=depth,
            parser_cls=ArticleParser,
            client=self._load_html,
            strategy="bfs",
            max_links_per_page=max_links_per_page,
        )
        crawler.crawl(start_phrase, callback)
