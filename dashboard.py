"""
ThemeForest Gap Analysis Dashboard
====================================
Uses ONLY Streamlit built-in charts — no plotly, no pandas, no extra installs.
Deploy on Streamlit Cloud with requirements.txt containing just:  streamlit

Run locally:
    pip install streamlit
    streamlit run dashboard.py
"""

import streamlit as st

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
[data-testid="stAppViewContainer"]  { background:#F0F4F8; }
[data-testid="stSidebar"]           { background:#1F4E78; }
[data-testid="stSidebar"] *         { color:#ffffff !important; }
[data-testid="stSidebar"] select    { color:#000 !important; }
.block-container                    { padding-top:1rem; padding-bottom:2rem; }
div[data-testid="metric-container"] {
    background:white; border-radius:10px;
    padding:12px; box-shadow:0 1px 4px rgba(0,0,0,.06);
}
.cover-banner {
    background:linear-gradient(135deg,#1F4E78 0%,#2563EB 60%,#1D9E75 100%);
    padding:22px 28px; border-radius:12px; margin-bottom:16px; color:white;
}
.cover-banner h2 { color:white !important; margin:0; }
.cover-banner p  { margin:4px 0 0; opacity:.8; font-size:.85rem; }
table.gap-tbl { width:100%; border-collapse:collapse; font-size:12px; }
table.gap-tbl th { background:#1F4E78; color:white; padding:6px 8px; text-align:left; }
table.gap-tbl td { padding:5px 8px; border-bottom:1px solid #E2E8F0; }
table.gap-tbl tr:nth-child(even) td { background:#F8FAFC; }
.no      { color:#991B1B; font-weight:700; }
.yes     { color:#166534; font-weight:700; }
.partial { color:#92400E; font-weight:700; }
.na      { color:#94A3B8; }
.pcr  { background:#FEE2E2; color:#991B1B; padding:2px 8px;
         border-radius:10px; font-size:11px; font-weight:700; }
.pmj  { background:#FEF3C7; color:#92400E; padding:2px 8px;
         border-radius:10px; font-size:11px; font-weight:700; }
.pmo  { background:#DCFCE7; color:#166534; padding:2px 8px;
         border-radius:10px; font-size:11px; font-weight:700; }
</style>
""", unsafe_allow_html=True)

# ══ DATA ══════════════════════════════════════════════════════════════

CRITERIA = [
    "Design Originality","Typography System","Colour & Identity",
    "Animation / Motion","Inner Page Count","Responsiveness",
    "UX / Navigation","Code Quality","Performance","Accessibility (WCAG)",
    "Documentation","Support Infrastructure","Marketplace Listing",
]
W1 = [3,3,4,0,1,5,4,4,5,2,0,0,0]
W2 = [4,4,4,0,1,5,5,4,5,3,0,0,0]
W3 = [5,4,5,2,2,6,5,5,5,3,0,0,0]
TG = [8,8,8,7,10,9,8,8,8,8,8,8,8]

FUNNEL_STAGES = ["TF Search","Click Thumbnail","Watch Video",
                 "Live Preview","Read Description","Add to Cart","Purchase"]
FW1  = [10000,180,0,25,38,4,3]
FW2  = [10000,210,0,32,44,5,4]
FW3  = [10000,240,5,38,52,6,5]
FOPT = [10000,1200,540,780,660,42,34]

SDATES = ["5-Feb","12-Feb","19-Feb","26-Feb","5-Mar","12-Mar","19-Mar",
          "26-Mar","2-Apr","9-Apr","16-Apr","23-Apr","30-Apr"]
SW1 = [4,5,5,6,7,7,8,6,7,8,9,8,10]
SW2 = [6,7,8,8,9,10,9,11,10,12,11,13,12]
SW3 = [9,11,13,12,14,13,15,16,14,17,16,18,19]

TCH = ["TF Search","Direct/Demo","Google Organic","YouTube",
       "Dribbble/Behance","Reddit/Forums","Email","Affiliate"]
TW1 = [1240,420,310,85,260,70,45,30]
TW2 = [2100,680,540,140,120,180,90,75]
TW3 = [1850,590,720,430,90,150,110,60]

SCEN = ["Conservative","Moderate","Optimistic"]
RW1  = [1509,3019,6038]
RW2  = [1072,2144,4288]
RW3  = [1728,3456,6913]

CNAMES = ["Avada","Flatsome","Divi","Bridge","Jupiter X","Astra Pro","Webflow","MOJO"]
CSALES = [4830,3200,2950,2070,1800,1450,1200,650]

GAPS = [
    ["Responsive Layout",       "Partial","Partial","Partial","Critical"],
    ["Sticky Header",           "No","No","No","Critical"],
    ["Mobile Hamburger Menu",   "Partial","Partial","Partial","Critical"],
    ["Contact Form+Validation", "No","No","No","Critical"],
    ["GDPR Cookie Consent",     "No","No","No","Critical"],
    ["Cross-browser Tested",    "No","No","No","Critical"],
    ["WCAG Keyboard Nav",       "No","No","No","Critical"],
    ["Documentation",           "No","No","No","Critical"],
    ["Smooth Scrolling",        "No","No","Partial","High"],
    ["Back-to-Top Button",      "No","No","No","High"],
    ["404 Error Page",          "No","No","No","Critical"],
    ["Search Functionality",    "No","No","No","High"],
    ["Dark Mode Variant",       "No","No","No","High"],
    ["Pricing Tables",          "N/A","No","No","Critical"],
    ["Testimonials Section",    "No","No","No","High"],
    ["Team / Instructor",       "No","No","No","High"],
    ["FAQ Accordion",           "No","No","No","High"],
    ["Video Lightbox",          "N/A","N/A","No","High"],
    ["Social Share Buttons",    "No","No","No","Medium"],
    ["Schema.org Data",         "No","No","No","Medium"],
]

ROADMAP = [
    ["Phase 1","Responsive layout (320-2560px)",  "Frontend Dev",1,3,"Critical"],
    ["Phase 1","Contact forms + validation",       "Frontend Dev",1,2,"Critical"],
    ["Phase 1","GDPR cookie consent",              "Frontend Dev",1,1,"Critical"],
    ["Phase 1","W3C HTML validate",                "Frontend Dev",2,3,"Critical"],
    ["Phase 1","Fix JS errors & broken links",     "Frontend Dev",2,3,"Critical"],
    ["Phase 1","Documentation PDF",                "Tech Writer", 2,3,"Critical"],
    ["Phase 2","Build 8-12 inner pages/site",      "Design+Dev",  4,6,"High"],
    ["Phase 2","Full visual redesign",             "Designer",    4,5,"High"],
    ["Phase 2","Scroll animations (AOS.js)",       "Frontend Dev",5,6,"High"],
    ["Phase 2","Dark mode variant",                "Designer",    5,6,"High"],
    ["Phase 2","WebP images + minification",       "Frontend Dev",6,6,"High"],
    ["Phase 2","Retina screenshots + promo video", "Marketing",   6,6,"High"],
    ["Phase 3","RTL + multi-language layout",      "Frontend Dev",7,8,"Medium"],
    ["Phase 3","Gulp/Webpack pipeline",            "Frontend Dev",7,8,"Medium"],
    ["Phase 3","CSS colour skin presets (3+)",     "Designer",    8,9,"Medium"],
    ["Phase 3","Schema.org structured data",       "Frontend Dev",9,9,"Medium"],
    ["Phase 3","Figma design system add-on",       "Designer",    9,10,"Medium"],
    ["Phase 3","Envato Elements listing",          "Marketing",  10,10,"Medium"],
]

# ── HELPERS ───────────────────────────────────────────────────────────
def avg(lst):
    return round(sum(lst) / len(lst), 2)

def rag(score):
    if score <= 2: return "🔴 Critical"
    if score <= 4: return "🟡 Major Gap"
    if score <= 6: return "🟢 Moderate"
    return "🔵 Ready"

def pill(p):
    cls = "pcr" if p == "Critical" else "pmj" if p == "High" else "pmo"
    return f'<span class="{cls}">{p}</span>'

def gap_cell(v):
    cls = "no" if v == "No" else "yes" if v == "Yes" else "partial" if v == "Partial" else "na"
    return f'<span class="{cls}">{v}</span>'

# ══ SIDEBAR ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📊 Dashboard")
    st.markdown("---")
    tmpl = st.selectbox("Template Filter", [
        "All Templates","W1 – Architect","W2 – Business","W3 – Course"
    ])
    st.markdown("---")
    page = st.radio("Navigate", [
        "📊 Overview",
        "🔽 Conversion Funnel",
        "📈 Sales Trend",
        "🌐 Traffic Sources",
        "💰 Revenue Projection",
        "⚠️  Gap Matrix",
        "🗓  Action Roadmap",
    ])
    st.markdown("---")
    st.caption("ThemeForest Gap Analysis")
    st.caption("Sample data — replace with live submissions")

# ── BANNER ────────────────────────────────────────────────────────────
st.markdown("""
<div class="cover-banner">
  <h2>📊 ThemeForest Gap Analysis Dashboard</h2>
  <p>3 Website Templates &nbsp;·&nbsp; Marketplace Readiness
     &nbsp;·&nbsp; Conversion &amp; Revenue KPIs</p>
</div>
""", unsafe_allow_html=True)

# ── KPI ROW ───────────────────────────────────────────────────────────
def show_kpis(tmpl):
    if tmpl == "W1 – Architect":
        v = [f"{avg(W1)}/10","0.030%","16","$3,019","2,460","61"]
    elif tmpl == "W2 – Business":
        v = [f"{avg(W2)}/10","0.040%","17","$2,144","3,925","87"]
    elif tmpl == "W3 – Course":
        v = [f"{avg(W3)}/10","0.050%","16","$3,456","4,000","127"]
    else:
        combined = round((avg(W1)+avg(W2)+avg(W3))/3, 1)
        v = [f"{combined}/10","0.040%","17","$8,619","10,385","275"]

    labels = ["Avg Readiness","Conv. Rate","Critical Gaps",
              "Mod. Y1 Revenue","Traffic (30d)","Units (90d)"]
    deltas = ["Target 8.0+","Target 0.34%","Must fix","62.5% share","Visitors","All templates"]
    cols = st.columns(6)
    for col, lbl, val, dlt in zip(cols, labels, v, deltas):
        col.metric(lbl, val, dlt)

show_kpis(tmpl)
st.markdown("---")

# ══════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════
if page == "📊 Overview":
    st.header("Readiness Scorecard")

    col1, col2 = st.columns([1.4, 1])
    with col1:
        st.subheader("Scores vs Target — all criteria")
        st.bar_chart({
            "W1 Architect": dict(zip(CRITERIA, W1)),
            "W2 Business":  dict(zip(CRITERIA, W2)),
            "W3 Course":    dict(zip(CRITERIA, W3)),
            "Target":       dict(zip(CRITERIA, TG)),
        }, height=320)

    with col2:
        st.subheader("RAG Status Scorecard")
        rows = ""
        for i, c in enumerate(CRITERIA):
            a = avg([W1[i], W2[i], W3[i]])
            rows += f"<tr><td>{c}</td><td>{W1[i]}</td><td>{W2[i]}</td><td>{W3[i]}</td><td>{rag(a)}</td></tr>"
        st.markdown(f"""
        <div style="overflow-y:auto;max-height:320px">
        <table class="gap-tbl">
          <thead><tr><th>Criterion</th><th>W1</th><th>W2</th><th>W3</th><th>Status</th></tr></thead>
          <tbody>{rows}</tbody>
        </table></div>""", unsafe_allow_html=True)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Avg Readiness vs Target")
        st.bar_chart({
            "Score":  {"W1 Architect":avg(W1),"W2 Business":avg(W2),"W3 Course":avg(W3)},
            "Target": {"W1 Architect":8,      "W2 Business":8,      "W3 Course":8},
        }, height=220)
    with c2:
        st.subheader("Zero-Score Gaps")
        st.bar_chart({"Gaps": {
            "W1 Architect":W1.count(0),
            "W2 Business": W2.count(0),
            "W3 Course":   W3.count(0),
        }}, height=220)
    with c3:
        st.subheader("Competitor Lifetime Sales")
        st.bar_chart({"Sales": dict(zip(CNAMES, CSALES))}, height=220)

# ══════════════════════════════════════════════════════════════════════
# PAGE 2 — CONVERSION FUNNEL
# ══════════════════════════════════════════════════════════════════════
elif page == "🔽 Conversion Funnel":
    st.header("Conversion Funnel")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Current vs Optimised (per 10k impressions)")
        st.bar_chart({
            "W1":        dict(zip(FUNNEL_STAGES, FW1)),
            "W2":        dict(zip(FUNNEL_STAGES, FW2)),
            "W3":        dict(zip(FUNNEL_STAGES, FW3)),
            "Optimised": dict(zip(FUNNEL_STAGES, FOPT)),
        }, height=320)

    with col2:
        st.subheader("Stage Waterfall — Avg vs Optimised")
        avgs = [round((a+b+c)/3) for a,b,c in zip(FW1,FW2,FW3)]
        rows = ""
        for s, av, op in zip(FUNNEL_STAGES, avgs, FOPT):
            uplift = f"{op/av:.1f}×" if av > 0 else "n/a"
            rows += f"<tr><td>{s}</td><td>{av:,}</td><td>{op:,}</td><td><b>{uplift}</b></td></tr>"
        st.markdown(f"""
        <table class="gap-tbl">
          <thead><tr><th>Stage</th><th>Avg Current</th><th>Optimised</th><th>Uplift</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>""", unsafe_allow_html=True)
        st.info("Conv. rate: **0.04%** current → **0.34%** optimised = **8.5× uplift**")

    st.markdown("---")
    st.subheader("Uplift Multiplier per Stage")
    uplifts = {}
    for i in range(1, len(FUNNEL_STAGES)):
        a = avg([FW1[i], FW2[i], FW3[i]])
        uplifts[FUNNEL_STAGES[i]] = round(FOPT[i]/a, 1) if a > 0 else 0
    st.bar_chart({"Uplift ×": uplifts}, height=200)

# ══════════════════════════════════════════════════════════════════════
# PAGE 3 — SALES TREND
# ══════════════════════════════════════════════════════════════════════
elif page == "📈 Sales Trend":
    st.header("Sales Trend — 90 Days")

    st.subheader("Weekly Units Sold — Rolling Trend")
    st.line_chart({
        "W1 Architect ($69)": dict(zip(SDATES, SW1)),
        "W2 Business ($49)":  dict(zip(SDATES, SW2)),
        "W3 Course ($79)":    dict(zip(SDATES, SW3)),
    }, height=280)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Units by Template (90d)")
        st.bar_chart({"Units": {
            "W1 Architect":61,"W2 Business":87,"W3 Course":127
        }}, height=220)
    with c2:
        st.subheader("Revenue by Template (90d)")
        st.bar_chart({"Revenue ($)": {
            "W1 Architect":2631,"W2 Business":2664,"W3 Course":6271
        }}, height=220)
    with c3:
        st.subheader("Cumulative Revenue (90d)")
        cum1 = [round(sum(SW1[:i+1])*69*0.625) for i in range(len(SW1))]
        cum2 = [round(sum(SW2[:i+1])*49*0.625) for i in range(len(SW2))]
        cum3 = [round(sum(SW3[:i+1])*79*0.625) for i in range(len(SW3))]
        st.line_chart({
            "W1": dict(zip(SDATES, cum1)),
            "W2": dict(zip(SDATES, cum2)),
            "W3": dict(zip(SDATES, cum3)),
        }, height=220)

    st.markdown("---")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("W1 Units",    "61",      "$2,631 revenue")
    c2.metric("W2 Units",    "87",      "$2,664 revenue")
    c3.metric("W3 Units",    "127",     "$6,271 revenue")
    c4.metric("Total Revenue","$11,566","90 days · all templates")

# ══════════════════════════════════════════════════════════════════════
# PAGE 4 — TRAFFIC SOURCES
# ══════════════════════════════════════════════════════════════════════
elif page == "🌐 Traffic Sources":
    st.header("Traffic Sources — Last 30 Days")

    totals = [a+b+c for a,b,c in zip(TW1,TW2,TW3)]
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Visitors by Channel — Stacked")
        st.bar_chart({
            "W1": dict(zip(TCH, TW1)),
            "W2": dict(zip(TCH, TW2)),
            "W3": dict(zip(TCH, TW3)),
        }, height=340)
    with col2:
        st.subheader("Channel Totals — Combined")
        st.bar_chart({"Total Visitors": dict(zip(TCH, totals))}, height=220)
        rows = ""
        for ch, w1, w2, w3, tot in zip(TCH, TW1, TW2, TW3, totals):
            rows += f"<tr><td>{ch}</td><td>{w1:,}</td><td>{w2:,}</td><td>{w3:,}</td><td><b>{tot:,}</b></td></tr>"
        st.markdown(f"""
        <table class="gap-tbl">
          <thead><tr><th>Channel</th><th>W1</th><th>W2</th><th>W3</th><th>Total</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# PAGE 5 — REVENUE PROJECTION
# ══════════════════════════════════════════════════════════════════════
elif page == "💰 Revenue Projection":
    st.header("Year-1 Revenue Projection")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Revenue by Scenario per Template ($)")
        st.bar_chart({
            "W1 Architect": dict(zip(SCEN, RW1)),
            "W2 Business":  dict(zip(SCEN, RW2)),
            "W3 Course":    dict(zip(SCEN, RW3)),
        }, height=300)
    with col2:
        st.subheader("Portfolio Total by Scenario")
        port = [r1+r2+r3 for r1,r2,r3 in zip(RW1,RW2,RW3)]
        st.bar_chart({"Portfolio ($)": dict(zip(SCEN, port))}, height=200)
        rows = ""
        for s,r1,r2,r3,p in zip(SCEN,RW1,RW2,RW3,port):
            rows += f"<tr><td><b>{s}</b></td><td>${r1:,}</td><td>${r2:,}</td><td>${r3:,}</td><td><b>${p:,}</b></td></tr>"
        st.markdown(f"""
        <table class="gap-tbl">
          <thead><tr><th>Scenario</th><th>W1</th><th>W2</th><th>W3</th><th>Portfolio</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>""", unsafe_allow_html=True)
        st.caption("Prices: W1 $69 · W2 $49 · W3 $79 · Author share 62.5%")

    st.markdown("---")
    st.subheader("Competitor Lifetime Sales Benchmark")
    st.bar_chart({"Lifetime Sales": dict(zip(CNAMES, CSALES))}, height=220)

# ══════════════════════════════════════════════════════════════════════
# PAGE 6 — GAP MATRIX
# ══════════════════════════════════════════════════════════════════════
elif page == "⚠️  Gap Matrix":
    st.header("Feature Gap Matrix")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Gap Count by Template")
        labs = ["W1 Architect","W2 Business","W3 Course"]
        st.bar_chart({
            "No (gaps)": dict(zip(labs,[sum(1 for g in GAPS if g[i+1]=="No")     for i in range(3)])),
            "Partial":   dict(zip(labs,[sum(1 for g in GAPS if g[i+1]=="Partial") for i in range(3)])),
            "N/A":       dict(zip(labs,[sum(1 for g in GAPS if g[i+1]=="N/A")    for i in range(3)])),
        }, height=260)
    with c2:
        st.subheader("Priority Breakdown")
        st.bar_chart({"Tasks": {
            "Critical": sum(1 for g in GAPS if g[4]=="Critical"),
            "High":     sum(1 for g in GAPS if g[4]=="High"),
            "Medium":   sum(1 for g in GAPS if g[4]=="Medium"),
        }}, height=260)

    st.markdown("---")
    st.subheader("Feature Presence Matrix — 20 Critical Requirements")
    rows = ""
    for g in GAPS:
        rows += f"""<tr>
          <td>{g[0]}</td>
          <td>{gap_cell(g[1])}</td>
          <td>{gap_cell(g[2])}</td>
          <td>{gap_cell(g[3])}</td>
          <td>{pill(g[4])}</td>
        </tr>"""
    st.markdown(f"""
    <div style="overflow-x:auto">
    <table class="gap-tbl">
      <thead><tr>
        <th>Feature</th><th>W1 Architect</th><th>W2 Business</th>
        <th>W3 Course</th><th>Priority</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# PAGE 7 — ACTION ROADMAP
# ══════════════════════════════════════════════════════════════════════
elif page == "🗓  Action Roadmap":
    st.header("10-Week Action Roadmap")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Tasks by Phase")
        st.bar_chart({"Tasks": {
            "Phase 1": sum(1 for t in ROADMAP if t[0]=="Phase 1"),
            "Phase 2": sum(1 for t in ROADMAP if t[0]=="Phase 2"),
            "Phase 3": sum(1 for t in ROADMAP if t[0]=="Phase 3"),
        }}, height=200)
    with c2:
        st.subheader("Tasks by Owner")
        owner_c = {}
        for t in ROADMAP:
            owner_c[t[2]] = owner_c.get(t[2], 0) + 1
        st.bar_chart({"Tasks": owner_c}, height=200)
    with c3:
        st.subheader("Priority Split")
        st.bar_chart({"Tasks": {
            "Critical": sum(1 for t in ROADMAP if t[5]=="Critical"),
            "High":     sum(1 for t in ROADMAP if t[5]=="High"),
            "Medium":   sum(1 for t in ROADMAP if t[5]=="Medium"),
        }}, height=200)

    st.markdown("---")
    st.subheader("Gantt — 10-Week Timeline")
    phase_colors = {"Phase 1":"#BFDBFE","Phase 2":"#FDE68A","Phase 3":"#BBF7D0"}
    wk_headers = "".join(f"<th>W{i}</th>" for i in range(1,11))
    rows = ""
    last_phase = ""
    for t in ROADMAP:
        if t[0] != last_phase:
            last_phase = t[0]
            bg = phase_colors[t[0]]
            rows += f'<tr><td colspan="14" style="background:{bg};font-weight:700;padding:5px 8px;font-size:11px">{t[0]}</td></tr>'
        wks = ""
        for w in range(1, 11):
            if t[3] <= w <= t[4]:
                wks += f'<td style="background:{phase_colors[t[0]]};border-radius:3px;min-width:24px"></td>'
            else:
                wks += '<td style="background:#F0F4F8;min-width:24px"></td>'
        pri_style = ("color:#991B1B;font-weight:700" if t[5]=="Critical"
                     else "color:#92400E;font-weight:700" if t[5]=="High"
                     else "color:#166534")
        rows += f"""<tr>
          <td style="font-size:11px;min-width:200px">{t[1]}</td>
          <td style="font-size:10px;color:#64748B;min-width:80px">{t[2]}</td>
          {wks}
          <td style="font-size:10px;{pri_style};min-width:60px">{t[5]}</td>
        </tr>"""
    st.markdown(f"""
    <div style="overflow-x:auto">
    <table class="gap-tbl">
      <thead><tr>
        <th style="min-width:200px">Task</th>
        <th style="min-width:80px">Owner</th>
        {wk_headers}
        <th>Priority</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Full Task Table")
    rows2 = ""
    for t in ROADMAP:
        pri_style = ("color:#991B1B;font-weight:700" if t[5]=="Critical"
                     else "color:#92400E;font-weight:700" if t[5]=="High"
                     else "color:#166534")
        rows2 += f"""<tr>
          <td>{pill(t[0])}</td><td>{t[1]}</td><td>{t[2]}</td>
          <td style="text-align:center">{t[3]}</td>
          <td style="text-align:center">{t[4]}</td>
          <td style="{pri_style}">{t[5]}</td>
        </tr>"""
    st.markdown(f"""
    <table class="gap-tbl">
      <thead><tr>
        <th>Phase</th><th>Task</th><th>Owner</th>
        <th>Start Wk</th><th>End Wk</th><th>Priority</th>
      </tr></thead>
      <tbody>{rows2}</tbody>
    </table>""", unsafe_allow_html=True)
