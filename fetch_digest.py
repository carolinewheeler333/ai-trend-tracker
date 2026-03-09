"""
Fetches latest AI news from RSS feeds, summarises with Groq (LLaMA 3),
generates per-category briefings, and saves to digest/latest.json.
Run manually or via GitHub Actions.
"""

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import feedparser

FEEDS = {
    "ArXiv AI":        "https://rss.arxiv.org/rss/cs.AI",
    "ArXiv ML":        "https://rss.arxiv.org/rss/cs.LG",
    "TechCrunch AI":   "https://techcrunch.com/category/artificial-intelligence/feed/",
    "VentureBeat AI":  "https://venturebeat.com/category/ai/feed/",
    "The Verge AI":    "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
    "MIT Tech Review": "https://www.technologyreview.com/feed/",
    "Wired AI":        "https://www.wired.com/feed/tag/artificial-intelligence/latest/rss",
}

RESEARCH_SOURCES = {"ArXiv AI", "ArXiv ML"}
MAX_PER_FEED = 6
DIGEST_DIR = Path(__file__).parent / "digest"


def clean_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text or "").strip()


def fetch_articles() -> list[dict]:
    articles = []
    for source, url in FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:MAX_PER_FEED]:
                raw_summary = getattr(entry, "summary", "") or getattr(entry, "description", "")
                articles.append({
                    "source": source,
                    "category": "research" if source in RESEARCH_SOURCES else "industry",
                    "title": clean_html(entry.get("title", "No title")),
                    "link": entry.get("link", ""),
                    "raw_summary": clean_html(raw_summary)[:600],
                })
            print(f"✓ {source}: {min(len(feed.entries), MAX_PER_FEED)} articles")
        except Exception as e:
            print(f"✗ {source}: {e}")
    return articles


def summarise_with_groq(articles: list[dict]) -> list[dict]:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("No GROQ_API_KEY — using raw summaries.")
        for a in articles:
            a["summary"] = a["raw_summary"]
        return articles

    from groq import Groq
    client = Groq(api_key=api_key)

    for i, article in enumerate(articles):
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{
                    "role": "user",
                    "content": (
                        "Summarise this AI news article in exactly 1 clear, specific sentence. "
                        "No fluff, no 'this article', just the key fact.\n\n"
                        f"Title: {article['title']}\n"
                        f"Content: {article['raw_summary']}"
                    )
                }],
                max_tokens=80,
                temperature=0.3,
            )
            article["summary"] = response.choices[0].message.content.strip()
            print(f"  [{i+1}/{len(articles)}] {article['title'][:55]}...")
        except Exception as e:
            print(f"  Error on article {i+1}: {e}")
            article["summary"] = article["raw_summary"]

    return articles


def _call_groq(client, prompt: str, max_tokens: int = 220) -> str:
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()


def generate_briefings(articles: list[dict]) -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"industry": "", "research": "", "overall": ""}

    from groq import Groq
    client = Groq(api_key=api_key)

    industry = [a for a in articles if a["category"] == "industry"]
    research = [a for a in articles if a["category"] == "research"]

    def headlines(items):
        return "\n".join(f"- {a['title']}" for a in items[:15])

    briefings = {}
    try:
        briefings["industry"] = _call_groq(client, (
            "You are a sharp AI industry analyst writing a daily brief for a graduate researcher. "
            "Based on these headlines, write 3–4 sentences covering the most important industry "
            "developments, product launches, and business moves in AI today. "
            "Be specific and insightful. Name companies and products.\n\n"
            f"Headlines:\n{headlines(industry)}"
        ))
        print("✓ Industry briefing generated")
    except Exception as e:
        print(f"Industry briefing error: {e}")
        briefings["industry"] = ""

    try:
        briefings["research"] = _call_groq(client, (
            "You are an AI research editor writing a daily brief for a graduate student. "
            "Based on these paper titles, write 3–4 sentences summarising the key research themes, "
            "breakthroughs, and directions in AI/ML today. "
            "Be technical but clear. Mention specific methods or models where relevant.\n\n"
            f"Paper titles:\n{headlines(research)}"
        ))
        print("✓ Research briefing generated")
    except Exception as e:
        print(f"Research briefing error: {e}")
        briefings["research"] = ""

    try:
        all_headlines = "\n".join(f"- {a['title']}" for a in articles[:20])
        briefings["overall"] = _call_groq(client, (
            "In 2 sentences, give the single most important AI story today and why it matters. "
            "Be direct.\n\n"
            f"Headlines:\n{all_headlines}"
        ), max_tokens=100)
        print("✓ Overall briefing generated")
    except Exception as e:
        print(f"Overall briefing error: {e}")
        briefings["overall"] = ""

    return briefings


def save_digest(articles: list[dict], briefings: dict) -> None:
    DIGEST_DIR.mkdir(exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    digest = {
        "date": today,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "article_count": len(articles),
        "briefings": briefings,
        "articles": articles,
    }
    (DIGEST_DIR / f"{today}.json").write_text(json.dumps(digest, indent=2))
    (DIGEST_DIR / "latest.json").write_text(json.dumps(digest, indent=2))
    print(f"\n✅ Saved {len(articles)} articles → digest/latest.json")


if __name__ == "__main__":
    print("── Fetching AI news ──\n")
    articles = fetch_articles()
    print(f"\nFetched {len(articles)} articles total.\n── Summarising ──\n")
    articles = summarise_with_groq(articles)
    print("\n── Generating briefings ──\n")
    briefings = generate_briefings(articles)
    save_digest(articles, briefings)

