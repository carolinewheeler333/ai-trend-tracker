import json
import re
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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400&family=UnifrakturMaguntia&family=Inter:wght@300;400;500;600&display=swap');

body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
.main .block-container {
  background-color: #F5F0E8 !important;
  color: #1a1a1a !important;
}
.block-container { padding-top: 0 !important; max-width: 1080px; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes ticker {
  0%   { transform: translateX(100vw); }
  100% { transform: translateX(-100%); }
}

.ticker-wrap {
  background: #8B1A1A;
  padding: 6px 0;
  overflow: hidden;
  white-space: nowrap;
}
.ticker-label {
  display: inline-block;
  background: #1a1a1a;
  color: #F5F0E8;
  padding: 1px 14px;
  font-family: 'Inter', sans-serif;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 2.5px;
  margin-right: 10px;
  vertical-align: middle;
}
.ticker-scroll {
  display: inline-block;
  animation: ticker 50s linear infinite;
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  font-weight: 500;
  color: #F5F0E8;
}

.masthead {
  text-align: center;
  border-top: 4px double #1a1a1a;
  border-bottom: 1px solid #1a1a1a;
  padding: 18px 0 12px;
  margin: 14px 0 0;
  animation: fadeIn 1s ease forwards;
}
.masthead-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 4.2rem;
  font-weight: 900;
  color: #1a1a1a;
  letter-spacing: 6px;
  text-transform: uppercase;
  line-height: 1;
  margin: 0;
}
.masthead-rule { border: none; border-top: 1px solid #C8B99A; margin: 8px auto 6px; width: 70%; }
.masthead-meta {
  font-family: 'Inter', sans-serif;
  font-size: 10.5px;
  letter-spacing: 2px;
  color: #6B5B45;
  text-transform: uppercase;
  display: flex;
  justify-content: center;
  gap: 20px;
}
.masthead-tagline {
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-size: 12.5px;
  color: #6B5B45;
  margin-top: 4px;
}

.overall-summary {
  background: #1a1a1a;
  color: #F5F0E8;
  padding: 16px 22px;
  margin: 16px 0 0;
  border-left: 4px solid #8B1A1A;
  animation: fadeIn 0.8s ease 0.1s forwards;
  opacity: 0;
}
.overall-eyebrow {
  font-family: 'Inter', sans-serif;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: #8B1A1A;
  margin-bottom: 7px;
}
.overall-body {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 15px;
  line-height: 1.8;
  font-style: italic;
  color: #E8E0D0;
}

.section-rule {
  border: none;
  border-top: 3px solid #1a1a1a;
  border-bottom: 1px solid #C8B99A;
  margin: 22px 0 0;
}
.section-label {
  font-family: 'Inter', sans-serif;
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: #8B1A1A;
  padding-top: 5px;
  margin-bottom: 14px;
}

.briefing {
  background: #FFFDF8;
  border: 1px solid #C8B99A;
  border-top: 3px solid #8B1A1A;
  padding: 16px 20px;
  animation: fadeIn 0.8s ease 0.3s forwards;
  opacity: 0;
}
.briefing-eyebrow {
  font-family: 'Inter', sans-serif;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: #8B1A1A;
  margin-bottom: 7px;
}
.briefing-body {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 13.5px;
  line-height: 1.8;
  color: #2a2a2a;
  font-style: italic;
}

.article {
  padding: 11px 0;
  border-bottom: 1px solid #D4C9B5;
  animation: fadeIn 0.5s ease forwards;
  opacity: 0;
}
.article:last-child { border-bottom: none; }
.art-source {
  font-family: 'Inter', sans-serif;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 3px;
}
.art-title a {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 16px;
  font-weight: 700;
  color: #1a1a1a;
  text-decoration: none;
  line-height: 1.3;
}
.art-title a:hover { color: #8B1A1A; }
.art-summary {
  font-family: 'Inter', sans-serif;
  font-size: 12.5px;
  color: #5A4F42;
  margin-top: 4px;
  line-height: 1.6;
}

.col-divider { border-left: 1px solid #C8B99A; min-height: 500px; margin-top: 50px; }

.stMultiSelect [data-baseweb="select"] > div {
  background: #FFFDF8 !important; border: 1px solid #C8B99A !important;
  color: #1a1a1a !important; font-family: 'Inter', sans-serif !important; font-size: 12px !important;
}
.stTextInput input {
  background: #FFFDF8 !important; border: 1px solid #C8B99A !important;
  color: #1a1a1a !important; font-family: 'Inter', sans-serif !important; font-size: 12px !important;
}
[data-baseweb="tag"] { background: #8B1A1A !important; }
[data-baseweb="tag"] span { color: #F5F0E8 !important; }

.paper-footer {
  text-align: center;
  border-top: 3px double #1a1a1a;
  margin-top: 36px;
  padding: 10px 0 24px;
  font-family: 'Inter', sans-serif;
  font-size: 10.5px;
  letter-spacing: 1.5px;
  color: #6B5B45;
  text-transform: uppercase;
}

#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
</style>
""", unsafe_allow_html=True)

SOURCE_COLOURS = {
    "ArXiv AI":        "#1E3A8A",
    "ArXiv ML":        "#1E3A8A",
    "TechCrunch AI":   "#991B1B",
    "VentureBeat AI":  "#92400E",
    "The Verge AI":    "#5B21B6",
    "MIT Tech Review": "#065F46",
    "Wired AI":        "#1F2937",
}

DIGEST_PATH = Path(__file__).parent / "digest" / "latest.json"

@st.cache_data(ttl=3600)
def load_digest():
    if not DIGEST_PATH.exists():
        return None
    return json.loads(DIGEST_PATH.read_text())

digest = load_digest()

# Ticker
if digest:
    titles = [a["title"] for a in digest.get("articles", [])[:14]]
    ticker = "  ·  ".join(f"◆ {t}" for t in titles)
    st.markdown(f'<div class="ticker-wrap"><span class="ticker-label">Today</span><span class="ticker-scroll">{ticker}</span></div>', unsafe_allow_html=True)

# Masthead
try:
    dt = datetime.fromisoformat(digest["generated_at"].replace("Z", "+00:00")) if digest else datetime.utcnow()
except Exception:
    dt = datetime.utcnow()

date_str = dt.strftime("%A, %B %-d, %Y").upper()
vol_no   = f"Vol. {dt.year - 2024}  ·  No. {dt.timetuple().tm_yday}"

st.markdown(f"""
<div class="masthead">
  <div class="masthead-tagline">"All the AI that's fit to print"</div>
  <hr class="masthead-rule"/>
  <div class="masthead-title">The AI Times</div>
  <hr class="masthead-rule"/>
  <div class="masthead-meta">
    <span>{date_str}</span><span>{vol_no}</span><span>Barcelona · Est. 2025</span>
  </div>
</div>
""", unsafe_allow_html=True)

if not digest:
    st.warning("No digest yet — run `python fetch_digest.py` to generate one.")
    st.stop()

articles  = digest.get("articles", [])
briefings = digest.get("briefings", {})
industry  = [a for a in articles if a.get("category") == "industry"]
research  = [a for a in articles if a.get("category") == "research"]

# Overall summary
overall = briefings.get("overall", "")
n_industry = len(industry)
n_research = len(research)
sources_today = sorted(set(a["source"] for a in articles))
fallback = f"{len(articles)} stories today across {len(sources_today)} sources — {n_industry} industry updates and {n_research} research papers. Trigger the daily digest action to generate AI summaries."
display_overall = overall if overall else fallback
st.markdown(f"""
<div class="overall-summary">
  <div class="overall-eyebrow">Today in AI</div>
  <div class="overall-body">{display_overall}</div>
</div>
""", unsafe_allow_html=True)

# Per-category briefings
if briefings.get("industry") or briefings.get("research"):
    st.markdown('<div class="section-rule"></div><div class="section-label">Today\'s Briefing</div>', unsafe_allow_html=True)
    b1, gap, b2 = st.columns([10, 1, 10])
    with b1:
        if briefings.get("industry"):
            st.markdown(f'<div class="briefing"><div class="briefing-eyebrow">Industry</div><div class="briefing-body">{briefings["industry"]}</div></div>', unsafe_allow_html=True)
    with gap:
        st.markdown('<div class="col-divider"></div>', unsafe_allow_html=True)
    with b2:
        if briefings.get("research"):
            st.markdown(f'<div class="briefing"><div class="briefing-eyebrow">Research</div><div class="briefing-body">{briefings["research"]}</div></div>', unsafe_allow_html=True)

# Filters
all_sources = sorted(set(a["source"] for a in articles))
f1, f2 = st.columns([4, 1])
with f1:
    selected = st.multiselect("Sources", all_sources, default=all_sources, label_visibility="collapsed", key="source_filter")
with f2:
    search = st.text_input("Search", placeholder="Search headlines...", label_visibility="collapsed", key="search_input")

industry_f = [a for a in industry if a["source"] in selected and (not search or search.lower() in a["title"].lower())]
research_f = [a for a in research if a["source"] in selected and (not search or search.lower() in a["title"].lower())]

# Articles
def clean_summary(text: str) -> str:
    # Strip ArXiv announce prefix
    text = re.sub(r'arXiv:\S+\s+Announce Type:\s+\w+\s+Abstract:\s*', '', text or '')
    text = re.sub(r'Announce Type:\s+\w+\s+Abstract:\s*', '', text)
    text = text.strip()
    # Trim to one sentence, max 160 chars
    text = text.split(". ")[0].strip()
    if len(text) > 160:
        text = text[:157] + "..."
    if text and not text.endswith("."):
        text += "."
    return text

def render_articles(items, delay_start=0.3):
    for i, a in enumerate(items):
        colour  = SOURCE_COLOURS.get(a["source"], "#3D3D3D")
        summary = clean_summary(a.get("summary") or a.get("raw_summary", ""))
        delay = delay_start + i * 0.06
        st.markdown(f"""
        <div class="article" style="animation-delay:{delay:.2f}s;">
          <div class="art-source" style="color:{colour};">{a['source']}</div>
          <div class="art-title"><a href="{a['link']}" target="_blank">{a['title']}</a></div>
          <div class="art-summary">{summary}</div>
        </div>""", unsafe_allow_html=True)

left, mid, right = st.columns([10, 1, 10])
with left:
    st.markdown('<div class="section-rule"></div><div class="section-label">Industry News</div>', unsafe_allow_html=True)
    render_articles(industry_f) if industry_f else st.markdown('<p style="color:#9C8672;font-size:13px;font-style:italic;">No results.</p>', unsafe_allow_html=True)
with mid:
    st.markdown('<div class="col-divider"></div>', unsafe_allow_html=True)
with right:
    st.markdown('<div class="section-rule"></div><div class="section-label">Research</div>', unsafe_allow_html=True)
    render_articles(research_f) if research_f else st.markdown('<p style="color:#9C8672;font-size:13px;font-style:italic;">No results.</p>', unsafe_allow_html=True)

# Footer
st.markdown(f'<div class="paper-footer">The AI Times &nbsp;·&nbsp; {digest.get("article_count", len(articles))} articles &nbsp;·&nbsp; Updated daily 07:00 UTC &nbsp;·&nbsp; Summaries by LLaMA 3</div>', unsafe_allow_html=True)
