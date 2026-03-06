# BRIEFING.md — Stock Technical Analysis Dashboard

## Purpose
This document orients any AI agent instance working on this project. Read it in full before any task.

---

## What this project is
Streamlit application that fetches real historical stock data and displays an interactive technical analysis dashboard. The app calculates moving averages, Fibonacci retracement levels and support/resistance zones using pandas. An optional AI-generated text summary is produced via Hugging Face Inference API. This is a portfolio project: it demonstrates data engineering, financial visualization and AI integration in Python.

**This tool is descriptive, not predictive. It does not forecast prices. This disclaimer must always be visible in the UI.**

---

## How Antigravity works in this project

- **`.antigravity/rules.md`** loads automatically every session. Contains global rules that always apply.
- **`.agent/skills/backend/skill.md`** is the only active role. This project has no frontend role (Streamlit handles UI in Python).
- **`PROJECT.md`** is the source of truth. Contains all technical decisions, stack and structure.
- **`code-patterns/`** reference patterns from the project library when relevant. Check `python/data/yfinance-fetch` and `python/api/groq-call` structure as reference for external API calls.

---

## Folder structure
```
stock-dashboard/
├── PROJECT.md                        ← Source of truth. Always read first.
├── BRIEFING.md                       ← This document.
├── .antigravity/
│   └── rules.md                      ← Global rules (auto-loaded)
├── .agent/
│   └── skills/
│       └── backend/
│           └── skill.md              ← Only active role: Python/Streamlit/data
├── app.py                            ← Streamlit entry point
├── analysis/
│   ├── __init__.py
│   ├── indicators.py                 ← MA, Fibonacci, support/resistance
│   └── summary.py                    ← Hugging Face Inference API call
├── data/
│   ├── __init__.py
│   ├── fetcher.py                    ← yfinance data fetching
│   └── example/
│       └── AAPL_example.csv          ← Preloaded demo data
├── .streamlit/
│   └── secrets.toml                  ← HF_API_KEY (do not push to GitHub)
├── requirements.txt
└── .gitignore
```

---

## Active roles in this project

| Role | Skill | Responsibility |
|---|---|---|
| Backend | `.agent/skills/backend/skill.md` | All Python: Streamlit UI, data fetching, indicators, HF API |

No frontend role. No DB role. Streamlit renders UI directly from Python.

---

## Mandatory reading order at session start

1. This document (BRIEFING.md)
2. PROJECT.md
3. .antigravity/rules.md
4. .agent/skills/backend/skill.md

Do not write code until all four steps are complete.

---

## Key technical constraints

- All indicators calculated with pandas only. No ta, ta-lib or similar libraries.
- yfinance data: daily OHLCV, up to 1 year. Not real-time.
- HF API call is optional: if HF_API_KEY is absent from secrets, app skips summary silently.
- Demo button: preloads AAPL_example.csv from data/example/. Does not call yfinance.
- Fibonacci levels: calculated from visible range min/max, not hardcoded.
- Support/resistance: rolling window local minima/maxima on Close price.

---

## Conventions
| Concept | Value |
|---|---|
| Code language | English |
| Comments language | Spanish |
| API key | st.secrets["HF_API_KEY"] — never hardcoded |
| Commit format | Conventional: feat:, fix:, docs:, refactor:, chore: |
| Type hints | Required on all functions |
| Priority | Quality over speed. Portfolio project. |

---

## What this project demonstrates to the client

| Capability | Evidence |
|---|---|
| Python data engineering | pandas, yfinance, OHLCV processing |
| Financial data visualization | Plotly interactive charts with overlaid indicators |
| Technical analysis knowledge | MA, Fibonacci, support/resistance implemented from scratch |
| AI integration | Hugging Face Inference API for text summary |
| Streamlit deployment | Live app on Streamlit Community Cloud |
| Clean architecture | Separation of data fetching, analysis and UI layers |
