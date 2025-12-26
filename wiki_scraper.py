import argparse
from pathlib import Path

from wikiscraper.scraper.app import WikiScraperApp


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--summary",
        type=str,
        required=True,
        help="Fraza do wyszukania w wiki",
    )
    parser.add_argument(
        "--local-html",
        type=Path,
        required=True,
        help="sciezka do lokalnie zapisanego pliku html",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()

    try:
        app = WikiScraperApp()
        if args.local_html is not None:
            summary = app.summary_from_local_html(args.local_html)
        else:
            summary = app.summary_from_phrase(args.summary)
        print(summary)
    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
