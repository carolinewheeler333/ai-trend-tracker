import json
import streamlit as st
from pathlib import Path
from datetime import datetime

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
