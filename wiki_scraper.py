import argparse
from pathlib import Path

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
        "table-phrase",
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
    ### Dodaje frequency relative word na razie w troche inny sposob z ciekawosci
    parser.add_argument(
        "--analyze-relative-word-frequency",
        action="store_true",
        help="Analyze relative word frequency",
    )
    parser.add_argument(
        "--mode",
        choices=["language", "article"],
        default=None,
        required=False,
        help="Sorting mode (requires --analyze-relative-word-frequency)",
    )
    parser.add_argument(
        "--count",
        type=int,
        help="Number of rows to show (requires --analyze-relative-word-frequency)",
    )
    parser.add_argument(
        "--chart",
        action="store_true",
        required=False,
        default=None,
        help="Optional path to save bar chart (requires --analyze-relative-word-frequency)",
    )

    args = parser.parse_args()

    ### walidacja zależności
    used_any_analyze_opts = any(
        [
            args.mode is not None,
            args.count is not None,
            args.chart is not None,
        ]
    )
    # print(args)
    if used_any_analyze_opts and not args.analyze_relative_word_frequency:
        parser.error("--mode/--count/--chart require --analyze-relative-word-frequency")
    if args.analyze_relative_word_frequency:
        if args.mode is None or args.count is None:
            parser.error(
                "--analyze-relative-word-frequency requires --mode and --count"
            )
    return args


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
            app.run_table(args.table_phrase, args.number, args.first_row_is_header)
        if args.analyze_relative_word_frequency:
            app.analyze_relative_frequencies(args.mode, args.count, args.chart)
    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
