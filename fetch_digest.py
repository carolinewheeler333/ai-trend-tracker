"""
Fetches latest AI news from RSS feeds, summarises with Groq (LLaMA 3),
and saves to digest/latest.json.
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
}

MAX_PER_FEED = 5
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
        print("No GROQ_API_KEY found — using raw summaries.")
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
                        f"Summarise this AI news article in 1 clear sentence. "
                        f"Be direct and specific. No fluff.\n\n"
                        f"Title: {article['title']}\n"
                        f"Content: {article['raw_summary']}"
                    )
                }],
                max_tokens=80,
                temperature=0.3,
            )
            article["summary"] = response.choices[0].message.content.strip()
            print(f"  Summarised {i+1}/{len(articles)}: {article['title'][:50]}...")
        except Exception as e:
            print(f"  Groq error for article {i+1}: {e}")
            article["summary"] = article["raw_summary"]

    return articles


def generate_briefing(articles: list[dict]) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return ""

    from groq import Groq
    client = Groq(api_key=api_key)

    headlines = "\n".join(f"- {a['title']}" for a in articles[:20])
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{
                "role": "user",
                "content": (
                    "You are an AI editor writing a daily briefing for an AI researcher. "
                    "Based on these headlines, write a 3-4 sentence paragraph summarising "
                    "the key themes and most important developments in AI today. "
                    "Be specific, intelligent, and direct. No fluff.\n\n"
                    f"Headlines:\n{headlines}"
                )
            }],
            max_tokens=200,
            temperature=0.4,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Briefing generation error: {e}")
        return ""


def save_digest(articles: list[dict], briefing: str = "") -> None:
    DIGEST_DIR.mkdir(exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    digest = {
        "date": today,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "article_count": len(articles),
        "briefing": briefing,
        "articles": articles,
    }
    # Save dated copy + latest
    (DIGEST_DIR / f"{today}.json").write_text(json.dumps(digest, indent=2))
    (DIGEST_DIR / "latest.json").write_text(json.dumps(digest, indent=2))
    print(f"\n✅ Saved {len(articles)} articles to digest/latest.json")


if __name__ == "__main__":
    print("Fetching AI news...\n")
    articles = fetch_articles()
    print(f"\nFetched {len(articles)} articles. Summarising...\n")
    articles = summarise_with_groq(articles)
    print("\nGenerating daily briefing...\n")
    briefing = generate_briefing(articles)
    save_digest(articles, briefing)
