from wikiscraper.sources import SourceInfo


def build_license_notice(source: SourceInfo, page_title: str) -> str:
    page_url = f"{source.base_url}{page_title.replace(' ', '_')}"
    return (
        f"\nWyjście (oraz wszelkie utworzone elementy) programu na licencji {source.license_short} "
        f"stworzone na podstawie artykułu dostępnego na stronie\n"
        f"{page_url}."
    )
