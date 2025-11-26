# Daily Insight Agent (LinkedIn Auto Publisher)

This project automatically:

1. Selects an AI/Tech source
2. Scrapes the latest article
3. Summarizes using a HuggingFace model
4. Formats a professional post
5. Publishes to LinkedIn DAILY at 9:00 AM IST (via GitHub Actions)

## 🚀 Setup Instructions

### 1. Clone repo & install dependencies
pip install -r requirements.txt

### 2. Create a `.env` file
Copy `.env.example` → `.env` and fill your tokens:
- HuggingFace token
- LinkedIn Access Token
- LinkedIn Client ID
- LinkedIn Client Secret
- LinkedIn Person URN

### 3. Add GitHub Secrets
Go to:
Settings → Secrets → Actions → Add New Secret

Add:
- HUGGINGFACE_TOKEN
- LINKEDIN_CLIENT_ID
- LINKEDIN_CLIENT_SECRET
- LINKEDIN_PERSON_URN
- LINKEDIN_ACCESS_TOKEN

### 4. Run locally
python src/main.py

### 5. GitHub Actions schedule
Daily at 9:00 AM IST.
