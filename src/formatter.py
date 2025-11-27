from datetime import datetime

def build_post(title: str, summary: str, insight: str, url: str) -> str:
    date_str = datetime.now().strftime("%d %b %Y").upper()

    return f"""
📅 DAILY AI INSIGHT — {date_str}

🔹 {title}

{summary}

💡 Insight: {insight}

🔗 Source: {url}

#AI #MachineLearning #DeepLearning #LLM #GenAI #TechNews #DailyInsights
""".strip()
