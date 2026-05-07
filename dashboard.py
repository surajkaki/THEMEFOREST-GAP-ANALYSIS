"""
ThemeForest Gap Analysis Dashboard — Web Server
================================================
Serves the dashboard over HTTP so anyone on the network can open it.

Usage:
    python dashboard_server.py              # default port 8080
    python dashboard_server.py --port 5000  # custom port
    python dashboard_server.py --port 80    # standard HTTP (needs sudo on Linux)

Access from any browser:
    http://<YOUR_SERVER_IP>:8080
    e.g.  http://192.168.1.10:8080
          http://123.45.67.89:8080

Stop server:  Ctrl + C
"""

import os
import socket
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler

# ── CONFIG ───────────────────────────────────────────────────────────
DEFAULT_PORT = 8080
OUTPUT_FILE  = "ThemeForest_Dashboard.html"

# ── ALL DATA ─────────────────────────────────────────────────────────
READINESS_CRITERIA = [
    "Design Originality", "Typography System", "Colour & Visual Identity",
    "Animation / Motion", "Inner Page Count", "Responsiveness",
    "UX / Navigation", "Code Quality", "Performance (PageSpeed)",
    "Accessibility (WCAG)", "Documentation", "Support Infrastructure",
    "Marketplace Listing"
]
W1_SCORES  = [3, 3, 4, 0, 1, 5, 4, 4, 5, 2, 0, 0, 0]
W2_SCORES  = [4, 4, 4, 0, 1, 5, 5, 4, 5, 3, 0, 0, 0]
W3_SCORES  = [5, 4, 5, 2, 2, 6, 5, 5, 5, 3, 0, 0, 0]
TGT_SCORES = [8, 8, 8, 7,10, 9, 8, 8, 8, 8, 8, 8, 8]

FUNNEL_STAGES = [
    "TF Search Impressions", "Click Thumbnail", "Watch Video Preview",
    "Click Live Preview", "Read Description", "Add to Cart", "Complete Purchase"
]
FUNNEL_W1  = [10000, 180,   0,  25,  38,  4,  3]
FUNNEL_W2  = [10000, 210,   0,  32,  44,  5,  4]
FUNNEL_W3  = [10000, 240,   5,  38,  52,  6,  5]
FUNNEL_OPT = [10000,1200, 540, 780, 660, 42, 34]

SALES_DATES = ["5-Feb","12-Feb","19-Feb","26-Feb","5-Mar","12-Mar","19-Mar",
               "26-Mar","2-Apr","9-Apr","16-Apr","23-Apr","30-Apr"]
SALES_W1 = [4, 5, 5, 6, 7, 7, 8, 6,  7,  8,  9,  8, 10]
SALES_W2 = [6, 7, 8, 8, 9,10, 9,11, 10, 12, 11, 13, 12]
SALES_W3 = [9,11,13,12,14,13,15,16, 14, 17, 16, 18, 19]

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
    ["Responsive Layout",       "Partial","Partial","Partial","Critical"],
    ["Sticky Header",           "No",    "No",    "No",    "Critical"],
    ["Mobile Hamburger Menu",   "Partial","Partial","Partial","Critical"],
    ["Contact Form+Validation", "No",    "No",    "No",    "Critical"],
    ["GDPR Cookie Consent",     "No",    "No",    "No",    "Critical"],
    ["Cross-browser Tested",    "No",    "No",    "No",    "Critical"],
    ["WCAG Keyboard Nav",       "No",    "No",    "No",    "Critical"],
    ["Documentation (PDF/HTML)","No",    "No",    "No",    "Critical"],
    ["Smooth Scrolling",        "No",    "No",    "Partial","High"],
    ["Back-to-Top Button",      "No",    "No",    "No",    "High"],
    ["404 Error Page",          "No",    "No",    "No",    "Critical"],
    ["Search Functionality",    "No",    "No",    "No",    "High"],
    ["Dark Mode Variant",       "No",    "No",    "No",    "High"],
    ["Pricing Tables",          "N/A",   "No",    "No",    "Critical"],
    ["Testimonials Section",    "No",    "No",    "No",    "High"],
    ["Team / Instructor Section","No",   "No",    "No",    "High"],
    ["FAQ Accordion",           "No",    "No",    "No",    "High"],
    ["Video Lightbox",          "N/A",   "N/A",   "No",    "High"],
    ["Social Share Buttons",    "No",    "No",    "No",    "Medium"],
    ["Schema.org Data",         "No",    "No",    "No",    "Medium"],
]

ROADMAP = [
    ["p1","Responsive layout (320-2560px)",  "Frontend Dev", 1,3,"Critical"],
    ["p1","Contact forms + validation",       "Frontend Dev", 1,2,"Critical"],
    ["p1","GDPR cookie consent",              "Frontend Dev", 1,1,"Critical"],
    ["p1","W3C HTML validate",                "Frontend Dev", 2,3,"Critical"],
    ["p1","Fix JS errors & broken links",     "Frontend Dev", 2,3,"Critical"],
    ["p1","Documentation PDF",                "Tech Writer",  2,3,"Critical"],
    ["p2","Build 8-12 inner pages/site",      "Design+Dev",   4,6,"High"],
    ["p2","Full visual redesign",             "Designer",     4,5,"High"],
    ["p2","Scroll animations (AOS.js)",       "Frontend Dev", 5,6,"High"],
    ["p2","Dark mode variant",                "Designer",     5,6,"High"],
    ["p2","WebP images + minification",       "Frontend Dev", 6,6,"High"],
    ["p2","Retina screenshots + promo video", "Marketing",    6,6,"High"],
    ["p3","RTL + multi-language layout",      "Frontend Dev", 7,8,"Medium"],
    ["p3","Gulp/Webpack pipeline",            "Frontend Dev", 7,8,"Medium"],
    ["p3","CSS colour skin presets (3+)",     "Designer",     8,9,"Medium"],
    ["p3","Schema.org structured data",       "Frontend Dev", 9,9,"Medium"],
    ["p3","Figma design system add-on",       "Designer",     9,10,"Medium"],
    ["p3","Envato Elements listing",          "Marketing",   10,10,"Medium"],
]


# ── HTML TEMPLATE ────────────────────────────────────────────────────
def to_js_array(lst):
    """Convert a Python list to a JS array string."""
    if all(isinstance(x, (int, float)) for x in lst):
        return "[" + ",".join(str(x) for x in lst) + "]"
    return "[" + ",".join(f'"{x}"' for x in lst) + "]"

def to_js_2d(lst):
    """Convert a Python list of lists to a JS 2D array string."""
    rows = []
    for row in lst:
        items = ",".join(f'"{x}"' if isinstance(x, str) else str(x) for x in row)
        rows.append(f"[{items}]")
    return "[" + ",".join(rows) + "]"

def build_html():
    # Inject Python data into JS variables block
    data_block = f"""
const readinessCriteria = {to_js_array(READINESS_CRITERIA)};
const w1Scores  = {to_js_array(W1_SCORES)};
const w2Scores  = {to_js_array(W2_SCORES)};
const w3Scores  = {to_js_array(W3_SCORES)};
const tgtScores = {to_js_array(TGT_SCORES)};

const funnelStages = {to_js_array(FUNNEL_STAGES)};
const funnelW1  = {to_js_array(FUNNEL_W1)};
const funnelW2  = {to_js_array(FUNNEL_W2)};
const funnelW3  = {to_js_array(FUNNEL_W3)};
const funnelOpt = {to_js_array(FUNNEL_OPT)};

const salesDates = {to_js_array(SALES_DATES)};
const salesW1 = {to_js_array(SALES_W1)};
const salesW2 = {to_js_array(SALES_W2)};
const salesW3 = {to_js_array(SALES_W3)};

const trafficChannels = {to_js_array(TRAFFIC_CHANNELS)};
const trafficW1 = {to_js_array(TRAFFIC_W1)};
const trafficW2 = {to_js_array(TRAFFIC_W2)};
const trafficW3 = {to_js_array(TRAFFIC_W3)};

const revScenarios = {to_js_array(REV_SCENARIOS)};
const revW1 = {to_js_array(REV_W1)};
const revW2 = {to_js_array(REV_W2)};
const revW3 = {to_js_array(REV_W3)};

const compNames = {to_js_array(COMP_NAMES)};
const compSales = {to_js_array(COMP_SALES)};

const gaps    = {to_js_2d(GAPS)};
const roadmap = {to_js_2d(ROADMAP)};

const avgW1 = w1Scores.reduce((a,b)=>a+b,0)/w1Scores.length;
const avgW2 = w2Scores.reduce((a,b)=>a+b,0)/w2Scores.length;
const avgW3 = w3Scores.reduce((a,b)=>a+b,0)/w3Scores.length;
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ThemeForest Gap Analysis Dashboard</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
:root{{
  --navy:#1F4E78;--blue:#2E75B6;--lblue:#BDD7EE;
  --w1:#378ADD;--w2:#EF9F27;--w3:#1D9E75;
  --red:#E24B4A;--gold:#C9A44B;
  --bg:#F0F4F8;--card:#FFFFFF;--border:#E2E8F0;
  --text1:#1A2332;--text2:#64748B;--text3:#94A3B8;
  --green:#22C55E;--amber:#F59E0B;
  --pill-cr-bg:#FEE2E2;--pill-cr:#991B1B;
  --pill-mj-bg:#FEF3C7;--pill-mj:#92400E;
  --pill-mo-bg:#DCFCE7;--pill-mo:#166534;
  --pill-rd-bg:#DBEAFE;--pill-rd:#1E40AF;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--text1);font-size:13px;min-height:100vh}}
.cover{{background:linear-gradient(135deg,var(--navy) 0%,#2563EB 60%,#1D9E75 100%);padding:28px 36px 22px;position:relative;overflow:hidden}}
.cover::before{{content:'';position:absolute;top:-60px;right:-60px;width:280px;height:280px;border-radius:50%;background:rgba(255,255,255,.04)}}
.cover::after{{content:'';position:absolute;bottom:-80px;left:20%;width:200px;height:200px;border-radius:50%;background:rgba(255,255,255,.03)}}
.cover-top{{display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:12px}}
.cover-badge{{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);border-radius:20px;padding:4px 14px;font-size:11px;color:rgba(255,255,255,.85);font-weight:500;letter-spacing:.3px}}
.cover h1{{font-size:26px;font-weight:700;color:#fff;margin:14px 0 4px;letter-spacing:-.3px}}
.cover h1 span{{color:#93C5FD}}
.cover-sub{{font-size:12px;color:rgba(255,255,255,.7);margin-bottom:16px}}
.cover-meta{{display:flex;gap:20px;flex-wrap:wrap}}
.cover-meta-item{{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);border-radius:8px;padding:8px 14px}}
.cover-meta-item .lbl{{font-size:10px;color:rgba(255,255,255,.6);text-transform:uppercase;letter-spacing:.5px;margin-bottom:2px}}
.cover-meta-item .val{{font-size:13px;font-weight:600;color:#fff}}
.nav-wrap{{background:#fff;border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100;padding:0 36px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;min-height:48px}}
.tabs{{display:flex;gap:2px;overflow-x:auto;padding:6px 0}}
.tab{{font-size:12px;font-weight:500;padding:6px 14px;border:none;background:none;color:var(--text2);cursor:pointer;border-radius:6px;transition:all .15s;white-space:nowrap}}
.tab:hover{{background:var(--bg);color:var(--text1)}}
.tab.active{{background:var(--navy);color:#fff}}
.filter-wrap{{display:flex;align-items:center;gap:8px}}
.filter-wrap label{{font-size:11px;color:var(--text2);font-weight:500}}
select{{font-family:'DM Sans',sans-serif;font-size:12px;padding:5px 10px;border:1px solid var(--border);border-radius:6px;background:#fff;color:var(--text1);cursor:pointer;outline:none}}
select:focus{{border-color:var(--blue)}}
.main{{padding:20px 36px 40px}}
.page{{display:none}}.page.active{{display:block}}
.kpi-row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-bottom:18px}}
.kpi-card{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:16px 18px;position:relative;overflow:hidden}}
.kpi-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:12px 12px 0 0}}
.kpi-card.blue::before{{background:var(--w1)}}.kpi-card.amber::before{{background:var(--w2)}}
.kpi-card.green::before{{background:var(--w3)}}.kpi-card.red::before{{background:var(--red)}}
.kpi-card.navy::before{{background:var(--navy)}}.kpi-card.gold::before{{background:var(--gold)}}
.kpi-lbl{{font-size:10px;font-weight:600;color:var(--text2);text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px}}
.kpi-val{{font-size:24px;font-weight:700;color:var(--text1);line-height:1;margin-bottom:4px;font-family:'DM Mono',monospace}}
.kpi-delta{{font-size:11px;color:var(--text2)}}
.kpi-delta.up{{color:#166534}}.kpi-delta.dn{{color:#991B1B}}
.g2{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px}}
.g3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin-bottom:14px}}
.g13{{display:grid;grid-template-columns:1.15fr 1fr;gap:14px;margin-bottom:14px}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:18px}}
.card-title{{font-size:11px;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:.6px;margin-bottom:14px;display:flex;align-items:center;gap:6px}}
.card-title .dot{{width:8px;height:8px;border-radius:50%}}
.ch{{position:relative;width:100%}}
.legend{{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:10px}}
.legend span{{display:flex;align-items:center;gap:5px;font-size:11px;color:var(--text2)}}
.legend b{{width:10px;height:10px;border-radius:2px;flex-shrink:0}}
.dash-table{{width:100%;border-collapse:collapse;font-size:11px}}
.dash-table th{{text-align:left;font-weight:600;color:var(--text2);padding:6px 8px;border-bottom:1px solid var(--border);font-size:10px;text-transform:uppercase;letter-spacing:.4px}}
.dash-table td{{padding:6px 8px;border-bottom:1px solid var(--bg);color:var(--text1)}}
.dash-table tr:last-child td{{border-bottom:none}}
.dash-table tr:hover td{{background:var(--bg)}}
.pill{{display:inline-block;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:600;letter-spacing:.2px}}
.pill.cr{{background:var(--pill-cr-bg);color:var(--pill-cr)}}
.pill.mj{{background:var(--pill-mj-bg);color:var(--pill-mj)}}
.pill.mo{{background:var(--pill-mo-bg);color:var(--pill-mo)}}
.pill.rd{{background:var(--pill-rd-bg);color:var(--pill-rd)}}
.rag-cr{{color:#991B1B;font-weight:700}}.rag-mj{{color:#92400E;font-weight:600}}
.rag-mo{{color:#166534}}.rag-ok{{color:#1E40AF}}
td.no{{color:#DC2626;font-weight:600}}td.yes{{color:#16A34A;font-weight:600}}
td.partial{{color:#D97706;font-weight:600}}td.na2{{color:var(--text3)}}
.funnel-item{{margin-bottom:9px}}
.funnel-label{{display:flex;justify-content:space-between;margin-bottom:3px;font-size:11px}}
.funnel-label .name{{color:var(--text1);font-weight:500}}
.funnel-label .nums{{color:var(--text2);font-family:'DM Mono',monospace;font-size:10px}}
.funnel-bar-bg{{height:14px;background:var(--bg);border-radius:4px;overflow:hidden}}
.funnel-bar-fill{{height:100%;border-radius:4px;transition:width .5s ease}}
.gantt-row{{display:flex;align-items:center;gap:8px;margin-bottom:6px;font-size:11px}}
.gantt-task{{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--text1)}}
.gantt-owner{{width:80px;color:var(--text2);font-size:10px;text-align:right;flex-shrink:0}}
.gantt-wks{{display:flex;gap:2px;flex-shrink:0}}
.gantt-wk{{width:20px;height:16px;border-radius:3px;background:var(--bg)}}
.gantt-wk.p1{{background:#BFDBFE}}.gantt-wk.p2{{background:#FDE68A}}.gantt-wk.p3{{background:#BBF7D0}}
.phase-header{{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;padding:3px 0 2px;margin-top:6px}}
.phase-header.p1{{color:#1D4ED8}}.phase-header.p2{{color:#92400E}}.phase-header.p3{{color:#166534}}
.footer{{text-align:center;padding:16px 36px;color:var(--text3);font-size:10px;border-top:1px solid var(--border);background:#fff;margin-top:20px}}
@media(max-width:768px){{
  .cover{{padding:20px 18px 16px}}
  .main{{padding:14px 12px 30px}}
  .nav-wrap{{padding:0 12px}}
  .g2,.g3,.g13{{grid-template-columns:1fr}}
}}
</style>
</head>
<body>

<!-- ══ COVER HEADER ══ -->
<div class="cover">
  <div class="cover-top">
    <div>
      <div class="cover-badge">&#128202; Gap Analysis Dashboard</div>
      <h1>ThemeForest <span>Gap Analysis</span></h1>
      <div class="cover-sub">3 Website Templates &nbsp;&middot;&nbsp; Marketplace Readiness &nbsp;&middot;&nbsp; Conversion &amp; Revenue KPIs</div>
    </div>
  </div>
  <div class="cover-meta">
    <div class="cover-meta-item"><div class="lbl">Templates Reviewed</div><div class="val">W1 &middot; W2 &middot; W3</div></div>
    <div class="cover-meta-item"><div class="lbl">Data Source</div><div class="val">ThemeForest_Dashboard_SampleData.xlsx</div></div>
    <div class="cover-meta-item"><div class="lbl">Report Status</div><div class="val">Sample Data &mdash; Ready for Review</div></div>
  </div>
</div>

<!-- ══ NAV ══ -->
<div class="nav-wrap">
  <div class="tabs" id="tabNav"></div>
  <div class="filter-wrap">
    <label>Template:</label>
    <select id="tmplFilter" onchange="applyFilter()">
      <option value="all">All Templates</option>
      <option value="w1">W1 &ndash; Architect</option>
      <option value="w2">W2 &ndash; Business</option>
      <option value="w3">W3 &ndash; Course</option>
    </select>
  </div>
</div>

<!-- ══ PAGES ══ -->
<div class="main">
  <div id="p-overview"  class="page active"></div>
  <div id="p-funnel"    class="page"></div>
  <div id="p-sales"     class="page"></div>
  <div id="p-traffic"   class="page"></div>
  <div id="p-revenue"   class="page"></div>
  <div id="p-gaps"      class="page"></div>
  <div id="p-roadmap"   class="page"></div>
</div>

<div class="footer">
  ThemeForest Gap Analysis Dashboard &nbsp;&middot;&nbsp;
  Data: ThemeForest_Dashboard_SampleData.xlsx &nbsp;&middot;&nbsp;
  Sample data &mdash; replace with live submissions
</div>

<script>
// ── DATA (injected from Python) ───────────────────────────────────────
{data_block}

// ── CHART HELPERS ─────────────────────────────────────────────────────
const C = {{w1:'#378ADD',w2:'#EF9F27',w3:'#1D9E75',tgt:'#E24B4A',lb:'#BDD7EE',la:'#FDE68A',lg:'#BBF7D0'}};
const charts = {{}};
function dc(id){{if(charts[id]){{charts[id].destroy();delete charts[id];}}}}
function mkc(id,h){{return `<div class="ch" style="height:${{h}}px"><canvas id="${{id}}"></canvas></div>`;}}
function leg(items){{return `<div class="legend">${{items.map(([c,l])=>`<span><b style="background:${{c}}"></b>${{l}}</span>`).join('')}}</div>`;}}

let activeFilter = 'all';
function applyFilter(){{
  activeFilter = document.getElementById('tmplFilter').value;
  buildKPIs();
  const active = document.querySelector('.page.active');
  if(active){{ const id=active.id.replace('p-',''); builders[id]&&builders[id](); }}
}}

// ── KPI ROW ───────────────────────────────────────────────────────────
function buildKPIs(){{
  const row = document.getElementById('kpiRow');
  if(!row) return;
  let avg=((avgW1+avgW2+avgW3)/3).toFixed(1), conv='0.040%', gapsN=17, rev='$8,619', trafficN='10,385', units=275;
  if(activeFilter==='w1'){{avg=avgW1.toFixed(1);conv='0.030%';gapsN=16;rev='$3,019';trafficN='2,460';units=61;}}
  if(activeFilter==='w2'){{avg=avgW2.toFixed(1);conv='0.040%';gapsN=17;rev='$2,144';trafficN='3,925';units=87;}}
  if(activeFilter==='w3'){{avg=avgW3.toFixed(1);conv='0.050%';gapsN=16;rev='$3,456';trafficN='4,000';units=127;}}
  const kpis=[
    {{c:'navy', lbl:'Avg TF Readiness',    val:avg+'/10',  d:'Target 8.0+/10',        cls:'dn'}},
    {{c:'red',  lbl:'Current Conv. Rate',  val:conv,       d:'Target: 0.34%',         cls:'dn'}},
    {{c:'red',  lbl:'Critical Gaps',       val:gapsN,      d:'Must fix before submit', cls:'dn'}},
    {{c:'green',lbl:'Moderate Y1 Revenue', val:rev,        d:'62.5% author share',    cls:''}},
    {{c:'blue', lbl:'Monthly Visitors',    val:trafficN,   d:'(30 days)',             cls:'up'}},
    {{c:'amber',lbl:'Units Sold (90d)',     val:units,      d:'All templates',         cls:'up'}},
  ];
  row.innerHTML=kpis.map(k=>`<div class="kpi-card ${{k.c}}"><div class="kpi-lbl">${{k.lbl}}</div><div class="kpi-val">${{k.val}}</div><div class="kpi-delta ${{k.cls}}">${{k.d}}</div></div>`).join('');
}}

// ── RAG HELPERS ───────────────────────────────────────────────────────
function ragClass(a){{return a<=2?'rag-cr':a<=4?'rag-mj':a<=6?'rag-mo':'rag-ok';}}
function ragLabel(a){{
  if(a<=2)return '<span class="pill cr">Critical</span>';
  if(a<=4)return '<span class="pill mj">Major Gap</span>';
  if(a<=6)return '<span class="pill mo">Moderate</span>';
  return '<span class="pill rd">Ready</span>';
}}

// ══ PAGE 1 — OVERVIEW ════════════════════════════════════════════════
function buildOverview(){{
  document.getElementById('p-overview').innerHTML=`
  <div id="kpiRow" class="kpi-row"></div>
  <div class="g13">
    <div class="card">
      <div class="card-title"><span class="dot" style="background:var(--navy)"></span>Readiness scores vs target</div>
      ${{leg([[C.w1,'W1 Architect'],[C.w2,'W2 Business'],[C.w3,'W3 Course'],[C.tgt,'Target (8+)']])}}<br>
      ${{mkc('overviewBar',240)}}
    </div>
    <div class="card">
      <div class="card-title"><span class="dot" style="background:var(--red)"></span>RAG status scorecard</div>
      <div style="overflow-y:auto;max-height:265px">
        <table class="dash-table">
          <thead><tr><th>Criterion</th><th>W1</th><th>W2</th><th>W3</th><th>Status</th></tr></thead>
          <tbody id="ragBody"></tbody>
        </table>
      </div>
    </div>
  </div>
  <div class="g3">
    <div class="card"><div class="card-title"><span class="dot" style="background:var(--blue)"></span>Overall readiness vs target</div>${{mkc('readBar',180)}}</div>
    <div class="card"><div class="card-title"><span class="dot" style="background:var(--red)"></span>Zero-score gaps per template</div>${{mkc('gapDonut',180)}}</div>
    <div class="card"><div class="card-title"><span class="dot" style="background:var(--text3)"></span>Competitor lifetime sales</div>${{mkc('compBar',180)}}</div>
  </div>`;
  buildKPIs();
  setTimeout(()=>{{
    document.getElementById('ragBody').innerHTML=readinessCriteria.map((c,i)=>{{
      const avg=(w1Scores[i]+w2Scores[i]+w3Scores[i])/3;
      return `<tr><td>${{c}}</td><td class="${{ragClass(avg)}}">${{w1Scores[i]}}</td><td class="${{ragClass(avg)}}">${{w2Scores[i]}}</td><td class="${{ragClass(avg)}}">${{w3Scores[i]}}</td><td>${{ragLabel(avg)}}</td></tr>`;
    }}).join('');
    dc('overviewBar');
    charts['overviewBar']=new Chart(document.getElementById('overviewBar'),{{type:'bar',data:{{labels:readinessCriteria.map(c=>c.length>16?c.slice(0,15)+'\u2026':c),datasets:[{{label:'W1',data:w1Scores,backgroundColor:C.w1+'BB'}},{{label:'W2',data:w2Scores,backgroundColor:C.w2+'BB'}},{{label:'W3',data:w3Scores,backgroundColor:C.w3+'BB'}},{{label:'Target',data:tgtScores,backgroundColor:'transparent',borderColor:C.tgt,borderWidth:2,type:'line',pointRadius:3,pointBackgroundColor:C.tgt}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{font:{{size:9}},maxRotation:45}}}},y:{{min:0,max:10,ticks:{{font:{{size:9}},stepSize:2}}}}}}}}}});
    dc('readBar');
    charts['readBar']=new Chart(document.getElementById('readBar'),{{type:'bar',data:{{labels:['W1 Architect','W2 Business','W3 Course'],datasets:[{{label:'Score',data:[parseFloat(avgW1.toFixed(1)),parseFloat(avgW2.toFixed(1)),parseFloat(avgW3.toFixed(1))],backgroundColor:[C.w1,C.w2,C.w3],borderRadius:4}},{{label:'Target',data:[8,8,8],backgroundColor:'rgba(226,75,74,.12)',borderColor:C.tgt,borderWidth:1.5}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{y:{{min:0,max:10,ticks:{{font:{{size:9}}}}}},x:{{ticks:{{font:{{size:9}}}}}}}}}}}});
    dc('gapDonut');
    charts['gapDonut']=new Chart(document.getElementById('gapDonut'),{{type:'doughnut',data:{{labels:['W1','W2','W3'],datasets:[{{data:[w1Scores.filter(x=>x===0).length,w2Scores.filter(x=>x===0).length,w3Scores.filter(x=>x===0).length],backgroundColor:[C.w1,C.w2,C.w3],borderWidth:0}}]}},options:{{responsive:true,maintainAspectRatio:false,cutout:'65%',plugins:{{legend:{{position:'bottom',labels:{{font:{{size:9}},boxWidth:10}}}}}}}}}});
    dc('compBar');
    charts['compBar']=new Chart(document.getElementById('compBar'),{{type:'bar',data:{{labels:compNames,datasets:[{{label:'Sales',data:compSales,backgroundColor:C.lb,borderRadius:3}}]}},options:{{responsive:true,maintainAspectRatio:false,indexAxis:'y',plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{font:{{size:9}}}}}},y:{{ticks:{{font:{{size:9}}}}}}}}}}}});
  }},60);
}}

// ══ PAGE 2 — FUNNEL ══════════════════════════════════════════════════
function buildFunnel(){{
  const bars=funnelStages.map((s,i)=>{{
    const avg=Math.round((funnelW1[i]+funnelW2[i]+funnelW3[i])/3);
    const pct=Math.min(100,Math.round(avg/(funnelOpt[i]||1)*100));
    return `<div class="funnel-item"><div class="funnel-label"><span class="name">${{s}}</span><span class="nums">Avg:${{avg.toLocaleString()}} / Opt:${{funnelOpt[i].toLocaleString()}}</span></div><div class="funnel-bar-bg"><div class="funnel-bar-fill" style="width:${{pct}}%;background:${{C.w1}}"></div></div></div>`;
  }}).join('');
  document.getElementById('p-funnel').innerHTML=`
  <div id="kpiRow" class="kpi-row"></div>
  <div class="g2">
    <div class="card"><div class="card-title"><span class="dot" style="background:var(--blue)"></span>Funnel: current vs optimised</div>${{leg([[C.w1,'W1'],[C.w2,'W2'],[C.w3,'W3'],[C.tgt,'Optimised']])}}<br>${{mkc('funnelChart',280)}}</div>
    <div class="card"><div class="card-title"><span class="dot" style="background:var(--w3)"></span>Stage waterfall</div>${{bars}}<div style="margin-top:10px;font-size:11px;color:var(--text2)">Conv. rate: <b style="color:var(--red)">0.04%</b> &rarr; <b style="color:var(--w3)">0.34%</b> = <b>8.5&times; uplift</b></div></div>
  </div>
  <div class="card" style="margin-bottom:14px"><div class="card-title"><span class="dot" style="background:var(--amber)"></span>Uplift multiplier per stage</div>${{mkc('upliftBar',150)}}</div>`;
  buildKPIs();
  setTimeout(()=>{{
    dc('funnelChart');
    charts['funnelChart']=new Chart(document.getElementById('funnelChart'),{{type:'bar',data:{{labels:funnelStages.map(s=>s.length>18?s.slice(0,17)+'\u2026':s),datasets:[{{label:'W1',data:funnelW1,backgroundColor:C.w1+'CC'}},{{label:'W2',data:funnelW2,backgroundColor:C.w2+'CC'}},{{label:'W3',data:funnelW3,backgroundColor:C.w3+'CC'}},{{label:'Optimised',data:funnelOpt,backgroundColor:'rgba(226,75,74,.15)',borderColor:C.tgt,borderWidth:1.5}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{font:{{size:8}},maxRotation:40,autoSkip:false}}}},y:{{ticks:{{font:{{size:9}}}}}}}}}}}});
    dc('upliftBar');
    const up=funnelStages.slice(1).map((_,i)=>{{const j=i+1,avg=(funnelW1[j]+funnelW2[j]+funnelW3[j])/3;return avg===0?null:parseFloat((funnelOpt[j]/avg).toFixed(1));}});
    charts['upliftBar']=new Chart(document.getElementById('upliftBar'),{{type:'bar',data:{{labels:funnelStages.slice(1).map(s=>s.length>18?s.slice(0,17)+'\u2026':s),datasets:[{{label:'Uplift',data:up,backgroundColor:up.map(v=>v===null?'#ccc':v>50?C.tgt:v>10?C.w2:C.w3),borderRadius:4}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{font:{{size:8}},maxRotation:40,autoSkip:false}}}},y:{{title:{{display:true,text:'x uplift',font:{{size:9}}}},ticks:{{font:{{size:9}}}}}}}}}}}});
  }},60);
}}

// ══ PAGE 3 — SALES ═══════════════════════════════════════════════════
function buildSales(){{
  document.getElementById('p-sales').innerHTML=`
  <div id="kpiRow" class="kpi-row"></div>
  <div class="card" style="margin-bottom:14px"><div class="card-title"><span class="dot" style="background:var(--blue)"></span>Weekly units sold — 90-day rolling trend</div>${{leg([[C.w1,'W1 Architect ($69)'],[C.w2,'W2 Business ($49)'],[C.w3,'W3 Course ($79)']])}}<br>${{mkc('salesLine',230)}}</div>
  <div class="g3">
    <div class="card"><div class="card-title"><span class="dot" style="background:var(--w3)"></span>Revenue mix (90d)</div>${{mkc('revDonut',185)}}</div>
    <div class="card"><div class="card-title"><span class="dot" style="background:var(--blue)"></span>Units by template (90d)</div>${{mkc('unitBar',185)}}</div>
    <div class="card"><div class="card-title"><span class="dot" style="background:var(--amber)"></span>Cumulative revenue (90d)</div>${{mkc('revArea',185)}}</div>
  </div>`;
  buildKPIs();
  setTimeout(()=>{{
    dc('salesLine');
    charts['salesLine']=new Chart(document.getElementById('salesLine'),{{type:'line',data:{{labels:salesDates,datasets:[{{label:'W1',data:salesW1,borderColor:C.w1,backgroundColor:C.w1+'18',fill:true,tension:.35,pointRadius:3,borderWidth:2}},{{label:'W2',data:salesW2,borderColor:C.w2,backgroundColor:C.w2+'18',fill:true,tension:.35,pointRadius:3,borderWidth:2,borderDash:[5,2]}},{{label:'W3',data:salesW3,borderColor:C.w3,backgroundColor:C.w3+'18',fill:true,tension:.35,pointRadius:3,borderWidth:2,borderDash:[2,2]}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{font:{{size:9}},maxRotation:30}}}},y:{{ticks:{{font:{{size:9}}}}}}}}}}}});
    dc('revDonut');
    charts['revDonut']=new Chart(document.getElementById('revDonut'),{{type:'doughnut',data:{{labels:['W1 $2,631','W2 $2,664','W3 $6,271'],datasets:[{{data:[2631,2664,6271],backgroundColor:[C.w1,C.w2,C.w3],borderWidth:0}}]}},options:{{responsive:true,maintainAspectRatio:false,cutout:'60%',plugins:{{legend:{{position:'bottom',labels:{{font:{{size:9}},boxWidth:10}}}}}}}}}});
    dc('unitBar');
    charts['unitBar']=new Chart(document.getElementById('unitBar'),{{type:'bar',data:{{labels:['W1','W2','W3'],datasets:[{{label:'Units',data:[61,87,127],backgroundColor:[C.w1,C.w2,C.w3],borderRadius:4}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{font:{{size:9}}}}}},y:{{ticks:{{font:{{size:9}}}}}}}}}}}});
    dc('revArea');
    const cumW1=salesW1.map((v,i)=>salesW1.slice(0,i+1).reduce((a,b)=>a+b,0)*69*0.625);
    const cumW2=salesW2.map((v,i)=>salesW2.slice(0,i+1).reduce((a,b)=>a+b,0)*49*0.625);
    const cumW3=salesW3.map((v,i)=>salesW3.slice(0,i+1).reduce((a,b)=>a+b,0)*79*0.625);
    charts['revArea']=new Chart(document.getElementById('revArea'),{{type:'line',data:{{labels:salesDates,datasets:[{{label:'W1',data:cumW1,borderColor:C.w1,backgroundColor:C.w1+'22',fill:true,tension:.3,pointRadius:0,borderWidth:1.5}},{{label:'W2',data:cumW2,borderColor:C.w2,backgroundColor:C.w2+'22',fill:true,tension:.3,pointRadius:0,borderWidth:1.5}},{{label:'W3',data:cumW3,borderColor:C.w3,backgroundColor:C.w3+'22',fill:true,tension:.3,pointRadius:0,borderWidth:1.5}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{font:{{size:8}},maxRotation:30}}}},y:{{ticks:{{font:{{size:9}},callback:v=>'$'+Math.round(v/1000)+'k'}}}}}}}}}});
  }},60);
}}

// ══ PAGE 4 — TRAFFIC ═════════════════════════════════════════════════
function buildTraffic(){{
  const totals=trafficChannels.map((_,i)=>trafficW1[i]+trafficW2[i]+trafficW3[i]);
  document.getElementById('p-traffic').innerHTML=`
  <div id="kpiRow" class="kpi-row"></div>
  <div class="g2">
    <div class="card"><div class="card-title"><span class="dot" style="background:var(--blue)"></span>Visitors by channel — stacked (30d)</div>${{leg([[C.w1,'W1'],[C.w2,'W2'],[C.w3,'W3']])}}<br>${{mkc('trafficStacked',320)}}</div>
    <div class="card"><div class="card-title"><span class="dot" style="background:var(--w3)"></span>Channel share — combined</div>${{mkc('trafficPie',200)}}
      <div style="overflow-y:auto;max-height:140px;margin-top:8px">
        <table class="dash-table"><thead><tr><th>Channel</th><th>W1</th><th>W2</th><th>W3</th><th>Total</th></tr></thead>
        <tbody>${{trafficChannels.map((ch,i)=>`<tr><td>${{ch}}</td><td>${{trafficW1[i].toLocaleString()}}</td><td>${{trafficW2[i].toLocaleString()}}</td><td>${{trafficW3[i].toLocaleString()}}</td><td><b>${{totals[i].toLocaleString()}}</b></td></tr>`).join('')}}</tbody></table>
      </div>
    </div>
  </div>`;
  buildKPIs();
  setTimeout(()=>{{
    dc('trafficStacked');
    charts['trafficStacked']=new Chart(document.getElementById('trafficStacked'),{{type:'bar',data:{{labels:trafficChannels,datasets:[{{label:'W1',data:trafficW1,backgroundColor:C.w1+'CC'}},{{label:'W2',data:trafficW2,backgroundColor:C.w2+'CC'}},{{label:'W3',data:trafficW3,backgroundColor:C.w3+'CC'}}]}},options:{{responsive:true,maintainAspectRatio:false,indexAxis:'y',plugins:{{legend:{{display:false}}}},scales:{{x:{{stacked:true,ticks:{{font:{{size:9}}}}}},y:{{stacked:true,ticks:{{font:{{size:9}}}}}}}}}}}});
    dc('trafficPie');
    charts['trafficPie']=new Chart(document.getElementById('trafficPie'),{{type:'pie',data:{{labels:trafficChannels,datasets:[{{data:totals,backgroundColor:['#378ADD','#EF9F27','#1D9E75','#BDD7EE','#FAC775','#A7F3D0','#FCA5A5','#C4B5FD'],borderWidth:0}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{position:'right',labels:{{font:{{size:9}},boxWidth:10,padding:6}}}}}}}}}});
  }},60);
}}

// ══ PAGE 5 — REVENUE ═════════════════════════════════════════════════
function buildRevenue(){{
  const portTotals=revScenarios.map((_,i)=>revW1[i]+revW2[i]+revW3[i]);
  document.getElementById('p-revenue').innerHTML=`
  <div id="kpiRow" class="kpi-row"></div>
  <div class="g2">
    <div class="card"><div class="card-title"><span class="dot" style="background:var(--blue)"></span>Year-1 revenue by scenario ($)</div>${{leg([[C.w1,'W1'],[C.w2,'W2'],[C.w3,'W3']])}}<br>${{mkc('revScenBar',250)}}</div>
    <div class="card"><div class="card-title"><span class="dot" style="background:var(--w3)"></span>Portfolio total</div>${{mkc('portBar',140)}}
      <table class="dash-table" style="margin-top:10px">
        <thead><tr><th>Scenario</th><th>W1</th><th>W2</th><th>W3</th><th>Total</th></tr></thead>
        <tbody>${{revScenarios.map((s,i)=>`<tr><td><b>${{s}}</b></td><td>$${{revW1[i].toLocaleString()}}</td><td>$${{revW2[i].toLocaleString()}}</td><td>$${{revW3[i].toLocaleString()}}</td><td><b>$${{portTotals[i].toLocaleString()}}</b></td></tr>`).join('')}}</tbody>
      </table>
      <div style="font-size:10px;color:var(--text2);margin-top:8px">Prices: W1 $69 &middot; W2 $49 &middot; W3 $79 &middot; Author share 62.5%</div>
    </div>
  </div>
  <div class="card" style="margin-bottom:14px"><div class="card-title"><span class="dot" style="background:var(--text3)"></span>Competitor lifetime sales benchmark</div>${{mkc('compBar2',160)}}</div>`;
  buildKPIs();
  setTimeout(()=>{{
    dc('revScenBar');
    charts['revScenBar']=new Chart(document.getElementById('revScenBar'),{{type:'bar',data:{{labels:revScenarios,datasets:[{{label:'W1',data:revW1,backgroundColor:'#4FA6E8',borderRadius:3}},{{label:'W2',data:revW2,backgroundColor:C.w2,borderRadius:3}},{{label:'W3',data:revW3,backgroundColor:C.w3,borderRadius:3}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{font:{{size:10}}}}}},y:{{ticks:{{font:{{size:9}},callback:v=>'$'+v.toLocaleString()}}}}}}}}}});
    dc('portBar');
    charts['portBar']=new Chart(document.getElementById('portBar'),{{type:'bar',data:{{labels:revScenarios,datasets:[{{label:'Portfolio',data:portTotals,backgroundColor:[C.lb,'#9FE1CB','#85B7EB'],borderRadius:4}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{font:{{size:9}}}}}},y:{{ticks:{{font:{{size:9}},callback:v=>'$'+v.toLocaleString()}}}}}}}}}});
    dc('compBar2');
    charts['compBar2']=new Chart(document.getElementById('compBar2'),{{type:'bar',data:{{labels:compNames,datasets:[{{label:'Sales',data:compSales,backgroundColor:'#CBD5E1',borderRadius:3}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{font:{{size:9}}}}}},y:{{ticks:{{font:{{size:9}}}}}}}}}}}});
  }},60);
}}

// ══ PAGE 6 — GAPS ════════════════════════════════════════════════════
function buildGaps(){{
  const sc=v=>v==='No'?'no':v==='Yes'?'yes':v==='Partial'?'partial':'na2';
  const pc=p=>p==='Critical'?'cr':p==='High'?'mj':'mo';
  document.getElementById('p-gaps').innerHTML=`
  <div id="kpiRow" class="kpi-row"></div>
  <div class="g2" style="margin-bottom:14px">
    <div class="card"><div class="card-title"><span class="dot" style="background:var(--red)"></span>Gap count by template</div>${{mkc('gapStackBar',200)}}</div>
    <div class="card"><div class="card-title"><span class="dot" style="background:var(--amber)"></span>Priority breakdown</div>${{mkc('priDonut',200)}}</div>
  </div>
  <div class="card">
    <div class="card-title"><span class="dot" style="background:var(--navy)"></span>Feature presence matrix — 20 requirements</div>
    <div style="overflow-x:auto">
      <table class="dash-table">
        <thead><tr><th>Feature</th><th>W1 Architect</th><th>W2 Business</th><th>W3 Course</th><th>Priority</th></tr></thead>
        <tbody>${{gaps.map(g=>`<tr><td>${{g[0]}}</td><td class="${{sc(g[1])}}">${{g[1]}}</td><td class="${{sc(g[2])}}">${{g[2]}}</td><td class="${{sc(g[3])}}">${{g[3]}}</td><td><span class="pill ${{pc(g[4])}}">${{g[4]}}</span></td></tr>`).join('')}}</tbody>
      </table>
    </div>
  </div>`;
  buildKPIs();
  setTimeout(()=>{{
    dc('gapStackBar');
    charts['gapStackBar']=new Chart(document.getElementById('gapStackBar'),{{type:'bar',data:{{labels:['W1 Architect','W2 Business','W3 Course'],datasets:[{{label:'No',data:[16,17,16],backgroundColor:'#FCA5A5'}},{{label:'Partial',data:[2,2,3],backgroundColor:'#FDE68A'}},{{label:'N/A',data:[2,1,1],backgroundColor:'#E2E8F0'}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{position:'bottom',labels:{{font:{{size:9}},boxWidth:10}}}}}},scales:{{x:{{stacked:true,ticks:{{font:{{size:9}}}}}},y:{{stacked:true,ticks:{{font:{{size:9}}}}}}}}}}}});
    dc('priDonut');
    charts['priDonut']=new Chart(document.getElementById('priDonut'),{{type:'doughnut',data:{{labels:['Critical (9)','High (8)','Medium (3)'],datasets:[{{data:[9,8,3],backgroundColor:['#FCA5A5','#FDE68A','#BBF7D0'],borderWidth:0}}]}},options:{{responsive:true,maintainAspectRatio:false,cutout:'60%',plugins:{{legend:{{position:'bottom',labels:{{font:{{size:9}},boxWidth:10}}}}}}}}}});
  }},60);
}}

// ══ PAGE 7 — ROADMAP ═════════════════════════════════════════════════
function buildRoadmap(){{
  const phNames={{p1:'Phase 1 — Critical Fixes (Wk 1-3)',p2:'Phase 2 — High Priority (Wk 4-6)',p3:'Phase 3 — Competitive Edge (Wk 7-10)'}};
  let lastP='';
  const rows=roadmap.map(t=>{{
    let ph='';if(t[0]!==lastP){{lastP=t[0];ph=`<div class="phase-header ${{t[0]}}">${{phNames[t[0]]}}</div>`;}}
    const wks=Array.from({{length:10}},(_,i)=>{{const w=i+1,on=w>=t[3]&&w<=t[4];return `<div class="gantt-wk${{on?' '+t[0]:''}}"></div>`;}}).join('');
    return `${{ph}}<div class="gantt-row"><div class="gantt-task">${{t[1]}}</div><div class="gantt-owner">${{t[2]}}</div><div class="gantt-wks">${{wks}}</div><div style="min-width:60px;text-align:right"><span class="pill ${{t[5]==='Critical'?'cr':t[5]==='High'?'mj':'mo'}}">${{t[5]}}</span></div></div>`;
  }}).join('');
  document.getElementById('p-roadmap').innerHTML=`
  <div id="kpiRow" class="kpi-row"></div>
  <div class="g3" style="margin-bottom:14px">
    <div class="card"><div class="card-title"><span class="dot" style="background:var(--blue)"></span>Tasks by phase</div>${{mkc('phaseDonut',170)}}</div>
    <div class="card"><div class="card-title"><span class="dot" style="background:var(--w2)"></span>Tasks by owner</div>${{mkc('ownerBar',170)}}</div>
    <div class="card"><div class="card-title"><span class="dot" style="background:var(--w3)"></span>Priority split</div>${{mkc('priBar2',170)}}</div>
  </div>
  <div class="card">
    <div class="card-title"><span class="dot" style="background:var(--navy)"></span>10-week Gantt — all 18 tasks
      <span style="margin-left:auto;font-size:10px;font-weight:400;color:var(--text2)">
        <span style="display:inline-block;width:10px;height:10px;background:#BFDBFE;border-radius:2px;margin-right:3px"></span>Phase 1
        <span style="display:inline-block;width:10px;height:10px;background:#FDE68A;border-radius:2px;margin:0 3px 0 8px"></span>Phase 2
        <span style="display:inline-block;width:10px;height:10px;background:#BBF7D0;border-radius:2px;margin:0 3px 0 8px"></span>Phase 3
      </span>
    </div>
    ${{rows}}
  </div>`;
  buildKPIs();
  setTimeout(()=>{{
    dc('phaseDonut');
    charts['phaseDonut']=new Chart(document.getElementById('phaseDonut'),{{type:'doughnut',data:{{labels:['Phase 1','Phase 2','Phase 3'],datasets:[{{data:[6,6,6],backgroundColor:['#BFDBFE','#FDE68A','#BBF7D0'],borderWidth:0}}]}},options:{{responsive:true,maintainAspectRatio:false,cutout:'55%',plugins:{{legend:{{position:'bottom',labels:{{font:{{size:9}},boxWidth:10}}}}}}}}}});
    dc('ownerBar');
    charts['ownerBar']=new Chart(document.getElementById('ownerBar'),{{type:'bar',data:{{labels:['Frontend Dev','Designer','Design+Dev','Tech Writer','Marketing'],datasets:[{{label:'Tasks',data:[10,4,1,1,2],backgroundColor:C.w1,borderRadius:3}}]}},options:{{responsive:true,maintainAspectRatio:false,indexAxis:'y',plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{font:{{size:9}}}}}},y:{{ticks:{{font:{{size:9}}}}}}}}}}}});
    dc('priBar2');
    charts['priBar2']=new Chart(document.getElementById('priBar2'),{{type:'bar',data:{{labels:['Critical','High','Medium'],datasets:[{{label:'Tasks',data:[6,9,3],backgroundColor:['#FCA5A5','#FDE68A','#BBF7D0'],borderRadius:4}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{font:{{size:9}}}}}},y:{{ticks:{{font:{{size:9}},stepSize:2}}}}}}}}}});
  }},60);
}}

// ── TABS & INIT ───────────────────────────────────────────────────────
const TABS=[
  {{id:'overview', label:'&#128202; Overview'}},
  {{id:'funnel',   label:'&#9661; Conversion'}},
  {{id:'sales',    label:'&#128200; Sales Trend'}},
  {{id:'traffic',  label:'&#127760; Traffic'}},
  {{id:'revenue',  label:'&#128176; Revenue'}},
  {{id:'gaps',     label:'&#9888;&#65039; Gap Matrix'}},
  {{id:'roadmap',  label:'&#128467; Roadmap'}},
];
const builders={{overview:buildOverview,funnel:buildFunnel,sales:buildSales,traffic:buildTraffic,revenue:buildRevenue,gaps:buildGaps,roadmap:buildRoadmap}};
document.getElementById('tabNav').innerHTML=TABS.map((t,i)=>`<button class="tab${{i===0?' active':''}}" onclick="switchTab('${{t.id}}')">${{t.label}}</button>`).join('');
function switchTab(id){{
  document.querySelectorAll('.tab').forEach((t,i)=>t.classList.toggle('active',TABS[i].id===id));
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.getElementById('p-'+id).classList.add('active');
  builders[id]&&builders[id]();
}}
buildOverview();
</script>
</body>
</html>"""
    return html


# ── HTTP REQUEST HANDLER ─────────────────────────────────────────────
class DashboardHandler(BaseHTTPRequestHandler):
    """Serves the dashboard HTML for every GET request."""

    html_content = b""  # filled in before server starts

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(self.html_content)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(self.html_content)

    def log_message(self, fmt, *args):
        # Clean up server log output
        print(f"  [{self.address_string()}]  {fmt % args}")


def get_local_ip():
    """Best-effort: returns the machine's LAN IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


# ── MAIN ─────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="ThemeForest Dashboard Web Server")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT,
                        help=f"Port to listen on (default: {DEFAULT_PORT})")
    parser.add_argument("--host", type=str, default="0.0.0.0",
                        help="Host to bind to (default: 0.0.0.0 = all interfaces)")
    args = parser.parse_args()

    # 1. Build the HTML
    print("Building dashboard HTML...")
    html_content = build_html()
    DashboardHandler.html_content = html_content.encode("utf-8")

    # 2. Also save a copy to disk (optional but handy)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    print(f"HTML saved to disk: {OUTPUT_FILE}  ({size_kb:.1f} KB)")

    # 3. Start the HTTP server
    server = HTTPServer((args.host, args.port), DashboardHandler)
    local_ip = get_local_ip()

    print()
    print("=" * 52)
    print("  ThemeForest Dashboard Server is RUNNING")
    print("=" * 52)
    print(f"  Local:    http://localhost:{args.port}")
    print(f"  Network:  http://{local_ip}:{args.port}")
    print(f"  All IPs:  http://0.0.0.0:{args.port}")
    print()
    print("  Share the Network URL with anyone on your network.")
    print("  For public access, use your server's public IP.")
    print()
    print("  Press Ctrl + C to stop the server.")
    print("=" * 52)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Server stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
