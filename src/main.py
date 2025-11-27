# src/main.py

import random
import os
from loguru import logger
from datetime import datetime

from rss_agent import get_articles_from_rss
from summarizer import generate_title, generate_summary, generate_insight
from formatter import build_post
from publisher import publish_to_linkedin
from sources import RSS_SOURCES, is_ai_related


def run():
    logger.info("Starting Daily AI Insight Agent")

    # Load LinkedIn credentials
    ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
    PERSON_URN = os.getenv("LINKEDIN_PERSON_URN")

    if not ACCESS_TOKEN or not PERSON_URN:
        logger.error("Missing LinkedIn credentials. Cannot publish.")
    
    # Pick a random RSS source
    rss_url = random.choice(RSS_SOURCES)
    logger.info(f"Selected RSS source: {rss_url}")

    # Pull last 30 days of articles
    articles = get_articles_from_rss(rss_url, days=30)

    if not articles:
        logger.error("No articles fetched from RSS.")
        return

    # Filter to AI specific articles only
    ai_articles = [
        a for a in articles
        if is_ai_related(a["title"])
    ]

    if not ai_articles:
        logger.error("No AI-related articles found after filtering.")
        return

    # Sort newest first
    ai_articles.sort(key=lambda x: x["published"], reverse=True)

    # Select top (newest) article
    selected = ai_articles[0]
    logger.info(f"Selected article: {selected['title']}")

    # Extract fields
    title_raw = selected["title"]
    link = selected["link"]
    content = selected.get("content", title_raw)

    # Generate enhanced title + summary + insight
    title = generate_title(title_raw)
    summary = generate_summary(content)
    insight = generate_insight(content)

    # Build final LinkedIn-ready post
    post_text = build_post(title, summary, insight, link)

    # Publish on LinkedIn
    success = publish_to_linkedin(post_text, ACCESS_TOKEN, PERSON_URN)

    if success:
        logger.info("Published successfully!")
    else:
        logger.error("Failed to publish.")


if __name__ == "__main__":
    run()
