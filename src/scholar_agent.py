from scholarly import scholarly
from loguru import logger
from pathlib import Path
from sources import SCHOLAR_KEYWORDS
from datetime import datetime

POSTED_FILE = Path("posted_articles.txt")

def load_posted_urls():
    if not POSTED_FILE.exists():
        return set()
    return set(line.strip() for line in POSTED_FILE.read_text().splitlines())

def save_posted_url(url):
    with open(POSTED_FILE, "a", encoding="utf-8") as f:
        f.write(url + "\n")

def fetch_recent_ai_paper(years_back=1):
    """
    Fetch recent AI papers from Google Scholar within the last `years_back` years.
    """
    cutoff_year = datetime.now().year - years_back
    posted_urls = load_posted_urls()

    for keyword in SCHOLAR_KEYWORDS:
        logger.info(f"Searching Scholar for keyword: {keyword}")
        search_query = scholarly.search_pubs(keyword)
        try:
            while True:
                paper = next(search_query)
                year = int(paper.bib.get("year", 0))
                url = paper.bib.get("url") or paper.bib.get("doi", "")
                if year < cutoff_year or url in posted_urls:
                    continue
                title = paper.bib.get("title", "")
                abstract = paper.bib.get("abstract", "")
                if title and abstract and url:
                    return {"title": title, "abstract": abstract, "url": url}
        except StopIteration:
            continue
    logger.error("No recent AI paper found.")
    return None
