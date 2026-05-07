"""
ThemeForest Gap Analysis Dashboard — Streamlit App
===================================================
Deploy on Streamlit Cloud:
  1. Push this file to GitHub as  dashboard.py
  2. Go to https://share.streamlit.io  →  New app  →  select repo
  3. Main file path: dashboard.py
  4. Click Deploy

Run locally:
  pip install streamlit plotly pandas
  streamlit run dashboard.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ── PAGE CONFIG ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="ThemeForest Gap Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CUSTOM CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stAppViewContainer"] { background: #F0F4F8; }
  [data-testid="stSidebar"] { background: #1F4E78; }
  [data-testid="stSidebar"] * { color: #ffffff !important; }
  [data-testid="stSidebar"] .stSelectbox label { color: #BDD7EE !important; }
  .block-container { padding-top: 1rem; padding-bottom: 2rem; }
  h1 { color: #1F4E78 !important; font-size: 1.6rem !important; }
  h2 { color: #2E75B6 !important; font-size: 1.2rem !important; }
  h3 { color: #1F4E78 !important; font-size: 1rem !important; }
  .metric-card {
    background: white; border-radius: 10px; padding: 14px 18px;
    border-left: 4px solid #2E75B6; margin-bottom: 8px;
    box-shadow: 0 1px 4px rgba(0,0,0,.06);
  }
  .pill-cr { background:#FEE2E2; color:#991B1B; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:600; }
  .pill-mj { background:#FEF3C7; color:#92400E; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:600; }
  .pill-mo { background:#DCFCE7; color:#166534; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:600; }
  .pill-rd { background:#DBEAFE; color:#1E40AF; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:600; }
  .cover-banner {
    background: linear-gradient(135deg, #1F4E78 0%, #2563EB 60%, #1D9E75 100%);
    padding: 22px 28px; border-radius: 12px; margin-bottom: 20px; color: white;
  }
  .cover-banner h1 { color: white !important; margin: 0; font-size: 1.5rem !important; }
  .cover-banner p  { margin: 4px 0 0; opacity: .8; font-size: .85rem; }
  div[data-testid="metric-container"] {
    background: white; border-radius: 10px; padding: 12px;
    box-shadow: 0 1px 4px rgba(0,0,0,.06);
  }
</style>
""", unsafe_allow_html=True)

# ── COLOURS ───────────────────────────────────────────────────────────
C = dict(w1="#378ADD", w2="#EF9F27", w3="#1D9E75",
         tgt="#E24B4A", navy="#1F4E78", gold="#C9A44B")

# ══ DATA ══════════════════════════════════════════════════════════════

READINESS_CRITERIA = [
    "Design Originality", "Typography System", "Colour & Visual Identity",
    "Animation / Motion", "Inner Page Count", "Responsiveness",
    "UX / Navigation", "Code Quality", "Performance (PageSpeed)",
    "Accessibility (WCAG)", "Documentation", "Support Infrastructure",
    "Marketplace Listing",
]
W1_SCORES  = [3, 3, 4, 0, 1, 5, 4, 4, 5, 2, 0, 0, 0]
W2_SCORES  = [4, 4, 4, 0, 1, 5, 5, 4, 5, 3, 0, 0, 0]
W3_SCORES  = [5, 4, 5, 2, 2, 6, 5, 5, 5, 3, 0, 0, 0]
TGT_SCORES = [8, 8, 8, 7,10, 9, 8, 8, 8, 8, 8, 8, 8]

FUNNEL_STAGES = ["TF Search","Click Thumbnail","Watch Video",
                 "Click Live Preview","Read Description","Add to Cart","Purchase"]
FUNNEL_W1  = [10000, 180,   0,  25,  38,  4,  3]
FUNNEL_W2  = [10000, 210,   0,  32,  44,  5,  4]
FUNNEL_W3  = [10000, 240,   5,  38,  52,  6,  5]
FUNNEL_OPT = [10000,1200, 540, 780, 660, 42, 34]

SALES_DATES = ["5-Feb","12-Feb","19-Feb","26-Feb","5-Mar","12-Mar","19-Mar",
               "26-Mar","2-Apr","9-Apr","16-Apr","23-Apr","30-Apr"]
SALES_W1 = [4,  5,  5,  6,  7,  7,  8,  6,  7,  8,  9,  8, 10]
SALES_W2 = [6,  7,  8,  8,  9, 10,  9, 11, 10, 12, 11, 13, 12]
SALES_W3 = [9, 11, 13, 12, 14, 13, 15, 16, 14, 17, 16, 18, 19]

TRAFFIC_CHANNELS = ["TF Search","Direct/Demo","Google Organic","YouTube",
                    "Dribbble/Behance","Reddit/Forums","Email","Affiliate"]
TRAFFIC_W1 = [1240, 420, 310,  85, 260,  70,  45, 30]
TRAFFIC_W2 = [2100, 680, 540, 140, 120, 180,  90, 75]
TRAFFIC_W3 = [1850, 590, 720, 430,  90, 150, 110, 60]

REV_SCENARIOS = ["Conservative", "Moderate", "Optimistic"]
REV_W1 = [1509, 3019, 6038]
REV_W2 = [1072, 2144, 4288]
REV_W3 = [1728, 3456, 6913]

COMP_NAMES = ["Avada","Flatsome","Divi","Bridge","Jupiter X","Astra Pro","Webflow","MOJO"]
COMP_SALES = [4830, 3200, 2950, 2070, 1800, 1450, 1200, 650]

GAPS = [
    ["Responsive Layout",        "Partial","Partial","Partial","Critical"],
    ["Sticky Header",            "No",    "No",    "No",    "Critical"],
    ["Mobile Hamburger Menu",    "Partial","Partial","Partial","Critical"],
    ["Contact Form+Validation",  "No",    "No",    "No",    "Critical"],
    ["GDPR Cookie Consent",      "No",    "No",    "No",    "Critical"],
    ["Cross-browser Tested",     "No",    "No",    "No",    "Critical"],
    ["WCAG Keyboard Nav",        "No",    "No",    "No",    "Critical"],
    ["Documentation (PDF/HTML)", "No",    "No",    "No",    "Critical"],
    ["Smooth Scrolling",         "No",    "No",    "Partial","High"],
    ["Back-to-Top Button",       "No",    "No",    "No",    "High"],
    ["404 Error Page",           "No",    "No",    "No",    "Critical"],
    ["Search Functionality",     "No",    "No",    "No",    "High"],
    ["Dark Mode Variant",        "No",    "No",    "No",    "High"],
    ["Pricing Tables",           "N/A",   "No",    "No",    "Critical"],
    ["Testimonials Section",     "No",    "No",    "No",    "High"],
    ["Team / Instructor",        "No",    "No",    "No",    "High"],
    ["FAQ Accordion",            "No",    "No",    "No",    "High"],
    ["Video Lightbox",           "N/A",   "N/A",   "No",    "High"],
    ["Social Share Buttons",     "No",    "No",    "No",    "Medium"],
    ["Schema.org Data",          "No",    "No",    "No",    "Medium"],
]

ROADMAP = [
    ["Phase 1","Responsive layout (320-2560px)",  "Frontend Dev", 1, 3,"Critical"],
    ["Phase 1","Contact forms + validation",       "Frontend Dev", 1, 2,"Critical"],
    ["Phase 1","GDPR cookie consent",              "Frontend Dev", 1, 1,"Critical"],
    ["Phase 1","W3C HTML validate",                "Frontend Dev", 2, 3,"Critical"],
    ["Phase 1","Fix JS errors & broken links",     "Frontend Dev", 2, 3,"Critical"],
    ["Phase 1","Documentation PDF",                "Tech Writer",  2, 3,"Critical"],
    ["Phase 2","Build 8-12 inner pages/site",      "Design+Dev",   4, 6,"High"],
    ["Phase 2","Full visual redesign",             "Designer",     4, 5,"High"],
    ["Phase 2","Scroll animations (AOS.js)",       "Frontend Dev", 5, 6,"High"],
    ["Phase 2","Dark mode variant",                "Designer",     5, 6,"High"],
    ["Phase 2","WebP images + minification",       "Frontend Dev", 6, 6,"High"],
    ["Phase 2","Retina screenshots + promo video", "Marketing",    6, 6,"High"],
    ["Phase 3","RTL + multi-language layout",      "Frontend Dev", 7, 8,"Medium"],
    ["Phase 3","Gulp/Webpack pipeline",            "Frontend Dev", 7, 8,"Medium"],
    ["Phase 3","CSS colour skin presets (3+)",     "Designer",     8, 9,"Medium"],
    ["Phase 3","Schema.org structured data",       "Frontend Dev", 9, 9,"Medium"],
    ["Phase 3","Figma design system add-on",       "Designer",     9,10,"Medium"],
    ["Phase 3","Envato Elements listing",          "Marketing",   10,10,"Medium"],
]

# ── HELPERS ───────────────────────────────────────────────────────────
def avg(lst): return sum(lst) / len(lst)

def rag_label(score):
    if score <= 2: return "🔴 Critical"
    if score <= 4: return "🟡 Major Gap"
    if score <= 6: return "🟢 Moderate"
    return "🔵 Ready"

def plotly_cfg():
    return {"displayModeBar": False, "responsive": True}

def base_layout(**kw):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=30, b=10),
        font=dict(family="DM Sans, sans-serif", size=11, color="#1A2332"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        **kw,
    )

# ── FILTER DATA BY TEMPLATE ───────────────────────────────────────────
def filter_scores(tmpl):
    if tmpl == "W1 – Architect": return W1_SCORES
    if tmpl == "W2 – Business":  return W2_SCORES
    if tmpl == "W3 – Course":    return W3_SCORES
    return None

# ══ SIDEBAR ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📊 Dashboard Controls")
    st.markdown("---")
    tmpl = st.selectbox(
        "Filter by Template",
        ["All Templates", "W1 – Architect", "W2 – Business", "W3 – Course"],
    )
    st.markdown("---")
    page = st.radio(
        "Navigate to",
        ["📊 Overview", "🔽 Conversion Funnel", "📈 Sales Trend",
         "🌐 Traffic Sources", "💰 Revenue Projection",
         "⚠️ Gap Matrix", "🗓 Action Roadmap"],
    )
    st.markdown("---")
    st.markdown("**Data source**")
    st.caption("ThemeForest_Dashboard_SampleData.xlsx")
    st.caption("Sample data — replace with live submissions")

# ── COVER BANNER ──────────────────────────────────────────────────────
st.markdown("""
<div class="cover-banner">
  <h1>ThemeForest Gap Analysis Dashboard</h1>
  <p>3 Website Templates &nbsp;·&nbsp; Marketplace Readiness &nbsp;·&nbsp;
     Conversion &amp; Revenue KPIs &nbsp;·&nbsp; Sample Data</p>
</div>
""", unsafe_allow_html=True)

# ── KPI TILES ─────────────────────────────────────────────────────────
def show_kpis(tmpl):
    if tmpl == "W1 – Architect":
        kpis = [("Avg Readiness", f"{avg(W1_SCORES):.1f}/10", "Target 8.0+", "inverse"),
                ("Conv. Rate",    "0.030%",  "Target 0.34%",  "inverse"),
                ("Critical Gaps","16",       "Must fix first","inverse"),
                ("Mod. Revenue", "$3,019",   "Y1 @ 62.5%",    "normal"),
                ("Traffic (30d)","2,460",    "Visitors",       "normal"),
                ("Units (90d)",  "61",       "W1 Architect",   "normal")]
    elif tmpl == "W2 – Business":
        kpis = [("Avg Readiness", f"{avg(W2_SCORES):.1f}/10", "Target 8.0+", "inverse"),
                ("Conv. Rate",    "0.040%",  "Target 0.34%",  "inverse"),
                ("Critical Gaps","17",       "Must fix first","inverse"),
                ("Mod. Revenue", "$2,144",   "Y1 @ 62.5%",    "normal"),
                ("Traffic (30d)","3,925",    "Visitors",       "normal"),
                ("Units (90d)",  "87",       "W2 Business",    "normal")]
    elif tmpl == "W3 – Course":
        kpis = [("Avg Readiness", f"{avg(W3_SCORES):.1f}/10", "Target 8.0+", "inverse"),
                ("Conv. Rate",    "0.050%",  "Target 0.34%",  "inverse"),
                ("Critical Gaps","16",       "Must fix first","inverse"),
                ("Mod. Revenue", "$3,456",   "Y1 @ 62.5%",    "normal"),
                ("Traffic (30d)","4,000",    "Visitors",       "normal"),
                ("Units (90d)",  "127",      "W3 Course",      "normal")]
    else:
        combined = f"{avg([avg(W1_SCORES),avg(W2_SCORES),avg(W3_SCORES)]):.1f}/10"
        kpis = [("Avg Readiness", combined,  "Target 8.0+",   "inverse"),
                ("Conv. Rate",    "0.040%",  "Target 0.34%",  "inverse"),
                ("Critical Gaps","17",       "Must fix first","inverse"),
                ("Mod. Revenue", "$8,619",   "Portfolio Y1",  "normal"),
                ("Traffic (30d)","10,385",   "Visitors",       "normal"),
                ("Units (90d)",  "275",      "All templates",  "normal")]

    cols = st.columns(6)
    for col, (label, val, delta, direction) in zip(cols, kpis):
        col.metric(label, val, delta, delta_color=direction)

show_kpis(tmpl)
st.markdown("---")

# ══════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════════════════
if page == "📊 Overview":
    st.header("Readiness Scorecard")

    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.subheader("Scores vs Target — all criteria")
        fig = go.Figure()
        fig.add_bar(name="W1 Architect", x=READINESS_CRITERIA, y=W1_SCORES,
                    marker_color=C["w1"], opacity=0.85)
        fig.add_bar(name="W2 Business",  x=READINESS_CRITERIA, y=W2_SCORES,
                    marker_color=C["w2"], opacity=0.85)
        fig.add_bar(name="W3 Course",    x=READINESS_CRITERIA, y=W3_SCORES,
                    marker_color=C["w3"], opacity=0.85)
        fig.add_scatter(name="Target", x=READINESS_CRITERIA, y=TGT_SCORES,
                        mode="lines+markers", line=dict(color=C["tgt"], width=2, dash="dot"),
                        marker=dict(size=6))
        fig.update_layout(**base_layout(barmode="group", yaxis_range=[0, 11],
                          xaxis_tickangle=-40, height=300))
        st.plotly_chart(fig, use_container_width=True, config=plotly_cfg())

    with col2:
        st.subheader("RAG Status Scorecard")
        rag_data = []
        for i, c in enumerate(READINESS_CRITERIA):
            a = avg([W1_SCORES[i], W2_SCORES[i], W3_SCORES[i]])
            rag_data.append({
                "Criterion": c, "W1": W1_SCORES[i],
                "W2": W2_SCORES[i], "W3": W3_SCORES[i],
                "Status": rag_label(a),
            })
        df_rag = pd.DataFrame(rag_data)
        st.dataframe(df_rag, use_container_width=True, height=300,
                     hide_index=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Avg Readiness vs Target")
        fig2 = go.Figure()
        fig2.add_bar(x=["W1 Architect","W2 Business","W3 Course"],
                     y=[round(avg(W1_SCORES),2), round(avg(W2_SCORES),2), round(avg(W3_SCORES),2)],
                     marker_color=[C["w1"],C["w2"],C["w3"]])
        fig2.add_scatter(x=["W1 Architect","W2 Business","W3 Course"], y=[8,8,8],
                         mode="lines", name="Target",
                         line=dict(color=C["tgt"], width=2, dash="dash"))
        fig2.update_layout(**base_layout(yaxis_range=[0,10], height=240, showlegend=False))
        st.plotly_chart(fig2, use_container_width=True, config=plotly_cfg())

    with c2:
        st.subheader("Zero-Score Gaps")
        z = [W1_SCORES.count(0), W2_SCORES.count(0), W3_SCORES.count(0)]
        fig3 = go.Figure(go.Pie(
            labels=["W1 Architect","W2 Business","W3 Course"], values=z,
            marker_colors=[C["w1"],C["w2"],C["w3"]], hole=0.6,
        ))
        fig3.update_layout(**base_layout(height=240))
        st.plotly_chart(fig3, use_container_width=True, config=plotly_cfg())

    with c3:
        st.subheader("Competitor Benchmark")
        fig4 = go.Figure(go.Bar(
            x=COMP_SALES, y=COMP_NAMES, orientation="h",
            marker_color="#BDD7EE",
        ))
        fig4.update_layout(**base_layout(height=240, xaxis_title="Lifetime Sales"))
        st.plotly_chart(fig4, use_container_width=True, config=plotly_cfg())

# ══════════════════════════════════════════════════════════════════════
# PAGE: CONVERSION FUNNEL
# ══════════════════════════════════════════════════════════════════════
elif page == "🔽 Conversion Funnel":
    st.header("Conversion Funnel")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Current vs Optimised (per 10k impressions)")
        fig = go.Figure()
        fig.add_bar(name="W1", x=FUNNEL_STAGES, y=FUNNEL_W1, marker_color=C["w1"]+"CC")
        fig.add_bar(name="W2", x=FUNNEL_STAGES, y=FUNNEL_W2, marker_color=C["w2"]+"CC")
        fig.add_bar(name="W3", x=FUNNEL_STAGES, y=FUNNEL_W3, marker_color=C["w3"]+"CC")
        fig.add_bar(name="Optimised", x=FUNNEL_STAGES, y=FUNNEL_OPT,
                    marker_color="rgba(226,75,74,.2)",
                    marker_line=dict(color=C["tgt"], width=1.5))
        fig.update_layout(**base_layout(barmode="group", height=320, xaxis_tickangle=-30))
        st.plotly_chart(fig, use_container_width=True, config=plotly_cfg())

    with col2:
        st.subheader("Stage Waterfall — Avg Current vs Optimised")
        avgs = [round((a+b+c)/3) for a,b,c in zip(FUNNEL_W1, FUNNEL_W2, FUNNEL_W3)]
        df_fw = pd.DataFrame({
            "Stage": FUNNEL_STAGES,
            "Avg Current": avgs,
            "Optimised":   FUNNEL_OPT,
        })
        st.dataframe(df_fw, use_container_width=True, height=250, hide_index=True)
        st.info("**Final conversion rate:** Current **0.04%** → Optimised **0.34%** = **8.5× uplift**")

    st.subheader("Uplift Multiplier per Stage")
    uplifts = []
    for i in range(1, len(FUNNEL_STAGES)):
        a = avg([FUNNEL_W1[i], FUNNEL_W2[i], FUNNEL_W3[i]])
        uplifts.append(round(FUNNEL_OPT[i] / a, 1) if a > 0 else 0)
    colours = [C["tgt"] if u > 50 else C["w2"] if u > 10 else C["w3"] for u in uplifts]
    fig5 = go.Figure(go.Bar(
        x=FUNNEL_STAGES[1:], y=uplifts,
        marker_color=colours, text=uplifts, textposition="outside",
    ))
    fig5.update_layout(**base_layout(height=220, yaxis_title="× Uplift", showlegend=False))
    st.plotly_chart(fig5, use_container_width=True, config=plotly_cfg())

# ══════════════════════════════════════════════════════════════════════
# PAGE: SALES TREND
# ══════════════════════════════════════════════════════════════════════
elif page == "📈 Sales Trend":
    st.header("Sales Trend — 90 Days")

    st.subheader("Weekly Units Sold — Rolling Trend")
    fig = go.Figure()
    fig.add_scatter(name="W1 Architect ($69)", x=SALES_DATES, y=SALES_W1,
                    mode="lines+markers", line=dict(color=C["w1"], width=2),
                    fill="tozeroy", fillcolor=C["w1"]+"18")
    fig.add_scatter(name="W2 Business ($49)",  x=SALES_DATES, y=SALES_W2,
                    mode="lines+markers", line=dict(color=C["w2"], width=2, dash="dash"),
                    fill="tozeroy", fillcolor=C["w2"]+"18")
    fig.add_scatter(name="W3 Course ($79)",    x=SALES_DATES, y=SALES_W3,
                    mode="lines+markers", line=dict(color=C["w3"], width=2, dash="dot"),
                    fill="tozeroy", fillcolor=C["w3"]+"18")
    fig.update_layout(**base_layout(height=280))
    st.plotly_chart(fig, use_container_width=True, config=plotly_cfg())

    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Revenue Mix (90d)")
        fig2 = go.Figure(go.Pie(
            labels=["W1 $2,631","W2 $2,664","W3 $6,271"],
            values=[2631, 2664, 6271],
            marker_colors=[C["w1"],C["w2"],C["w3"]], hole=0.55,
        ))
        fig2.update_layout(**base_layout(height=240))
        st.plotly_chart(fig2, use_container_width=True, config=plotly_cfg())

    with c2:
        st.subheader("Units by Template (90d)")
        fig3 = go.Figure(go.Bar(
            x=["W1 Architect","W2 Business","W3 Course"], y=[61, 87, 127],
            marker_color=[C["w1"],C["w2"],C["w3"]],
            text=[61, 87, 127], textposition="outside",
        ))
        fig3.update_layout(**base_layout(height=240, showlegend=False))
        st.plotly_chart(fig3, use_container_width=True, config=plotly_cfg())

    with c3:
        st.subheader("Cumulative Revenue (90d)")
        cum1 = [sum(SALES_W1[:i+1])*69*0.625 for i in range(len(SALES_W1))]
        cum2 = [sum(SALES_W2[:i+1])*49*0.625 for i in range(len(SALES_W2))]
        cum3 = [sum(SALES_W3[:i+1])*79*0.625 for i in range(len(SALES_W3))]
        fig4 = go.Figure()
        fig4.add_scatter(name="W1", x=SALES_DATES, y=cum1,
                         line=dict(color=C["w1"]), fill="tozeroy", fillcolor=C["w1"]+"22")
        fig4.add_scatter(name="W2", x=SALES_DATES, y=cum2,
                         line=dict(color=C["w2"]), fill="tozeroy", fillcolor=C["w2"]+"22")
        fig4.add_scatter(name="W3", x=SALES_DATES, y=cum3,
                         line=dict(color=C["w3"]), fill="tozeroy", fillcolor=C["w3"]+"22")
        fig4.update_layout(**base_layout(height=240,
                           yaxis=dict(tickprefix="$", tickformat=".0f")))
        st.plotly_chart(fig4, use_container_width=True, config=plotly_cfg())

# ══════════════════════════════════════════════════════════════════════
# PAGE: TRAFFIC SOURCES
# ══════════════════════════════════════════════════════════════════════
elif page == "🌐 Traffic Sources":
    st.header("Traffic Sources — Last 30 Days")

    totals = [a+b+c for a,b,c in zip(TRAFFIC_W1, TRAFFIC_W2, TRAFFIC_W3)]
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Visitors by Channel — Stacked")
        fig = go.Figure()
        fig.add_bar(name="W1", y=TRAFFIC_CHANNELS, x=TRAFFIC_W1,
                    orientation="h", marker_color=C["w1"]+"CC")
        fig.add_bar(name="W2", y=TRAFFIC_CHANNELS, x=TRAFFIC_W2,
                    orientation="h", marker_color=C["w2"]+"CC")
        fig.add_bar(name="W3", y=TRAFFIC_CHANNELS, x=TRAFFIC_W3,
                    orientation="h", marker_color=C["w3"]+"CC")
        fig.update_layout(**base_layout(barmode="stack", height=340))
        st.plotly_chart(fig, use_container_width=True, config=plotly_cfg())

    with col2:
        st.subheader("Channel Share — Combined")
        pie_cols = ["#378ADD","#EF9F27","#1D9E75","#BDD7EE",
                    "#FAC775","#A7F3D0","#FCA5A5","#C4B5FD"]
        fig2 = go.Figure(go.Pie(
            labels=TRAFFIC_CHANNELS, values=totals,
            marker_colors=pie_cols,
        ))
        fig2.update_layout(**base_layout(height=280))
        st.plotly_chart(fig2, use_container_width=True, config=plotly_cfg())

        df_tr = pd.DataFrame({
            "Channel": TRAFFIC_CHANNELS,
            "W1": TRAFFIC_W1, "W2": TRAFFIC_W2,
            "W3": TRAFFIC_W3, "Total": totals,
        })
        st.dataframe(df_tr, use_container_width=True, height=200, hide_index=True)

# ══════════════════════════════════════════════════════════════════════
# PAGE: REVENUE PROJECTION
# ══════════════════════════════════════════════════════════════════════
elif page == "💰 Revenue Projection":
    st.header("Year-1 Revenue Projection")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Revenue by Scenario per Template ($)")
        fig = go.Figure()
        fig.add_bar(name="W1 Architect", x=REV_SCENARIOS, y=REV_W1,
                    marker_color="#4FA6E8", text=REV_W1, textposition="outside")
        fig.add_bar(name="W2 Business",  x=REV_SCENARIOS, y=REV_W2,
                    marker_color=C["w2"], text=REV_W2, textposition="outside")
        fig.add_bar(name="W3 Course",    x=REV_SCENARIOS, y=REV_W3,
                    marker_color=C["w3"], text=REV_W3, textposition="outside")
        fig.update_layout(**base_layout(barmode="group", height=320,
                          yaxis=dict(tickprefix="$")))
        st.plotly_chart(fig, use_container_width=True, config=plotly_cfg())

    with col2:
        st.subheader("Portfolio Total by Scenario")
        port = [r1+r2+r3 for r1,r2,r3 in zip(REV_W1, REV_W2, REV_W3)]
        fig2 = go.Figure(go.Bar(
            x=REV_SCENARIOS, y=port,
            marker_color=["#BDD7EE","#9FE1CB","#85B7EB"],
            text=[f"${v:,}" for v in port], textposition="outside",
        ))
        fig2.update_layout(**base_layout(height=220, showlegend=False,
                           yaxis=dict(tickprefix="$")))
        st.plotly_chart(fig2, use_container_width=True, config=plotly_cfg())

        df_rev = pd.DataFrame({
            "Scenario": REV_SCENARIOS,
            "W1 ($)": REV_W1, "W2 ($)": REV_W2,
            "W3 ($)": REV_W3,
            "Portfolio ($)": port,
        })
        st.dataframe(df_rev, use_container_width=True, hide_index=True)
        st.caption("Prices: W1 $69 · W2 $49 · W3 $79 · Author share 62.5%")

    st.subheader("Competitor Lifetime Sales Benchmark")
    fig3 = go.Figure(go.Bar(
        x=COMP_NAMES, y=COMP_SALES,
        marker_color="#CBD5E1",
        text=COMP_SALES, textposition="outside",
    ))
    fig3.update_layout(**base_layout(height=220, showlegend=False,
                       yaxis_title="Lifetime Sales"))
    st.plotly_chart(fig3, use_container_width=True, config=plotly_cfg())

# ══════════════════════════════════════════════════════════════════════
# PAGE: GAP MATRIX
# ══════════════════════════════════════════════════════════════════════
elif page == "⚠️ Gap Matrix":
    st.header("Feature Gap Matrix")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Gap Count by Template")
        no_counts  = [sum(1 for g in GAPS if g[i+1]=="No")      for i in range(3)]
        par_counts = [sum(1 for g in GAPS if g[i+1]=="Partial")  for i in range(3)]
        na_counts  = [sum(1 for g in GAPS if g[i+1]=="N/A")      for i in range(3)]
        labels = ["W1 Architect","W2 Business","W3 Course"]
        fig = go.Figure()
        fig.add_bar(name="No",      x=labels, y=no_counts,  marker_color="#FCA5A5")
        fig.add_bar(name="Partial", x=labels, y=par_counts, marker_color="#FDE68A")
        fig.add_bar(name="N/A",     x=labels, y=na_counts,  marker_color="#E2E8F0")
        fig.update_layout(**base_layout(barmode="stack", height=260))
        st.plotly_chart(fig, use_container_width=True, config=plotly_cfg())

    with c2:
        st.subheader("Priority Breakdown")
        pri_counts = {
            "Critical": sum(1 for g in GAPS if g[4]=="Critical"),
            "High":     sum(1 for g in GAPS if g[4]=="High"),
            "Medium":   sum(1 for g in GAPS if g[4]=="Medium"),
        }
        fig2 = go.Figure(go.Pie(
            labels=list(pri_counts.keys()),
            values=list(pri_counts.values()),
            marker_colors=["#FCA5A5","#FDE68A","#BBF7D0"], hole=0.55,
            textinfo="label+value",
        ))
        fig2.update_layout(**base_layout(height=260))
        st.plotly_chart(fig2, use_container_width=True, config=plotly_cfg())

    st.subheader("Feature Presence Matrix — 20 Critical Requirements")

    def color_gap(val):
        if val == "No":      return "background-color:#FEE2E2; color:#991B1B; font-weight:600"
        if val == "Yes":     return "background-color:#DCFCE7; color:#166534; font-weight:600"
        if val == "Partial": return "background-color:#FEF3C7; color:#92400E; font-weight:600"
        if val == "N/A":     return "color:#94A3B8"
        if val == "Critical":return "background-color:#FEE2E2; color:#991B1B; font-weight:600"
        if val == "High":    return "background-color:#FEF3C7; color:#92400E; font-weight:600"
        if val == "Medium":  return "background-color:#DCFCE7; color:#166534"
        return ""

    df_gaps = pd.DataFrame(GAPS, columns=["Feature","W1 Architect","W2 Business","W3 Course","Priority"])
    styled = df_gaps.style.applymap(color_gap,
                                    subset=["W1 Architect","W2 Business","W3 Course","Priority"])
    st.dataframe(styled, use_container_width=True, height=500, hide_index=True)

# ══════════════════════════════════════════════════════════════════════
# PAGE: ACTION ROADMAP
# ══════════════════════════════════════════════════════════════════════
elif page == "🗓 Action Roadmap":
    st.header("10-Week Action Roadmap")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Tasks by Phase")
        phase_counts = {"Phase 1": 0, "Phase 2": 0, "Phase 3": 0}
        for t in ROADMAP: phase_counts[t[0]] += 1
        fig = go.Figure(go.Pie(
            labels=list(phase_counts.keys()),
            values=list(phase_counts.values()),
            marker_colors=["#BFDBFE","#FDE68A","#BBF7D0"], hole=0.55,
        ))
        fig.update_layout(**base_layout(height=230))
        st.plotly_chart(fig, use_container_width=True, config=plotly_cfg())

    with c2:
        st.subheader("Tasks by Owner")
        owner_counts = {}
        for t in ROADMAP:
            owner_counts[t[2]] = owner_counts.get(t[2], 0) + 1
        fig2 = go.Figure(go.Bar(
            y=list(owner_counts.keys()), x=list(owner_counts.values()),
            orientation="h", marker_color=C["w1"],
            text=list(owner_counts.values()), textposition="outside",
        ))
        fig2.update_layout(**base_layout(height=230, showlegend=False))
        st.plotly_chart(fig2, use_container_width=True, config=plotly_cfg())

    with c3:
        st.subheader("Priority Split")
        pri_c = {"Critical":0,"High":0,"Medium":0}
        for t in ROADMAP: pri_c[t[5]] += 1
        fig3 = go.Figure(go.Bar(
            x=list(pri_c.keys()), y=list(pri_c.values()),
            marker_color=["#FCA5A5","#FDE68A","#BBF7D0"],
            text=list(pri_c.values()), textposition="outside",
        ))
        fig3.update_layout(**base_layout(height=230, showlegend=False))
        st.plotly_chart(fig3, use_container_width=True, config=plotly_cfg())

    st.subheader("Gantt — All 18 Tasks (10 Weeks)")

    # Build Gantt with plotly timeline
    df_road = pd.DataFrame(ROADMAP,
        columns=["Phase","Task","Owner","Start Wk","End Wk","Priority"])

    phase_colors = {"Phase 1": "#93C5FD", "Phase 2": "#FDE68A", "Phase 3": "#BBF7D0"}
    fig_gantt = go.Figure()
    for _, row in df_road.iterrows():
        fig_gantt.add_shape(
            type="rect",
            x0=row["Start Wk"] - 0.4, x1=row["End Wk"] + 0.4,
            y0=row.name - 0.35, y1=row.name + 0.35,
            fillcolor=phase_colors.get(row["Phase"], "#E2E8F0"),
            line=dict(width=0),
        )
        fig_gantt.add_annotation(
            x=(row["Start Wk"] + row["End Wk"]) / 2,
            y=row.name, text=row["Task"],
            showarrow=False, font=dict(size=9, color="#1A2332"),
            xanchor="center",
        )

    fig_gantt.update_layout(
        **base_layout(
            height=520,
            xaxis=dict(title="Week", tickmode="linear", tick0=1, dtick=1,
                       range=[0.5, 10.5], gridcolor="#F0F4F8"),
            yaxis=dict(tickmode="array",
                       tickvals=list(range(len(ROADMAP))),
                       ticktext=[f"{t[0]} · {t[2]}" for t in ROADMAP],
                       autorange="reversed"),
            showlegend=False,
        )
    )
    st.plotly_chart(fig_gantt, use_container_width=True, config=plotly_cfg())

    def color_pri(val):
        if val == "Critical": return "background-color:#FEE2E2;color:#991B1B;font-weight:600"
        if val == "High":     return "background-color:#FEF3C7;color:#92400E;font-weight:600"
        if val == "Medium":   return "background-color:#DCFCE7;color:#166534"
        return ""

    st.subheader("Task Table")
    styled_road = df_road.style.applymap(color_pri, subset=["Priority"])
    st.dataframe(styled_road, use_container_width=True, height=400, hide_index=True)
