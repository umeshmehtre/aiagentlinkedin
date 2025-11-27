import feedparser
from datetime import datetime, timedelta
from loguru import logger

AI_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://www.technologyreview.com/feed/",
    "https://venturebeat.com/category/ai/feed/",
]


def get_articles_from_rss(url):
    try:
        feed = feedparser.parse(url)
        return feed.entries or []
    except Exception as e:
        logger.error(f"RSS error from {url}: {e}")
        return []


def get_fresh_article(max_age_days=2):
    """Return the freshest AI article from all feeds."""
    cutoff = datetime.utcnow() - timedelta(days=max_age_days)
    all_articles = []

    for url in AI_FEEDS:
        items = get_articles_from_rss(url)
        for item in items:
            try:
                published = (
                    datetime(*item.published_parsed[:6])
                    if hasattr(item, "published_parsed")
                    else datetime.utcnow()
                )
            except:
                published = datetime.utcnow()

            if published >= cutoff:
                all_articles.append({
                    "title": item.title,
                    "content": getattr(item, "summary", item.title),
                    "url": item.link
                })

    if not all_articles:
        return None

    return sorted(all_articles, key=lambda x: x["title"])[0]
