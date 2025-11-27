# src/rss_agent.py

import requests
import feedparser
from datetime import datetime, timedelta
from loguru import logger
from dateutil import parser as date_parser


def get_articles_from_rss(rss_url: str, days: int = 30):
    """
    Fetch articles from an RSS/Atom feed and return only those published
    within the last X days. Fully compatible with ISO timestamps (Google Research).
    """
    try:
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"RSS fetch failed: {e} for {rss_url}")
        return []

    try:
        feed = feedparser.parse(response.text)
    except Exception as e:
        logger.error(f"RSS parsing error for {rss_url}: {e}")
        return []

    if not feed.entries:
        logger.warning(f"No items found in RSS feed: {rss_url}")
        return []

    articles = []
    cutoff = datetime.utcnow() - timedelta(days=days)

    for entry in feed.entries:
        try:
            # Priority: published_parsed → updated_parsed → ISO date strings
            published = None

            if "published_parsed" in entry and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6])

            elif "updated_parsed" in entry and entry.updated_parsed:
                published = datetime(*entry.updated_parsed[:6])

            elif "published" in entry:
                published = date_parser.parse(entry.published)

            elif "updated" in entry:
                published = date_parser.parse(entry.updated)

            else:
                continue  # skip entries with no date

            # Convert timezone-aware to UTC naive
            if published.tzinfo is not None:
                published = published.astimezone(tz=None).replace(tzinfo=None)

            if published < cutoff:
                continue

            articles.append({
                "title": entry.title,
                "link": entry.link,
                "content": entry.get("summary", entry.title),
                "published": published
            })

        except Exception as e:
            logger.error(f"Error parsing entry: {e}")
            continue

    return articles
