from transformers import pipeline
from loguru import logger

# Load once, shared across functions
try:
    summarizer = pipeline(
        "summarization",
        model="facebook/bart-large-cnn",
        device="cpu"
    )
except Exception as e:
    logger.error(f"Failed to load summarization model: {e}")
    summarizer = None


def generate_title(text: str) -> str:
    """Generate an impactful, short, expert-level headline."""
    if not summarizer:
        return "AI Update"

    try:
        result = summarizer(
            f"Create a short, punchy, expert tech headline from this:\n{text}",
            max_length=15,
            min_length=5,
            do_sample=False
        )[0]["summary_text"]
        return result.strip()
    except Exception as e:
        logger.error(f"Title generation failed: {e}")
        return "AI Insight"


def generate_summary(text: str) -> str:
    """Generate a smooth, human-quality 2–3 sentence expert summary."""
    if not summarizer:
        return text[:250]

    try:
        result = summarizer(
            f"Summarize this into 2–3 crisp, expert-level sentences. No repetition:\n{text}",
            max_length=130,
            min_length=60,
            do_sample=False
        )[0]["summary_text"]
        return result.strip()
    except Exception as e:
        logger.error(f"Summary generation failed: {e}")
        return text[:250]


def generate_insight(text: str) -> str:
    """Generate 1 sentence explaining the significance of the article."""
    if not summarizer:
        return ""

    try:
        result = summarizer(
            f"Explain in 1 sentence why this development matters for AI practitioners:\n{text}",
            max_length=40,
            min_length=20,
            do_sample=False
        )[0]["summary_text"]
        return result.strip()
    except Exception as e:
        logger.error(f"Insight generation failed: {e}")
        return ""
