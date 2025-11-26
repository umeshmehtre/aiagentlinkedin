from datetime import datetime

def build_post(title: str, summary: str, insight: str, url: str) -> str:
    """Format a clean LinkedIn-ready daily AI post without markdown bold."""
    
    date_str = datetime.now().strftime("%d %b %Y").upper()

    post = f"""
📅 DAILY AI INSIGHT — {date_str}

🔹 {title}

{summary}


🔗 Source: {url}

#AI #MachineLearning #DeepLearning #LLM #GenAI #TechNews #DailyInsights
"""
    return post.strip()
