import re
import warnings

import pandas as pd
from bs4 import BeautifulSoup


class ArticleParser:
    def __init__(self, html: str) -> None:
        self.html = html
        self.soup = BeautifulSoup(html, "html.parser")

    @staticmethod
    def is_article_link(href: str | None, prefix="/wiki/") -> bool:
        if not href:
            return False
        if href.startswith("#"):
            return False
        if not href.startswith(prefix):
            return False

        rest = href[len(prefix) :]
        if not rest:
            return False
        if ":" in rest:
            return False

        return True

    def extract_links(self, prefix="/wiki/") -> list[str]:
        container = self.get_main_content()
        links = container.find_all("a")

        results: list[str] = []
        seen: set[str] = set()

        for link in links:
            href = link.get("href")
            if self.is_article_link(href, prefix):
                slug = href[len(prefix) :]
                if slug not in seen:
                    seen.add(slug)
                    results.append(slug)

        return results

    def get_main_content(self):
        root = self.soup.find("div", id="mw-content-text")
        if root is None:
            raise ValueError("Main content root (#mw-content-text) not found")

        content = root.find("div", class_="mw-parser-output")
        if content is None:
            raise ValueError("Main content (.mw-parser-output) not found")

        return content

    def extract_summary(self):
        container = self.get_main_content()

        for p in container.find_all("p"):
            text = p.get_text("", strip=False).strip()

            if text:
                return text

        raise Exception("Summary not found")

    def _remove_unwanted(self, container):

        if not container:
            return

        ### tagi, które prawie zawsze są śmieciem dla tekstu
        for tag in container.find_all(["script", "style", "noscript", "iframe"]):
            tag.decompose()

        ### typowe elementy „nie-artykułowe”
        selectors = [
            "span.mw-editsection",
            "#toc",
            ".toc",
            "#catlinks",
            "div.printfooter",
            "div.mw-jump-link",
            "div.mw-indicators",
            # reklamy
            ".adthrive-ad",
            ".adthrive-content",
            # przypisy/odnośniki
            "ol.references",
            "div.reflist",
        ]
        for sel in selectors:
            for el in container.select(sel):
                el.decompose()

        ###„szablonowe” rzeczy: infoboxy/tabele/miniaturki.
        selectors_tables = [
            "table.infobox",
            "table.roundy",
            "table.roundtable",
            "div.thumb",  # miniaturki z podpisami
            "div.tright",
            "div.tleft",  # boxy pływające
        ]
        for sel in selectors_tables:
            for el in container.select(sel):
                el.decompose()

        ### same znaczniki przypisów w tekście: [1], [12] itd.
        for sup in container.select("sup.reference"):
            sup.decompose()

    def _clean_text(self, text: str) -> str:
        text = re.sub(
            r"\[\s*\d+\s*\]", "", text
        )  # raz jeszcze dla pewnosci usuniete przypisy
        text = re.sub(r"\s+", " ", text).strip()  # normalizacja spacji
        return text

    def extract_article_text(self) -> str:
        container = self.get_main_content()
        if not container:
            return ""

        self._remove_unwanted(container)
        blocks = []

        # Biore rzeczy z których chce składać tekst do analizy
        for el in container.find_all(["h2", "h3", "h4", "p", "li"]):
            txt = el.get_text("", strip=False)
            txt = self._clean_text(txt)

            if not txt:
                continue

            if el.name in ("h2", "h3", "h4"):
                # Nie wiedzialem czy dodawac nagłówki ale na razie tak robie
                blocks.append(f"\n{txt}\n")
            else:
                blocks.append(txt)

        # sklejam
        text = "\n".join(blocks)

        # eksperymentalnie: porządki z pustymi liniami
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        return text

    def _merge_dupe_cols(self, df: pd.DataFrame) -> pd.DataFrame:
        for c in list(df.columns):
            if isinstance(c, str) and "." in c and c.rsplit(".", 1)[-1].isdigit():
                base = c.rsplit(".", 1)[0]
                if base in df.columns:
                    df[c] = df[c].replace("", pd.NA)
                    df[base] = df[base].fillna(df[c])
                    df.drop(columns=c, inplace=True)
        return df

    def extract_table_with_pandas(self, n, first_row_is_header=True):
        container = self.get_main_content()
        tables = container.find_all("table")
        if len(tables) == 0:
            raise ValueError("No tables found")
        if n < 1 or n > len(tables):
            raise ValueError(f"Table number {n} out of range (1..{len(tables)})")
        table_tag = tables[n - 1]
        tab_html = str(table_tag)

        header = 0 if first_row_is_header else None

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=FutureWarning)
            dfs = pd.read_html(tab_html, header=header, index_col=0)
        df = dfs[0] if dfs else pd.DataFrame()

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [
                " ".join(str(x) for x in col if pd.notna(x)).strip()
                for col in df.columns
            ]

        # if isinstance(df.index, pd.MultiIndex):
        #     df.index = df.index.map(
        #         lambda t: " ".join(str(x) for x in t if pd.notna(x)).strip()
        #     )

        df = df.loc[:, ~df.columns.astype(str).str.match(r"^Unnamed")]

        df = self._merge_dupe_cols(df)

        # if df.shape[1] >= 2:
        #     df = df.set_index(df.columns[0])
        return df
