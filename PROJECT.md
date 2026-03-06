# PROJECT.md — Stock Technical Analysis Dashboard

## Status
Phase: **Planning → Development**

## Functional description
Streamlit web application that fetches real historical stock data via yfinance and renders an interactive technical analysis dashboard. Includes moving averages, Fibonacci retracement levels, support/resistance zones and volume analysis. An optional AI-generated text summary of the analysis is produced via Hugging Face Inference API. A demo button preloads AAPL data so the app works without user input.

## Important disclaimer
This tool performs descriptive technical analysis only. It does not predict prices or future market behaviour. It does not constitute financial advice. This disclaimer must be visible in the UI at all times.

## System type
Data visualization + descriptive technical analysis. External data source (yfinance). Optional LLM text summary (Hugging Face). No database. No authentication.

## Stack
| Layer | Technology |
|---|---|
| App framework | Streamlit |
| Data fetching | yfinance |
| Data processing | pandas |
| Charts | Plotly (plotly.express + plotly.graph_objects) |
| AI summary | Hugging Face Inference API |
| Deployment | Streamlit Community Cloud (free tier) |
| Repo | GitHub (public, portfolio) |

## Technical decisions
- yfinance fetches up to 1 year of daily OHLCV data by default
- All technical indicators calculated with pandas, no external TA library
- Fibonacci levels calculated from the min/max of the visible range
- Support/resistance detected as price clusters using a rolling window approach
- HF_API_KEY stored in Streamlit Secrets (.streamlit/secrets.toml locally, Streamlit Cloud UI in production)
- AI summary is optional: if HF_API_KEY is missing the app works without it
- Demo button preloads ticker AAPL, 1 year range

## Environment variables
| Variable | Exact name | Environment |
|---|---|---|
| Hugging Face API key | HF_API_KEY | .streamlit/secrets.toml and Streamlit Cloud |

## Folder structure
```
stock-dashboard/
├── PROJECT.md
├── BRIEFING.md
├── .antigravity/
│   └── rules.md
├── .agent/
│   └── skills/
│       └── backend/
│           └── skill.md
├── app.py                        ← Streamlit entry point
├── analysis/
│   ├── __init__.py
│   ├── indicators.py             ← MA, Fibonacci, support/resistance
│   └── summary.py                ← HF Inference API call
├── data/
│   ├── __init__.py
│   ├── fetcher.py                ← yfinance data fetching
│   └── example/
│       └── AAPL_example.csv      ← Preloaded demo data
├── .streamlit/
│   └── secrets.toml              ← HF_API_KEY (do not push to GitHub)
├── requirements.txt
└── .gitignore
```

## Technical indicators to implement
| Indicator | Method |
|---|---|
| MA20, MA50, MA200 | pandas rolling mean on Close price |
| Fibonacci retracement | Levels: 0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0 from range min/max |
| Support / Resistance | Price clusters: rolling window local minima/maxima |
| Volume | Bar chart overlaid on price chart |

## Conventions
- Code language: English
- Comments language: Spanish
- Commits: conventional format (feat:, fix:, docs:, refactor:, chore:)
- Type hints required on all functions
- No external TA libraries (ta, ta-lib): calculate everything with pandas
