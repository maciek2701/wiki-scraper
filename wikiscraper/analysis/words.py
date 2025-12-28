import json
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import regex as re
import seaborn as sns
import wordfreq as wf
from matplotlib import pyplot as plt


class WordCounter:
    WORD_RE = re.compile(r"\w+", flags=re.UNICODE)
    WORD_RE_ANG = re.compile(r"[A-Za-z]+(?:[-'][A-Za-z]+)*|\d+")
    WORD_RE_LATIN = re.compile(r"\p{Script=Latin}+(?:[-'’]\p{Script=Latin}+)*|\d+")

    def __init__(self, counts_path: str = "./word-counts.json"):
        self.counts_path = Path(counts_path)

    def tokenize(self, text: str) -> list[str]:
        return [t.lower() for t in self.WORD_RE_LATIN.findall(text)]

    def count_tokens(self, tokens: list[str]) -> dict[str, int]:
        return dict(
            sorted(dict(Counter(tokens)).items(), key=lambda kv: kv[1], reverse=True)
        )

    def load_counts(self) -> dict[str, int]:
        if not self.counts_path.exists():
            return {}

        with self.counts_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return {str(k): int(v) for k, v in data.items()}

    def update_counts(
        self,
        total: dict[str, int],
        run_counts: dict[str, int],
    ) -> dict[str, int]:
        for w, c in run_counts.items():
            total[w] = total.get(w, 0) + c
        return total

    def save_counts(self, counts: dict[str, int]) -> None:
        with self.counts_path.open("w", encoding="utf-8") as f:
            json.dump(counts, f, ensure_ascii=False, indent=2, sort_keys=True)

    def run(self, text: str) -> dict[str, int]:
        tokens = self.tokenize(text)
        run_counts = self.count_tokens(tokens)

        total = self.load_counts()
        total = self.update_counts(total, run_counts)
        self.save_counts(total)

        return run_counts

    def reset_counts(self):
        self.save_counts({})


class RelativeFrequencyAnalyzer:
    def __init__(self, top_k, mode, lang="en", lang_top_k=1000):
        self.lang = lang
        self.top_k = top_k
        if mode not in {"article", "language"}:
            raise ValueError("mode must be 'article' or 'language'")
        self.mode = mode
        self.lang_top_k = lang_top_k

        counter = WordCounter()
        self.counts = counter.load_counts()

        if not self.counts:
            raise ValueError("No counts loaded")

    def analyze_frequency(self):
        article_sorted = sorted(self.counts.items(), key=lambda x: x[1], reverse=True)
        article_top_words = [w for w, _ in article_sorted[: self.top_k]]

        lang_words = wf.top_n_list(self.lang, self.lang_top_k)
        freqs = {}
        for w in lang_words:
            freqs[w] = wf.word_frequency(w, self.lang)
        flang_top_words = list(freqs.keys())[: self.top_k]

        if self.mode == "article":
            selected_words = article_top_words
        elif self.mode == "language":
            selected_words = flang_top_words

        max_article = max(self.counts.values()) if self.counts else 1.0
        article_norm = {w: c / max_article for w, c in self.counts.items()}

        max_lang = max(freqs.values()) if freqs else 1
        lang_norm = {w: c / max_lang for w, c in freqs.items()}

        rows = []

        for w in selected_words:
            rows.append(
                {
                    "words": w,
                    "frequency_in_article": article_norm.get(w, np.nan),
                    "frequency_in_language": lang_norm.get(w, np.nan),
                }
            )
        df = pd.DataFrame(rows)

        if self.mode == "article":
            df = df.sort_values("frequency_in_article", ascending=False)
        elif self.mode == "language":
            df = df.sort_values("frequency_in_language", ascending=False)

        df = df.head(self.top_k).reset_index(drop=True)

        return df

    def freqs_bar_chart(self, df, out_path=None, title=""):
        plot_df = df.copy()

        plot_df["frequency_in_article"] = plot_df["frequency_in_article"].fillna(0.0)
        plot_df["frequency_in_language"] = plot_df["frequency_in_language"].fillna(0.0)

        long_df = plot_df.melt(
            id_vars="words",
            value_vars=["frequency_in_article", "frequency_in_language"],
            var_name="source",
            value_name="frequency",
        )

        # ładniejsze etykiety legendy
        long_df["source"] = long_df["source"].replace(
            {
                "frequency_in_article": "article",
                "frequency_in_language": "language",
            }
        )

        plt.figure(figsize=(max(5, len(plot_df) * 0.5), 6))
        ax = sns.barplot(data=long_df, x="words", y="frequency", hue="source")
        ax.set_title(title or "Relative word frequency: article vs language")
        ax.set_xlabel("")
        ax.set_ylabel("Normalized frequency")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        if out_path is not None:
            plt.savefig(out_path, dpi=200)
            plt.close()
        else:
            plt.show()
