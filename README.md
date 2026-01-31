# Wiki Scraper

> [TODO: One-sentence description of what this project does.]

## Overview
[TODO: Add a short paragraph describing the goal, scope, and target users.]

## Features
- [TODO: Feature 1]
- [TODO: Feature 2]
- [TODO: Feature 3]

## Project structure
- `wikiscraper/` — [TODO: core package description]
- `wiki_scraper.py` — [TODO: CLI entry point description]
- `tests/` — [TODO: tests description]
- `notebooks/` — [TODO: notebooks usage]
- `fixtures/` — [TODO: sample data description]

## Installation
### Option A: pip
```bash
pip install -r requirements.txt
```

### Option B: editable install (recommended for development)
```bash
pip install -e .
```

## Usage
### Basic summary
```bash
python wiki_scraper.py --summary "Your phrase here"
```

### Local HTML
```bash
python wiki_scraper.py --local-html path\to\page.html --summary "Your phrase here"
```

### Extract a table
```bash
python wiki_scraper.py table "Your phrase here" --number 1 --first-row-is-header
```

### Word counts
```bash
python wiki_scraper.py --count-words "Your phrase here"
```

## Output
[TODO: Describe output files, formats, and where they are saved.]

## Configuration
[TODO: Mention config files, environment variables, or defaults.]

## Testing
```bash
pytest
```

## Development
### Linting and formatting
```bash
ruff check .
black .
```

## Roadmap
- [TODO: Planned improvement 1]
- [TODO: Planned improvement 2]

## License and data sources

The program code is provided for educational purposes.
Program outputs are based on content from Bulbapedia and are subject to the
Creative Commons BY-NC-SA license.

Example notice printed by the program:
"Wyjście programu na licencji BY-NC-SA stworzone na podstawie artykułu dostępnego
na stronie https://bulbapedia.bulbagarden.net/wiki/Team_Rocket."


