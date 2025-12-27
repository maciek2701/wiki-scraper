import argparse
from pathlib import Path

from wikiscraper.scraper.app import WikiScraperApp


def parse_arguments():
    parser = argparse.ArgumentParser()
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
        elif args.summary:
            summary = app.summary(args.summary)
            print(summary)
    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
