"""
wikiscraper package initialization
"""

from .analysis import table, words
from .licensing import build_license_notice
from .scraper import app, client, crawler, parser
from .sources import BULBAPEDIA, LOCAL, WIKIPEDIA

__all__ = [
    "app",
    "client",
    "crawler",
    "parser",
    "table",
    "words",
    "build_license_notice",
    "BULBAPEDIA",
    "LOCAL",
    "WIKIPEDIA",
]
