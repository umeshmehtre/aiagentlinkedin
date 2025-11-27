# src/sources.py

RSS_SOURCES = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.technologyreview.com/feed/",
    "https://huggingface.co/blog/feed.xml",
    "https://blog.research.google/atom.xml",
    "https://www.analyticsvidhya.com/blog/feed/",
    "https://www.nature.com/subjects/machine-learning.rss",
    "https://blogs.nvidia.com/ai/feed/"
]

# Keywords to ensure article is actually AI related
AI_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "deep learning",
    "llm", "gpt", "transformer", "nlp", "neural", "model", "dataset",
    "compute", "training", "inference", "vision", "robotics"
]

def is_ai_related(text: str) -> bool:
    """Return True if article text or title contains AI keywords."""
    text = text.lower()
    return any(keyword in text for keyword in AI_KEYWORDS)
