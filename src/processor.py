from transformers import pipeline
from loguru import logger
from config import SUMMARIZER_MODEL, HUGGINGFACE_TOKEN
import os
import re

os.environ["HUGGINGFACE_TOKEN"] = HUGGINGFACE_TOKEN


def get_summarizer():
    return pipeline(
        "summarization",
        model=SUMMARIZER_MODEL,
        tokenizer=SUMMARIZER_MODEL,
        device=-1
    )


def clean_title(text):
    """Take the first full sentence and turn it into a clean title."""
    sentences = re.split(r'[.!?]\s+', text)
    if sentences:
        title = sentences[0].strip()

        # Capitalize and shorten if too long
        if len(title) > 120:
            title = title[:120].rstrip() + "..."

        return title

    return "AI Update"


def convert_to_bullets(text):
    """Break long summary into clean bullet points."""
    sentences = re.split(r'[.!?]\s+', text)
    bullets = [f"- {s.strip()}" for s in sentences if len(s.strip()) > 20]
    return "\n".join(bullets)


def summarize(text: str, summarizer) -> dict:
    if not text or len(text) < 200:
        logger.error("Content too short. Using fallback summary.")
        return {
            "title": "Source Unavailable",
            "summary": "The article could not be accessed or contained insufficient readable content.",
        }

    try:
        cleaned = text[:3000]
        res = summarizer(cleaned, max_length=160, min_length=70, do_sample=False)
        summary = res[0]["summary_text"]

        title = clean_title(summary)
        bullet_summary = convert_to_bullets(summary)

        return {
            "title": title,
            "summary": bullet_summary
        }

    except Exception as e:
        logger.error(f"Summarization error: {e}")
        return {
            "title": "Summary Failed",
            "summary": "The model could not summarize the content.",
        }
