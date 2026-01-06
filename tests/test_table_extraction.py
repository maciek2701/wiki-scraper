import pandas as pd
import pytest

from wikiscraper.scraper.parser import ArticleParser


def test_extract_table_dimensions(html_dimension):
    parser = ArticleParser(html_dimension)
    df = parser.extract_table_with_pandas(1, first_row_is_header=True)  # dopasuj nr

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df.shape[0] > 0
    assert df.shape[1] > 0


def test_extract_table_rocket(html_team_rocket):
    parser = ArticleParser(html_team_rocket)
    df = parser.extract_table_with_pandas(1, first_row_is_header=True)  # dopasuj nr

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df.shape[0] > 0
    assert df.shape[1] > 0


def test_extract_table_empty(html_empty):
    with pytest.raises(ValueError):
        parser = ArticleParser(html_empty)
        df = parser.extract_table_with_pandas(1, first_row_is_header=True)  # dopasuj nr
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
