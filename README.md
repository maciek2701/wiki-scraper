# Wiki Scraper

> Prosty scraper artykułów z wiki (domyślnie Bulbapedia) z analizą tabel i słów.

## Opis
Projekt służy do pobierania treści artykułów z wiki, wyciągania krótkiego opisu,
ekstrakcji tabel oraz analizy częstości słów. Można pracować na stronie online
albo na lokalnym pliku HTML (np. zapisanym wcześniej).

## Funkcje
- Pobieranie i parsowanie artykułów (Bulbapedia lub lokalny HTML).
- Wyciąganie podsumowania artykułu.
- Ekstrakcja n-tej tabeli do CSV.
- Zliczanie słów i zapis sum do pliku JSON.
- Analiza względnych częstości słów + opcjonalny wykres.
- Automatyczne przechodzenie po linkach i zliczanie słów w wielu artykułach.

## Struktura projektu
- `wikiscraper/` — główna paczka z analizą, parserem i klientem HTTP.
- `wiki_scraper.py` — CLI do uruchamiania funkcji z linii poleceń.
- `tests/` — testy jednostkowe (pytest).
- `fixtures/` — przykładowe HTML do testów.
- `notebooks/` — notatniki do eksperymentów/analityki.

## Wymagania
- Python >= 3.11

## Instalacja
Jeśli jako pakiet po pobraniu repozytorium.
### Opcja A: pip
```bash
pip install -r requirements.txt
```

### Opcja B: instalacja edytowalna (dev)
```bash
pip install -e .
```

### Jako pakiet z githuba (paczka nie jest udostepniona w PyPI dlatego najlepiej z repo)
```bash
pip install git+https://github.com/maciek2701/wiki-scraper.git

pip install .[notebook]       # + jupyter
pip install .[dev]            # + narzędzia dev
pip install .[dev,notebook]   # oba extras
```

## Użycie

Można też używać tak:
```bash
wikiscraper --flagi argumenty
```
A test integracyjny:
``` bash
wiki_scraper_integration_test
```

### Podstawowe podsumowanie artykułu
```bash
python wiki_scraper.py --summary "Team Rocket"
```

### Lokalny HTML
```bash
python wiki_scraper.py --local-html path\to\page.html --summary "Team Rocket"
```

### Ekstrakcja tabeli
```bash
python wiki_scraper.py table "Team Rocket" --number 1 --first-row-is-header
```

### Zliczanie słów
```bash
python wiki_scraper.py --count-words "Team Rocket"
```

### Analiza względnych częstości słów
```bash
python wiki_scraper.py --analyze-relative-word-frequency --mode article --count 20
```

### Automatyczne zliczanie słów po linkach
```bash
python wiki_scraper.py --auto-count-words "Team Rocket" --depth 1 --wait 0.5
```

## Wyniki i pliki wyjściowe
- `word-counts.json` — skumulowane zliczenia słów (tworzone/aktualizowane).
- `*.csv` — tabela zapisana przez funkcję ekstrakcji tabel (nazwa z frazy).
- `chart.png` — opcjonalny wykres z analizy częstości (gdy użyjesz `--chart`).

## Konfiguracja
- Domyślne źródło to Bulbapedia.
- `--local-html` przełącza analizę na plik lokalny.
- Ścieżka pliku z licznikiem słów jest domyślnie `./word-counts.json`.

## Testy
```bash
pytest
```

## Development
### Linting i formatowanie
```bash
ruff check .
black .
```

## License i źródła danych

Kod programu jest udostępniony do celów edukacyjnych.
Wyniki programu oparte są o treści z Bulbapedia i podlegają licencji
Creative Commons BY-NC-SA.

Przykładowa informacja generowana przez program:
"Wyjście programu na licencji BY-NC-SA stworzone na podstawie artykułu dostępnego
na stronie https://bulbapedia.bulbagarden.net/wiki/Team_Rocket."
