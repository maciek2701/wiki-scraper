from pathlib import Path

import pytest

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


@pytest.fixture
def html_team_rocket():
    return (FIXTURES / "Team_Rocket.html").read_text(encoding="utf-8")


@pytest.fixture
def html_dimension():
    return (FIXTURES / "Dimension.html").read_text(encoding="utf-8")


@pytest.fixture
def html_sthweird():
    return (FIXTURES / "sthweird.html").read_text(encoding="utf-8")


@pytest.fixture
def html_empty():
    return (FIXTURES / "empty.html").read_text(encoding="utf-8")
