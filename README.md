# Climate Challenge Dashboard

Streamlit dashboard for exploring climate insights across multiple countries with interactive filters.

## Objective

Build a code-only Streamlit application that:
- Supports country comparison through multi-select filters.
- Supports time zoom with a year range slider.
- Supports variable switching with a selector (`T2M`, `PRECTOTCORR`, `RH2M`).
- Displays a temperature trend line chart and precipitation distribution boxplot.

## Project Structure

```text
climate-challenge-week0/
├── app/
│   ├── __init__.py
│   ├── main.py          # Streamlit app entry point
│   └── utils.py         # Data loading, filtering, and aggregation helpers
├── scripts/
│   ├── __init__.py
│   └── README.md
├── data/                # Local CSVs (ignored by git)
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup (Local)

1. Create and activate a virtual environment:
   - PowerShell:
     - `python -m venv .venv`
     - `.venv\Scripts\Activate.ps1`
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Add your local CSV files to either:
   - `data/*.csv` (preferred), or
   - repository root `*.csv`
4. Run the app:
   - `streamlit run app/main.py`

## Dashboard Usage

- **Country selector (multi-select):** Compare one or more countries.
- **Year range slider:** Zoom to a target period.
- **Variable selector:** Switch trend variable between `T2M`, `PRECTOTCORR`, and `RH2M`.
- **Charts included:**
  - Monthly variable trend line chart.
  - `PRECTOTCORR` distribution boxplot by country.

## Git Hygiene

- Data is intentionally excluded from version control (`data/` is ignored).
- App reads CSVs locally at runtime; if no CSVs are found, it falls back to deterministic demo data so the dashboard still runs.

## Development Process

Branch used: `dashboard-dev`

1. Added modular Streamlit app layout under `app/`.
2. Implemented reusable utility functions for:
   - CSV discovery and loading.
   - Country/year filtering.
   - Monthly trend aggregation.
3. Added interactive dashboard widgets and KPI tiles.
4. Added deployment and usage documentation.

## Deploy to Streamlit Community Cloud

1. Push repository to GitHub.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New app** and select this repository + branch.
4. Set **Main file path** to `app/main.py`.
5. Click **Deploy**.

After deployment, Streamlit provides a public URL for sharing.
