import feedparser
from datetime import datetime, timedelta
from loguru import logger

def parse_date(entry):
    """Safely parse RSS dates with fallback."""
    try:
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            return datetime(*entry.published_parsed[:6])
        if hasattr(entry, "updated_parsed") and entry.updated_parsed:
            return datetime(*entry.updated_parsed[:6])
    except:
        pass

    return None  # unknown date


def get_articles_from_rss(url: str, days_filter: int = 30):
    """
    Parse RSS feed and return articles published within the last X days.

    Returns list of:
    {
        "title": str,
        "summary": str,
        "link": str,
        "published": datetime
    }
    """
    try:
        feed = feedparser.parse(url)

        if feed.bozo:
            logger.error(f"RSS fetch failed: {feed.bozo_exception} for {url}")
            return []

        entries = feed.entries
        if not entries:
            logger.warning(f"No items found in RSS feed: {url}")
            return []

        fresh_articles = []
        cutoff = datetime.now() - timedelta(days=days_filter)

        for item in entries:
            pub_date = parse_date(item)
            if not pub_date:
                continue  # skip items with no valid date

            # Filter by freshness
            if pub_date < cutoff:
                continue

            article = {
                "title": item.title,
                "summary": getattr(item, "summary", item.title),
                "link": item.link,
                "published": pub_date
            }

            fresh_articles.append(article)

        return fresh_articles

    except Exception as e:
        logger.error(f"Error parsing RSS feed ({url}): {str(e)}")
        return []
