import time
from collections import deque

from wikiscraper.scraper.client import WikiClient


class AutoCrawler:
    def __init__(
        self,
        wait_time,
        depth,
        parser_cls,
        client,
        strategy="bfs",
        max_links_per_page=None,
    ):
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

    def __str__(self):
        return f"AutoCrawler(wait_time={self.wait_time}, depth={self.depth}, strategy={self.strategy})"

    def __repr__(self):
        return self.__str__()

    def crawl(self, start_phrase, callback):
        visited = set()

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
                callback(text)

                if d < self.depth:
                    links = parser.extract_links()
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
