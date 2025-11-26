import requests
from loguru import logger
import os
import re

ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
PERSON_URN_RAW = os.getenv("LINKEDIN_PERSON_URN")

def normalize_person_urn(raw: str) -> str:
    """
    Accept numeric id or full urn and return numeric ID.
    e.g. "urn:li:person:560872823" -> "560872823"
    """
    if not raw:
        return None
    m = re.search(r"(\d+)$", raw)
    if m:
        return m.group(1)
    return raw

PERSON_URN = normalize_person_urn(PERSON_URN_RAW)

def publish(text: str):
    if not ACCESS_TOKEN or not PERSON_URN:
        logger.error("LinkedIn credentials missing. Skipping publish.")
        return

    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }

    post_data = {
        "author": f"urn:li:person:{PERSON_URN}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }

    try:
        resp = requests.post(url, headers=headers, json=post_data, timeout=15)
        if resp.status_code in (200, 201):
            logger.info("Published successfully to LinkedIn.")
        else:
            logger.error(f"Failed to publish: {resp.status_code} - {resp.text}")
    except Exception as e:
        logger.error(f"HTTP error publishing to LinkedIn: {e}")
