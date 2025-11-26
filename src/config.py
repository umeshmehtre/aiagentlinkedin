import os
from dotenv import load_dotenv

load_dotenv()
# How fresh an article must be (days)
FRESH_DAYS = int(os.getenv("FRESH_DAYS", "7"))

SUMMARIZER_MODEL = os.getenv("SUMMARIZER_MODEL", "facebook/bart-large-cnn")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
LINKEDIN_PERSON_URN = os.getenv("LINKEDIN_PERSON_URN")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")

TARGET_PLATFORM = "linkedin"
