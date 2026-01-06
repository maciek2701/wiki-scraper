from pathlib import Path

from wikiscraper.scraper.app import WikiScraperApp

### Two tests will be defined and they should result in the same output
### One will use app and another internal classes


def main():
    fixtures_dir = Path(__file__).parent / "fixtures"
    file_path = fixtures_dir / "Team_Rocket.html"
    try:
        app = WikiScraperApp(path=file_path)
        app.count_words("Team_Rocket")
    except Exception as e:
        print(f"[FAIL] File not found: {e}")
        return 2
    try:
        summary = app.summary("Team Rocket cokolwiek")
        ### Program działa tak, że jesli zaladujemy html z pliku to ta fraza nie ma znaczenia
        print(summary)
    except Exception as e:
        print(f"Error: {e}")
        return 1
    ### check if summary starts and ends if desired phrase

    assert summary.startswith(
        "Team Rocket"
    ), "[FAIL] Summary does not start with 'Team Rocket"
    assert summary.endswith(
        "outpost in the Sevii Islands."
    ), "[FAIL] Summary does not end with 'outpost in the Sevii Islands."

    print("[PASS] Integration test passed")
    return 0


if __name__ == "__main__":
    SystemExit(main())
