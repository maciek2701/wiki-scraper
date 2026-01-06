import pytest

from wikiscraper.scraper.parser import ArticleParser


@pytest.mark.parametrize(
    "href, expected",
    [
        (None, False),
        ("", False),
        ("#section", False),
        ("/wiki/Team_Rocket", True),
        ("/wiki/File:Something.png", False),
        ("/wiki/Category:Pok%C3%A9mon", False),
        ("/notwiki/Team_Rocket", False),
    ],
)
def test_is_article_link(href, expected):
    assert ArticleParser.is_article_link(href) is expected
