import os
import requests
from loguru import logger

ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
PERSON_URN = os.getenv("LINKEDIN_PERSON_URN")  # must be full URN!


def publish_to_linkedin(text: str):
    if not ACCESS_TOKEN or not PERSON_URN:
        logger.error("Missing LinkedIn credentials.")
        return

    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "X-Restli-Protocol-Version": "2.0.0",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "author": PERSON_URN,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 201:
        logger.error(f"LinkedIn publish error: {response.status_code} - {response.text}")
    else:
        logger.info("Post published successfully!")
