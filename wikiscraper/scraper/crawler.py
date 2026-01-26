import time
from collections import deque
from typing import Callable

from wikiscraper.scraper.client import WikiClient


class AutoCrawler:
    """Crawl linked pages starting from a phrase and process article text."""

    def __init__(
        self,
        wait_time: float,
        depth: int,
        parser_cls: type,
        client: WikiClient | Callable[[], str],
        strategy: str = "bfs",
        max_links_per_page: int | None = None,
    ) -> None:
        """Configure crawl limits, parsing, and retrieval strategy."""
        self.wait_time = wait_time
        self.depth = depth
        self.strategy = strategy
        self.max_links_per_page = max_links_per_page
        self.parser_cls = parser_cls
        self.client = client
        if self.depth < 0:
            raise ValueError("max_depth must be >= 0")
        if self.wait_time < 0:
            raise ValueError("wait_seconds must be >= 0")
        if self.strategy not in ("bfs", "dfs"):
            raise ValueError(
                "strategy must be 'bfs' or 'dfs - although dfs doesn't work rn'"
            )

    def __str__(self) -> str:
        """Return a readable representation for debugging."""
        return f"AutoCrawler(wait_time={self.wait_time}, depth={self.depth}, strategy={self.strategy})"

    def __repr__(self) -> str:
        """Return the same representation as __str__."""
        return self.__str__()

    def crawl(
        self, start_phrase: str, callback: Callable[[str], object] | None
    ) -> set[str]:
        """Traverse pages and apply a callback to extracted article text."""
        visited: set[str] = set()
        return_links: set[str] = set()
        if self.strategy == "bfs":
            dek = deque()
            pop = dek.popleft
            push = dek.append
        else:
            print("not implemented yet")
            return
        visited.add(start_phrase)
        push((start_phrase, 0))

        while dek:
            task = pop()
            phrase, d = task

            print(f"visiting {phrase} at depth {d}")

            try:
                # here 2 options - it is either load_html within app
                # but can also be used with standalone WikiClient
                html = (
                    self.client.fetch_html(phrase)
                    if isinstance(self.client, WikiClient)
                    else self.client()
                )
                parser = self.parser_cls(html)
                text = parser.extract_article_text()

                ### Counting words
                if callback is not None:
                    callback(text)

                if d < self.depth:
                    links = parser.extract_links()
                    return_links.update(links)
                    fresh = [lin for lin in links if lin not in visited]
                    ### Log diagnostyczny
                    print(
                        f"  links={len(links)} new={len(fresh)} queued={min(len(fresh), self.max_links_per_page or len(fresh))}"
                    )

                    if self.max_links_per_page is not None:
                        fresh = fresh[: self.max_links_per_page]

                    added = 0
                    for nxt in fresh:
                        if nxt not in visited:  ### mozna by i bez tego
                            visited.add(nxt)
                            push((nxt, d + 1))
                            added += 1
            except Exception as e:
                print(f"ERROR on {phrase}: {type(e).__name__} - {e}")
            if self.wait_time > 0:
                time.sleep(self.wait_time)
            else:
                print("Warning wait_time is 0")
        return return_links
