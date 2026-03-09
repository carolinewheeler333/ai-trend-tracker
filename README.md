# 🤖 AI Trend Tracker

A daily digest of what's happening in AI — research papers, product launches, and breakthroughs — pulled from the best sources and summarised with LLaMA 3.

**Live app →** *(link once deployed on Streamlit Cloud)*

---

## What it does

- Fetches the latest AI news daily from ArXiv, TechCrunch, VentureBeat, The Verge, and MIT Tech Review
- Summarises each article in 2 sentences using Groq's free LLaMA 3 API
- Commits the digest to the repo automatically via GitHub Actions
- Displays everything in a clean, searchable Streamlit app

## Stack

`Python` · `Streamlit` · `Groq (LLaMA 3)` · `feedparser` · `GitHub Actions`

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/carolinewheeler333/ai-trend-tracker
cd ai-trend-tracker
pip install -r requirements.txt
```

**2. Add your Groq API key**

Get a free key at [console.groq.com](https://console.groq.com) then add it as a GitHub secret:
- Repo → Settings → Secrets and variables → Actions → New repository secret
- Name: `GROQ_API_KEY`

**3. Run locally**
```bash
python fetch_digest.py     # fetch + summarise today's news
streamlit run app.py       # launch the app
```

## Automated updates

A GitHub Action runs every day at 7am UTC, fetches the latest news, and commits `digest/latest.json` to the repo. The Streamlit app always reads from that file.

To trigger manually: Actions → Daily AI Digest → Run workflow
