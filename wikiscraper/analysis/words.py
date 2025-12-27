import json
import re
from collections import Counter
from pathlib import Path


class WordCounter:
    WORD_RE = re.compile(r"\w+", flags=re.UNICODE)
    WORD_RE_ANG = re.compile(r"[A-Za-z]+(?:[-'][A-Za-z]+)*|\d+")

    def __init__(self, counts_path: str = "./word-counts.json"):
        self.counts_path = Path(counts_path)

    def tokenize(self, text: str) -> list[str]:
        return [t.lower() for t in self.WORD_RE_ANG.findall(text)]

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
