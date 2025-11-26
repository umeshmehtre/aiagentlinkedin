import torch
from loguru import logger

from rss_agent import get_articles_from_rss
from summarizer import generate_title, generate_summary, generate_insight
from formatter import build_post
from publisher import publish
from sources import RSS_SOURCES

# ---------------------------
# DEVICE CONFIG
# ---------------------------
if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"

print(f"Device set to use {device}")

# ---------------------------
# MAIN DAILY AGENT
# ---------------------------
def run():
    logger.info("Starting GitHub-safe Daily AI Insight Agent")

    collected_articles = []

    for rss_url in RSS_SOURCES:
        try:
            articles = get_articles_from_rss(rss_url)
            if articles:
                collected_articles.extend(articles)
        except Exception as e:
            logger.error(f"RSS read error from {rss_url}: {str(e)}")
            continue

    if not collected_articles:
        logger.error("No fresh AI article found today.")
        return

    # Pick the newest article
    article = sorted(collected_articles, key=lambda x: x["published"], reverse=True)[0]

    title_raw = article["title"]
    content_raw = article["summary"]
    url = article["link"]

    logger.info(f"Selected fresh AI article: {title_raw}")

    # ---------------------------
    # SUMMARIZER PIPELINE
    # ---------------------------
    try:
        title = generate_title(content_raw)
        summary = generate_summary(content_raw)
        insight = generate_insight(content_raw)
    except Exception as e:
        logger.error(f"Summarization failed, using fallback: {e}")
        title = title_raw
        summary = content_raw[:400] + "..."
        insight = "This update highlights a notable development in the AI ecosystem."

    # Format LinkedIn-ready post
    post_text = build_post(title, summary, insight, url)

    # ---------------------------
    # PUBLISH TO LINKEDIN
    # ---------------------------
    try:
        publish(post_text)
        logger.info("Published 1 daily AI post from RSS")
    except Exception as e:
        logger.error(f"Publishing failed: {e}")


if __name__ == "__main__":
    run()
