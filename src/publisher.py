# src/publisher.py

import requests
from loguru import logger


def publish_to_linkedin(post_text: str, access_token: str, person_urn: str) -> bool:
    """
    Publish a simple text post to LinkedIn using the v2 UGC API.
    """

    if not access_token or not person_urn:
        logger.error("Missing LinkedIn credentials.")
        return False

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }

    payload = {
        "author": person_urn,          # must stay exactly this
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post_text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    url = "https://api.linkedin.com/v2/ugcPosts"

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)

        if response.status_code in (200, 201):
            logger.info("LinkedIn post published successfully.")
            return True

        logger.error(
            f"LinkedIn publish error: {response.status_code} - {response.text}"
        )
        return False

    except Exception as e:
        logger.error(f"LinkedIn publish exception: {e}")
        return False
