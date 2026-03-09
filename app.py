import json
import streamlit as st
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="The AI Times",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@400;500;600&display=swap');

  .stApp { background-color: #0D1117; color: #E6EDF3; }

  /* Masthead */
  .masthead {
    text-align: center;
    border-top: 3px solid #A0C4FF;
    border-bottom: 3px solid #A0C4FF;
    padding: 18px 0 14px 0;
    margin-bottom: 6px;
  }
  .masthead-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 3.2rem;
    font-weight: 900;
    letter-spacing: 4px;
    color: #E6EDF3;
    margin: 0;
  }
  .masthead-meta {
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    color: #8B949E;
    letter-spacing: 1px;
    margin-top: 4px;
  }

  /* Briefing box */
  .briefing {
    background: #161B22;
    border-left: 4px solid #A0C4FF;
    padding: 16px 20px;
    margin: 18px 0;
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    line-height: 1.7;
    color: #C9D1D9;
    border-radius: 0 6px 6px 0;
  }
  .briefing-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #A0C4FF;
    margin-bottom: 8px;
  }

  /* Section divider */
  .section-header {
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #8B949E;
    text-transform: uppercase;
    border-bottom: 1px solid #30363D;
    padding-bottom: 6px;
    margin: 20px 0 14px 0;
  }

  /* Article card */
  .article {
    padding: 12px 0;
    border-bottom: 1px solid #21262D;
  }
  .article:last-child { border-bottom: none; }

  .article-source {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 4px;
  }
  .article-title a {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 17px;
    font-weight: 700;
    color: #E6EDF3;
    text-decoration: none;
    line-height: 1.3;
  }
  .article-title a:hover { color: #A0C4FF; }
  .article-summary {
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    color: #8B949E;
    margin-top: 5px;
    line-height: 1.6;
  }

  /* Search box */
  .stTextInput input {
    background: #161B22 !important;
    border: 1px solid #30363D !important;
    color: #E6EDF3 !important;
    border-radius: 6px !important;
  }
  .stMultiSelect > div { background: #161B22 !important; }

  #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

SOURCE_COLOURS = {
    "ArXiv AI":        "#58A6FF",
    "ArXiv ML":        "#79C0FF",
    "TechCrunch AI":   "#FF7B72",
    "VentureBeat AI":  "#FFA657",
    "The Verge AI":    "#D2A8FF",
    "MIT Tech Review": "#3FB950",
}

DIGEST_PATH = Path(__file__).parent / "digest" / "latest.json"

@st.cache_data(ttl=3600)
def load_digest():
    if not DIGEST_PATH.exists():
        return None
    return json.loads(DIGEST_PATH.read_text())

digest = load_digest()

# ── Masthead ──────────────────────────────────────────────────────────────────
try:
    date_str = datetime.fromisoformat(digest["generated_at"].replace("Z","+00:00")).strftime("%A, %d %B %Y").upper() if digest else ""
except Exception:
    date_str = datetime.utcnow().strftime("%A, %d %B %Y").upper()

st.markdown(f"""
<div class="masthead">
  <div class="masthead-title">THE AI TIMES</div>
  <div class="masthead-meta">{date_str} &nbsp;·&nbsp; DAILY AI INTELLIGENCE BRIEFING</div>
</div>
""", unsafe_allow_html=True)

if not digest:
    st.warning("No digest yet. Run `python fetch_digest.py` to generate one.")
    st.stop()

# ── Daily briefing ────────────────────────────────────────────────────────────
briefing = digest.get("briefing", "")
if briefing:
    st.markdown(f"""
    <div class="briefing">
      <div class="briefing-label">TODAY'S BRIEFING</div>
      {briefing}
    </div>
    """, unsafe_allow_html=True)

# ── Filters ───────────────────────────────────────────────────────────────────
articles = digest.get("articles", [])
all_sources = sorted(set(a["source"] for a in articles))

col1, col2 = st.columns([3, 1])
with col1:
    selected = st.multiselect("Sources", all_sources, default=all_sources, label_visibility="collapsed")
with col2:
    search = st.text_input("Search", placeholder="Search...", label_visibility="collapsed")

filtered = [
    a for a in articles
    if a["source"] in selected
    and (not search or search.lower() in a["title"].lower() or search.lower() in a.get("summary","").lower())
]

# ── Articles split by type ────────────────────────────────────────────────────
research = [a for a in filtered if "arxiv" in a["source"].lower()]
news     = [a for a in filtered if "arxiv" not in a["source"].lower()]

def render_articles(items):
    for a in items:
        colour = SOURCE_COLOURS.get(a["source"], "#8B949E")
        summary = a.get("summary") or a.get("raw_summary", "")
        # Trim to one sentence for display
        if ". " in summary:
            summary = summary.split(". ")[0] + "."
        st.markdown(f"""
        <div class="article">
          <div class="article-source" style="color:{colour};">{a['source']}</div>
          <div class="article-title"><a href="{a['link']}" target="_blank">{a['title']}</a></div>
          <div class="article-summary">{summary}</div>
        </div>
        """, unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    if news:
        st.markdown('<div class="section-header">Industry News</div>', unsafe_allow_html=True)
        render_articles(news)

with right:
    if research:
        st.markdown('<div class="section-header">Research</div>', unsafe_allow_html=True)
        render_articles(research)


# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Trend Tracker",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Dark background */
  .stApp { background-color: #0D1117; color: #E6EDF3; }

  /* Card */
  .card {
    background: #161B22;
    border: 1px solid #30363D;
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 14px;
    transition: border-color 0.2s;
  }
  .card:hover { border-color: #A0C4FF; }

  /* Source badge */
  .badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    padding: 2px 10px;
    border-radius: 20px;
    margin-bottom: 8px;
    letter-spacing: 0.4px;
  }

  /* Title link */
  .card-title a {
    font-size: 16px;
    font-weight: 600;
    color: #A0C4FF;
    text-decoration: none;
  }
  .card-title a:hover { text-decoration: underline; }

  /* Summary */
  .card-summary { font-size: 14px; color: #8B949E; margin-top: 6px; line-height: 1.6; }

  /* Header */
  .header { text-align: center; padding: 30px 0 10px 0; }
  .header h1 { font-size: 2.4rem; margin-bottom: 4px; }
  .header p  { color: #8B949E; font-size: 15px; }

  /* Updated tag */
  .updated-tag {
    text-align: center;
    font-size: 12px;
    color: #3FB950;
    margin-bottom: 20px;
  }

  /* Filter label */
  label { color: #E6EDF3 !important; }

  /* Hide streamlit branding */
  #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Source badge colours ──────────────────────────────────────────────────────
BADGE_COLOURS = {
    "ArXiv AI":        ("#58A6FF", "#0D1117"),
    "ArXiv ML":        ("#79C0FF", "#0D1117"),
    "TechCrunch AI":   ("#FF7B72", "#0D1117"),
    "VentureBeat AI":  ("#FFA657", "#0D1117"),
    "The Verge AI":    ("#D2A8FF", "#0D1117"),
    "MIT Tech Review": ("#3FB950", "#0D1117"),
}

def badge(source: str) -> str:
    bg, fg = BADGE_COLOURS.get(source, ("#8B949E", "#0D1117"))
    return f'<span class="badge" style="background:{bg};color:{fg};">{source}</span>'


# ── Load digest ───────────────────────────────────────────────────────────────
DIGEST_PATH = Path(__file__).parent / "digest" / "latest.json"

@st.cache_data(ttl=3600)
def load_digest():
    if not DIGEST_PATH.exists():
        return None
    return json.loads(DIGEST_PATH.read_text())

digest = load_digest()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header">
  <h1>🤖 AI Trend Tracker</h1>
  <p>Daily digest of what's happening in AI — papers, products, and breakthroughs.</p>
</div>
""", unsafe_allow_html=True)

if not digest:
    st.warning("No digest found. Run `python fetch_digest.py` to generate one.")
    st.stop()

# Last updated
try:
    gen_dt = datetime.fromisoformat(digest["generated_at"].replace("Z", "+00:00"))
    updated_str = gen_dt.strftime("%A %d %B %Y, %H:%M UTC")
except Exception:
    updated_str = digest.get("date", "Unknown")

st.markdown(f'<p class="updated-tag">🟢 Last updated: {updated_str} &nbsp;·&nbsp; {digest["article_count"]} articles</p>', unsafe_allow_html=True)

# ── Filters ───────────────────────────────────────────────────────────────────
articles = digest.get("articles", [])
all_sources = sorted(set(a["source"] for a in articles))

col1, col2 = st.columns([3, 1])
with col1:
    selected_sources = st.multiselect(
        "Filter by source",
        options=all_sources,
        default=all_sources,
        label_visibility="collapsed",
    )
with col2:
    search = st.text_input("Search", placeholder="Search headlines...", label_visibility="collapsed")

# Apply filters
filtered = [
    a for a in articles
    if a["source"] in selected_sources
    and (not search or search.lower() in a["title"].lower() or search.lower() in a.get("summary", "").lower())
]

st.markdown(f"<p style='color:#8B949E;font-size:13px;margin-bottom:16px;'>{len(filtered)} stories</p>", unsafe_allow_html=True)

# ── Article cards ─────────────────────────────────────────────────────────────
if not filtered:
    st.info("No articles match your filters.")
else:
    for article in filtered:
        title   = article.get("title", "Untitled")
        link    = article.get("link", "#")
        summary = article.get("summary") or article.get("raw_summary", "")
        source  = article.get("source", "Unknown")

        st.markdown(f"""
        <div class="card">
          {badge(source)}
          <div class="card-title"><a href="{link}" target="_blank">{title}</a></div>
          <div class="card-summary">{summary}</div>
        </div>
        """, unsafe_allow_html=True)
