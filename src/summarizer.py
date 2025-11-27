from transformers import pipeline
from loguru import logger

try:
    summarizer = pipeline(
        "summarization",
        model="facebook/bart-large-cnn",
        device="cpu"
    )
except Exception as e:
    logger.error(f"Failed to load summarizer: {e}")
    summarizer = None


def safe_summarize(text: str, max_len, min_len):
    """Safe summarizer: avoids hallucinations for short texts."""
    if not summarizer:
        return text[:250]

    if len(text.split()) < 20:
        return text  # DO NOT summarize ultra-short text

    try:
        result = summarizer(
            text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )[0]["summary_text"]
        return result.strip()
    except Exception as e:
        logger.error(f"Summarization failed: {e}")
        return text[:250]


def generate_title(text: str) -> str:
    """Generate short expert title."""
    return safe_summarize(
        f"Write a punchy 4–6 word headline: {text}",
        max_len=15,
        min_len=5
    )


def generate_summary(text: str) -> str:
    """2–3 sentence clean summary."""
    return safe_summarize(
        f"Summarize into 2–3 crisp expert sentences. No repetition: {text}",
        max_len=110,
        min_len=50
    )


def generate_insight(text: str) -> str:
    """Why this matters."""
    return safe_summarize(
        f"Explain in 1 sentence why this matters to AI practitioners: {text}",
        max_len=40,
        min_len=20
    )
