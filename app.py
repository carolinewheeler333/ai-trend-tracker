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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400&family=UnifrakturMaguntia&family=Inter:wght@300;400;500;600&display=swap');

/* ── Reset & base ── */
.stApp { background: #F5F0E8; color: #1a1a1a; }
.block-container { padding-top: 0 !important; max-width: 1100px; }
h1,h2,h3 { font-family: 'Playfair Display', Georgia, serif; }
.stMultiSelect [data-baseweb="select"] > div,
.stTextInput input { background: #fff !important; border: 1px solid #c8b99a !important; color: #1a1a1a !important; }

/* ── Animations ── */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInSlow {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes ticker {
  0%   { transform: translateX(100vw); }
  100% { transform: translateX(-100%); }
}
@keyframes borderPulse {
  0%, 100% { border-color: #8B1A1A; }
  50%       { border-color: #c0392b; }
}
@keyframes shimmer {
  0%   { background-position: -400px 0; }
  100% { background-position: 400px 0; }
}

/* ── Breaking news ticker ── */
.ticker-wrap {
  background: #8B1A1A;
  color: #F5F0E8;
  padding: 7px 0;
  overflow: hidden;
  white-space: nowrap;
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
  margin-bottom: 0;
}
.ticker-label {
  display: inline-block;
  background: #1a1a1a;
  color: #F5F0E8;
  padding: 0 14px;
  margin-right: 12px;
  font-size: 10px;
  letter-spacing: 2px;
  font-weight: 700;
}
.ticker-content {
  display: inline-block;
  animation: ticker 40s linear infinite;
}

/* ── Masthead ── */
.masthead {
  text-align: center;
  border-top: 4px double #1a1a1a;
  border-bottom: 4px double #1a1a1a;
  padding: 20px 0 16px;
  margin: 12px 0 0 0;
  animation: fadeInSlow 1.2s ease forwards;
}
.masthead-title {
  font-family: 'UnifrakturMaguntia', 'Playfair Display', serif;
  font-size: 4.2rem;
  color: #1a1a1a;
  letter-spacing: 3px;
  line-height: 1;
  margin: 0;
}
.masthead-rule {
  border: none;
  border-top: 1px solid #1a1a1a;
  margin: 8px auto;
  width: 80%;
}
.masthead-meta {
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  letter-spacing: 2.5px;
  color: #555;
  display: flex;
  justify-content: center;
  gap: 24px;
  text-transform: uppercase;
}
.masthead-tagline {
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-size: 13px;
  color: #555;
  margin-top: 2px;
}

/* ── Section header ── */
.section-header {
  font-family: 'Inter', sans-serif;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 3.5px;
  text-transform: uppercase;
  color: #8B1A1A;
  border-top: 3px solid #1a1a1a;
  border-bottom: 1px solid #1a1a1a;
  padding: 6px 0;
  margin: 24px 0 16px 0;
}

/* ── Briefing box ── */
.briefing-box {
  background: #fff;
  border: 1px solid #c8b99a;
  border-left: 4px solid #8B1A1A;
  padding: 18px 22px;
  margin-bottom: 10px;
  animation: fadeIn 0.8s ease forwards;
  animation-delay: 0.3s;
  opacity: 0;
}
.briefing-box h4 {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 10px 0;
  color: #1a1a1a;
}
.briefing-box p {
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  line-height: 1.75;
  color: #333;
  margin: 0;
}
.briefing-label {
  font-family: 'Inter', sans-serif;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: #8B1A1A;
  margin-bottom: 6px;
}

/* ── Article card ── */
.article {
  padding: 13px 0;
  border-bottom: 1px solid #c8b99a;
  animation: fadeIn 0.6s ease forwards;
  opacity: 0;
}
.article:last-child { border-bottom: none; }

.art-source {
  font-family: 'Inter', sans-serif;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 4px;
}
.art-title a {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 16.5px;
  font-weight: 700;
  color: #1a1a1a;
  text-decoration: none;
  line-height: 1.3;
  transition: color 0.2s;
}
.art-title a:hover { color: #8B1A1A; text-decoration: underline; }
.art-summary {
  font-family: 'Inter', sans-serif;
  font-size: 12.5px;
  color: #555;
  margin-top: 5px;
  line-height: 1.65;
}

/* ── Column divider ── */
.col-divider {
  border-left: 1px solid #c8b99a;
  height: 100%;
}

/* ── Footer ── */
.paper-footer {
  text-align: center;
  border-top: 2px solid #1a1a1a;
  margin-top: 30px;
  padding: 12px 0 20px;
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  color: #888;
  letter-spacing: 1px;
  animation: fadeInSlow 1s ease 1s forwards;
  opacity: 0;
}

/* Hide streamlit chrome */
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
</style>
""", unsafe_allow_html=True)

# ── Source colours ────────────────────────────────────────────────────────────
SOURCE_COLOURS = {
    "ArXiv AI":        "#2563EB",
    "ArXiv ML":        "#1D4ED8",
    "TechCrunch AI":   "#8B1A1A",
    "VentureBeat AI":  "#B45309",
    "The Verge AI":    "#6D28D9",
    "MIT Tech Review": "#065F46",
    "Wired AI":        "#374151",
}

# ── Load digest ───────────────────────────────────────────────────────────────
DIGEST_PATH = Path(__file__).parent / "digest" / "latest.json"

@st.cache_data(ttl=3600)
def load_digest():
    if not DIGEST_PATH.exists():
        return None
    return json.loads(DIGEST_PATH.read_text())

digest = load_digest()

# ── Ticker ────────────────────────────────────────────────────────────────────
if digest:
    headlines = [a["title"] for a in digest.get("articles", [])[:12]]
    ticker_text = "  ·  ".join(f"◆  {h}" for h in headlines)
    st.markdown(f"""
    <div class="ticker-wrap">
      <span class="ticker-label">BREAKING</span>
      <span class="ticker-content">{ticker_text}</span>
    </div>
    """, unsafe_allow_html=True)

# ── Masthead ──────────────────────────────────────────────────────────────────
try:
    dt = datetime.fromisoformat(digest["generated_at"].replace("Z", "+00:00")) if digest else datetime.utcnow()
except Exception:
    dt = datetime.utcnow()

date_str  = dt.strftime("%A, %B %d, %Y").upper()
vol_str   = f"VOL. {dt.year - 2024}, NO. {dt.timetuple().tm_yday}"

st.markdown(f"""
<div class="masthead">
  <div class="masthead-tagline">"All the AI that's fit to print"</div>
  <hr class="masthead-rule"/>
  <div class="masthead-title">The AI Times</div>
  <hr class="masthead-rule"/>
  <div class="masthead-meta">
    <span>{date_str}</span>
    <span>{vol_str}</span>
    <span>POWERED BY LLAMA 3</span>
  </div>
</div>
""", unsafe_allow_html=True)

if not digest:
    st.warning("No digest yet. Run `python fetch_digest.py` to generate one.")
    st.stop()

articles   = digest.get("articles", [])
briefings  = digest.get("briefings", {})
industry   = [a for a in articles if a.get("category") == "industry"]
research   = [a for a in articles if a.get("category") == "research"]

# ── Today's briefings ─────────────────────────────────────────────────────────
if briefings.get("industry") or briefings.get("research"):
    st.markdown('<div class="section-header">Today\'s Briefing</div>', unsafe_allow_html=True)

    b_col1, b_col2 = st.columns(2)
    with b_col1:
        if briefings.get("industry"):
            st.markdown(f"""
            <div class="briefing-box">
              <div class="briefing-label">Industry News Today</div>
              <h4>What's moving in AI</h4>
              <p>{briefings['industry']}</p>
            </div>
            """, unsafe_allow_html=True)
    with b_col2:
        if briefings.get("research"):
            st.markdown(f"""
            <div class="briefing-box">
              <div class="briefing-label">Research Today</div>
              <h4>From the labs</h4>
              <p>{briefings['research']}</p>
            </div>
            """, unsafe_allow_html=True)

# ── Filter bar ────────────────────────────────────────────────────────────────
all_sources = sorted(set(a["source"] for a in articles))
f1, f2 = st.columns([4, 1])
with f1:
    selected = st.multiselect("Sources", all_sources, default=all_sources, label_visibility="collapsed")
with f2:
    search = st.text_input("Search", placeholder="Search...", label_visibility="collapsed")

industry_f = [a for a in industry if a["source"] in selected and
              (not search or search.lower() in a["title"].lower())]
research_f = [a for a in research if a["source"] in selected and
              (not search or search.lower() in a["title"].lower())]

# ── Article columns ───────────────────────────────────────────────────────────
def render_articles(items, delay_start=0):
    for i, a in enumerate(items):
        colour  = SOURCE_COLOURS.get(a["source"], "#555")
        summary = a.get("summary") or a.get("raw_summary", "")
        if ". " in summary:
            summary = summary.split(". ")[0] + "."
        delay   = delay_start + i * 0.07
        st.markdown(f"""
        <div class="article" style="animation-delay:{delay:.2f}s;">
          <div class="art-source" style="color:{colour};">{a['source']}</div>
          <div class="art-title"><a href="{a['link']}" target="_blank">{a['title']}</a></div>
          <div class="art-summary">{summary}</div>
        </div>
        """, unsafe_allow_html=True)

left, _, right = st.columns([10, 1, 10])

with left:
    st.markdown('<div class="section-header">Industry News</div>', unsafe_allow_html=True)
    if industry_f:
        render_articles(industry_f, delay_start=0.4)
    else:
        st.markdown('<p style="color:#888;font-size:13px;">No industry articles.</p>', unsafe_allow_html=True)

with _:
    st.markdown('<div style="border-left:1px solid #c8b99a;min-height:600px;margin-top:50px;"></div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-header">Research</div>', unsafe_allow_html=True)
    if research_f:
        render_articles(research_f, delay_start=0.4)
    else:
        st.markdown('<p style="color:#888;font-size:13px;">No research articles.</p>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="paper-footer">
  THE AI TIMES  ·  Updated daily at 07:00 UTC  ·  {digest.get('article_count', 0)} articles today
</div>
""", unsafe_allow_html=True)


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
