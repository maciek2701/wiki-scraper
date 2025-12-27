import argparse
import re
from pathlib import Path

from tomlkit import table

from wikiscraper.scraper.app import WikiScraperApp


def parse_arguments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=False)
    parser.add_argument(
        "--summary",
        type=str,
        required=False,
        help="Fraza do wyszukania w wiki",
    )
    parser.add_argument(
        "--local-html",
        type=Path,
        help="sciezka do lokalnie zapisanego pliku html",
    )
    parser.add_argument(
        "--count-words",
        type=str,
        required=False,
        help="Count word frequencies instead of printing summary",
    )
    table_parser = subparsers.add_parser(
        "table", help="Extract n-th table from article"
    )
    table_parser.add_argument(
        "phrase",
        type=str,
        help="Phrase to search for",
    )
    table_parser.add_argument(
        "--number",
        type=int,
        required=True,
        help="Number of table to extract",
    )
    table_parser.add_argument(
        "--first-row-is-header",
        action="store_true",
        help="Treat first row as column headers",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_arguments()

    try:
        if args.local_html is not None:
            app = WikiScraperApp(path=args.local_html)
        else:
            app = WikiScraperApp()

    except ValueError as e:
        print(f"Error: {e}")
        return 2

    try:
        if args.count_words:
            app.count_words(args.count_words)
        if args.summary:
            summary = app.summary(args.summary)
            print(summary)
        if args.command == "table":
            app.run_table(args.phrase, args.number, args.first_row_is_header)
    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
