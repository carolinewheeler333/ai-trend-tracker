# The AI Times

I built this because I got tired of opening six tabs every morning to figure out what happened in AI overnight.

The AI Times pulls from ArXiv, TechCrunch, VentureBeat, MIT Tech Review, and Wired every day at 7am UTC, runs the headlines through LLaMA 3 (via Groq's free API), and produces two things: a written briefing that synthesises the day's industry news and research separately, and a full two-column newspaper-style feed of every article with a one-sentence summary. The whole thing looks like a newspaper because that's how I want to read news — scannably, with hierarchy.

The daily update is fully automated via GitHub Actions. A workflow runs every morning, fetches the feeds, calls Groq, and commits the new digest JSON to the repo. Streamlit Cloud picks it up and redeploys automatically.

**Live →** *(add your Streamlit Cloud URL here)*

---

## Stack

`Python` · `Streamlit` · `Groq API (LLaMA 3)` · `feedparser` · `GitHub Actions`

## Sources

| Source | Category |
|---|---|
| ArXiv cs.AI | Research |
| ArXiv cs.LG | Research |
| TechCrunch AI | Industry |
| VentureBeat AI | Industry |
| MIT Tech Review | Industry |
| Wired AI | Industry |

## Run it yourself

```bash
git clone https://github.com/carolinewheeler333/ai-trend-tracker
cd ai-trend-tracker
pip install -r requirements.txt

# Optional: add your free Groq key for AI summaries
export GROQ_API_KEY=your_key_here   # get one free at console.groq.com

python fetch_digest.py   # fetch today's news
streamlit run app.py     # open the app
```

## Automated daily updates

A GitHub Action runs every day at 7am UTC. To use it:

1. Add `GROQ_API_KEY` as a repository secret (Settings → Secrets → Actions)
2. Enable **Read and write** workflow permissions (Settings → Actions → General)
3. Trigger manually first: Actions → Daily AI Digest → Run workflow

After the first run, it updates itself every morning without you touching anything.

