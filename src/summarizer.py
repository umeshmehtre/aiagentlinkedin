from transformers import pipeline
from loguru import logger

# Load globally
try:
    summarizer = pipeline(
        "summarization",
        model="facebook/bart-large-cnn",
        device="cpu"
    )
except Exception as e:
    logger.error(f"Summarizer load failed: {e}")
    summarizer = None


def generate_title(text: str) -> str:
    """Generate a crisp, short expert headline."""
    if not summarizer:
        return "AI Insight"

    try:
        result = summarizer(
            text,
            max_length=20,
            min_length=5,
            do_sample=False
        )[0]["summary_text"]
        return result.strip().replace(".", "")
    except Exception as e:
        logger.error(f"Title generation failed: {e}")
        return "AI Update"


def generate_summary(text: str) -> str:
    """Generate a clean 2–3 sentence expert summary."""
    if not summarizer:
        return text[:250]

    try:
        result = summarizer(
            text,
            max_length=130,
            min_length=60,
            do_sample=False
        )[0]["summary_text"]
        return result.strip()
    except Exception as e:
        logger.error(f"Summary generation failed: {e}")
        return text[:250]


def generate_insight(text: str) -> str:
    """Generate one meaningful expert insight sentence."""
    if not summarizer:
        return ""

    try:
        raw = summarizer(
            text,
            max_length=40,
            min_length=20,
            do_sample=False
        )[0]["summary_text"]

        return f"This development matters because {raw.strip().lower()}."
    except Exception as e:
        logger.error(f"Insight generation failed: {e}")
        return ""
