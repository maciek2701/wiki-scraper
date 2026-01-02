from wikiscraper.analysis.table import save_table_csv, value_freqs
from wikiscraper.analysis.words import RelativeFrequencyAnalyzer, WordCounter
from wikiscraper.scraper.client import WikiClient
from wikiscraper.scraper.crawler import AutoCrawler
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
        return WordCounter().run(text)

    def run_table(self, phrase, nr, first_row_as_header=False, display=True):
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

    def analyze_relative_frequencies(self, mode, count, chart):
        analyser = RelativeFrequencyAnalyzer(count, mode)
        df = analyser.analyze_frequency()

        print(df)

        if chart:
            analyser.freqs_bar_chart(
                df,
                out_path="./chart.png",
                title="Relative word frequency: article vs language",
            )

        return df

    def auto_count_words(self, start_phrase, depth, wait, max_links_per_page):
        counter = WordCounter()
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
