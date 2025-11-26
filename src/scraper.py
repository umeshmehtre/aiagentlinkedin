import requests
from bs4 import BeautifulSoup
from loguru import logger

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def resolve_url(url: str) -> str:
    try:
        r = requests.get(url, timeout=10, allow_redirects=True, headers=HEADERS)
        return r.url
    except Exception as e:
        logger.error(f"URL resolution failed: {e}")
        return url


def scrape_article(url: str) -> str:
    try:
        response = requests.get(url, timeout=10, headers=HEADERS)

        if response.status_code >= 400:
            logger.error(f"Bad status: {response.status_code}")
            return ""

        soup = BeautifulSoup(response.text, "lxml")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        paragraphs = soup.find_all("p")
        content = "\n".join([p.get_text().strip() for p in paragraphs if len(p.get_text()) > 40])

        return content

    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        return ""
