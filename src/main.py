import os
from loguru import logger
from rss_agent import get_fresh_article
from summarizer import generate_title, generate_summary, generate_insight
from formatter import build_post
from publisher import publish_to_linkedin


def run():
    logger.info("Starting Daily AI Insight Agent")

    # 1. Get trending fresh AI article
    article = get_fresh_article()
    if not article:
        logger.error("No AI article found today.")
        return

    title_raw = article["title"]
    content = article["content"]
    url = article["url"]

    logger.info(f"Selected article: {title_raw}")

    # 2. Generate clean AI insights
    title = generate_title(content)
    summary = generate_summary(content)
    insight = generate_insight(content)

    # 3. Format LinkedIn-ready post
    final_post = build_post(title, summary, insight, url)

    print("\n----- Generated LinkedIn Post -----\n")
    print(final_post)
    print("\n----------------------------------\n")

    # 4. Publish to LinkedIn only if secrets are available
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    person_urn = os.getenv("LINKEDIN_PERSON_URN")

    if not access_token or not person_urn:
        logger.error("Missing LinkedIn secrets. Skipping publish.")
        return

    publish_to_linkedin(final_post, access_token, person_urn)
    logger.info("Done!")


if __name__ == "__main__":
    run()
