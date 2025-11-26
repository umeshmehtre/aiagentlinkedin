from datetime import datetime

def build_post(title: str, summary: str, insight: str, url: str) -> str:
    """
    Format a polished, LinkedIn-ready AI news post.
    Works together with summarizer.py.
    """

    date_str = datetime.now().strftime("%d %b %Y").upper()

    post = f"""
📅 DAILY AI INSIGHT — {date_str}

🔹 **{title}**

{summary}

**Why it matters:** {insight}

🔗 Source: {url}

#AI #MachineLearning #DeepLearning #LLM #GenAI #TechNews #DailyInsights
"""
    return post.strip()
