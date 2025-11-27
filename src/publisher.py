import requests
from loguru import logger


def publish_to_linkedin(text: str, access_token: str, person_urn: str):
    """Publish LinkedIn post."""
    try:
        api_url = "https://api.linkedin.com/v2/ugcPosts"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json"
        }

        payload = {
            "author": person_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }

        response = requests.post(api_url, json=payload, headers=headers)

        if response.status_code != 201:
            logger.error(f"LinkedIn publish error: {response.status_code} - {response.text}")
        else:
            logger.info("Successfully published to LinkedIn!")

    except Exception as e:
        logger.error(f"Failed to publish to LinkedIn: {e}")
