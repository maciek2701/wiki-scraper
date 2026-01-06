import pytest

from wikiscraper.scraper.parser import ArticleParser


def test_extract_summary_team_rocket_starts_correctly(html_team_rocket):
    summary = ArticleParser(html_team_rocket).extract_summary()

    assert isinstance(summary, str)
    assert summary.strip()  # niepusty
    assert summary.startswith("Team Rocket")
    assert summary.endswith("outpost in the Sevii Islands.")
    assert len(summary) > 50


def test_extract_summary_from_weird_site_raises(html_sthweird):
    with pytest.raises(ValueError):
        ArticleParser(html_sthweird).extract_summary()
