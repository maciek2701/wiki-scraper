from dataclasses import dataclass
from re import S


@dataclass(frozen=True)
class SourceInfo:
    name: str
    base_url: str
    license_name: str
    license_short: str


BULBAPEDIA = SourceInfo(
    name="Bulbapedia",
    base_url="https://bulbapedia.bulbagarden.net/wiki/",
    license_name="Creative Commons BY-NC-SA",
    license_short="BY-NC-SA",
)

### Not really used here but an example of what could be done with other sources
WIKIPEDIA = SourceInfo(
    name="Wikipedia",
    base_url="https://en.wikipedia.org/wiki/",
    license_name="Creative Commons BY-SA",
    license_short="BY-SA",
)

LOCAL = SourceInfo(
    name="Local",
    base_url="",
    license_name="",
    license_short="",
)
