# ThemeForest Gap Analysis Dashboard

An interactive, browser-based dashboard built entirely in Python — no frameworks, no npm, no installs.  
Run one command and share the live URL with your team.

---

## 📁 Project Structure

```
themeforest-dashboard/
│
├── dashboard_server.py        ← Main script — builds HTML + runs web server
├── generate_dashboard.py      ← Offline version — saves HTML file only (no server)
├── ThemeForest_Dashboard.html ← Auto-generated output (do not edit manually)
├── requirements.txt           ← Dependency list (standard library only)
└── README.md                  ← This file
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/themeforest-dashboard.git
cd themeforest-dashboard
```

### 2. Run the server

```bash
python dashboard_server.py
```

### 3. Open in browser

```
http://localhost:8080
```

Share with your team using your machine's IP:

```
http://192.168.1.10:8080       ← Local network
http://123.45.67.89:8080       ← Public server IP
```

---

## ⚙️ Requirements

| Requirement | Version |
|-------------|---------|
| Python      | >= 3.7  |
| pip packages | **None** — standard library only |

No `pip install` needed. Everything used (`http.server`, `socket`, `argparse`, `os`) is built into Python.

---

## 🖥️ Server Options

```bash
# Default — port 8080, all network interfaces
python dashboard_server.py

# Custom port
python dashboard_server.py --port 5000

# Bind to localhost only (private, not accessible from network)
python dashboard_server.py --host 127.0.0.1 --port 8080

# Port 80 — standard HTTP (requires sudo on Linux/Mac)
sudo python dashboard_server.py --port 80

# View all options
python dashboard_server.py --help
```

---

## 📊 Dashboard Pages

| Tab | Description | Charts |
|-----|-------------|--------|
| 📊 Overview | TF readiness scores vs target | Grouped bar, RAG scorecard, donut, competitor bar |
| 🔽 Conversion | 7-stage marketplace funnel | Funnel chart, stage waterfall, uplift multiplier |
| 📈 Sales Trend | 90-day rolling units & revenue | Line chart, area chart, donut, bar |
| 🌐 Traffic | Visitors by channel (30 days) | Stacked bar, pie chart, table |
| 💰 Revenue | Y1 projections by scenario | Clustered column, portfolio bar, competitor bench |
| ⚠️ Gap Matrix | Feature presence (Yes/No/Partial) | Stacked bar, priority donut, heatmap table |
| 🗓 Roadmap | 10-week task tracker | Gantt bar, phase donut, owner bar |

**Template filter** (top right) — switches all KPI cards and charts between All / W1 Architect / W2 Business / W3 Course.

---

## 📂 Data Source

All data is sourced from:

```
ThemeForest_Dashboard_SampleData.xlsx
```

The Excel file contains 8 sheets:

| Sheet | Contents |
|-------|----------|
| `Readiness_Scores` | 13 criteria scored /10 per template vs target |
| `Conversion_Funnel` | 7-stage funnel — current vs optimised |
| `Sales_Trend` | 90 days of daily units & revenue |
| `Traffic_Sources` | Visitors by channel (30 days) |
| `Gap_Matrix` | Feature presence matrix (Yes / No / Partial) |
| `Revenue_Projection` | Conservative / Moderate / Optimistic Y1 scenarios |
| `Competitor_Bench` | USA competitor lifetime sales benchmark |
| `Action_Roadmap` | 10-week task tracker with owners & priority |

> ⚠️ **Note:** All figures are **sample data** created for the dashboard build.  
> Replace with live team submissions once the gap analysis is consolidated.

---

## ✏️ How to Update the Data

All data lives at the top of `dashboard_server.py` as plain Python lists.  
No HTML or JavaScript knowledge needed — just edit the lists and restart the server.

**Example — update readiness scores:**

```python
# dashboard_server.py  ←  lines ~25–40

W1_SCORES  = [3, 3, 4, 0, 1, 5, 4, 4, 5, 2, 0, 0, 0]   # ← edit these
W2_SCORES  = [4, 4, 4, 0, 1, 5, 5, 4, 5, 3, 0, 0, 0]
W3_SCORES  = [5, 4, 5, 2, 2, 6, 5, 5, 5, 3, 0, 0, 0]
TGT_SCORES = [8, 8, 8, 7,10, 9, 8, 8, 8, 8, 8, 8, 8]
```

Then restart:

```bash
python dashboard_server.py
```

The dashboard regenerates automatically every time the server starts.

---

## 🌐 Deploying to a Cloud Server (Public URL)

### AWS EC2 / DigitalOcean / Azure / Any VPS

```bash
# 1. SSH into your server
ssh user@YOUR_SERVER_IP

# 2. Clone the repo
git clone https://github.com/YOUR_USERNAME/themeforest-dashboard.git
cd themeforest-dashboard

# 3. Run the server in the background
nohup python dashboard_server.py --port 8080 &

# 4. Open firewall port 8080 (AWS: Security Groups → Inbound → TCP 8080)

# 5. Share the URL
# http://YOUR_SERVER_IP:8080
```

### Run persistently with systemd (Linux)

Create `/etc/systemd/system/dashboard.service`:

```ini
[Unit]
Description=ThemeForest Gap Analysis Dashboard
After=network.target

[Service]
WorkingDirectory=/path/to/themeforest-dashboard
ExecStart=/usr/bin/python3 dashboard_server.py --port 8080
Restart=always
User=ubuntu

[Install]
WantedBy=multi-user.target
```

Then enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable dashboard
sudo systemctl start dashboard
sudo systemctl status dashboard
```

---

## 🛑 Stopping the Server

```bash
# If running in foreground:
Ctrl + C

# If running in background (nohup):
pkill -f dashboard_server.py

# If running as systemd service:
sudo systemctl stop dashboard
```

---

## 🔒 Security Note

This server has **no authentication**. Anyone with the URL can view the dashboard.  
For internal use behind a VPN or firewall this is fine.  
For public-facing production use, add a reverse proxy (nginx) with basic auth or HTTPS.

---

## 📋 Suggested `.gitignore`

```
# Auto-generated output — don't commit
ThemeForest_Dashboard.html

# Python cache
__pycache__/
*.pyc
*.pyo
.DS_Store

# Environment
.env
venv/
```

---

## 📬 Project Info

| Field | Value |
|-------|-------|
| Prepared for | Dan Rodney |
| Report | ThemeForest Gap Analysis |
| Templates | W1 – Architect · W2 – Business · W3 – Course |
| Data | Sample — replace with live submissions |
| Target | 08/05/2026 |

---

## 📄 License

Internal use only. Not for public distribution.
