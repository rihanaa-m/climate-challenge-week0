from pathlib import Path
from typing import Iterable

import pandas as pd
import numpy as np

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
PREFERRED_COUNTRIES = ["ethiopia", "kenya", "nigeria", "sudan", "tanzania"]
REQUIRED_COLUMNS = {"DATE", "T2M", "PRECTOTCORR", "RH2M"}


def _prepare_country_frame(df: pd.DataFrame, country_name: str) -> pd.DataFrame:
    """Standardize country dataframe columns and add derived date fields."""
    frame = df.copy()
    frame.columns = [col.strip().upper() for col in frame.columns]

    if "COUNTRY" not in frame.columns:
        frame["COUNTRY"] = country_name.title()

    if "DATE" not in frame.columns:
        return pd.DataFrame()

    frame["DATE"] = pd.to_datetime(frame["DATE"], errors="coerce")
    frame = frame.dropna(subset=["DATE"])
    frame["YEAR_INT"] = frame["DATE"].dt.year.astype(int)
    frame["MONTH"] = frame["DATE"].dt.month.astype(int)
    return frame


def _discover_csv_paths(data_dir: Path) -> Iterable[Path]:
    """Yield CSV files from data/ then fallback to repository root."""
    csv_in_data = sorted(data_dir.glob("*.csv"))
    if csv_in_data:
        return csv_in_data
    return sorted(ROOT_DIR.glob("*.csv"))


def load_data() -> pd.DataFrame:
    """Load and concatenate climate CSV files from local workspace."""
    frames: list[pd.DataFrame] = []
    csv_paths = _discover_csv_paths(DATA_DIR)

    for csv_path in csv_paths:
        try:
            raw = pd.read_csv(csv_path)
        except Exception:
            continue

        country = csv_path.stem.replace("_clean", "").replace("_", " ")
        prepared = _prepare_country_frame(raw, country)
        if prepared.empty or not REQUIRED_COLUMNS.issubset(set(prepared.columns)):
            continue
        frames.append(prepared)

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)
    combined = combined.sort_values(["COUNTRY", "DATE"]).reset_index(drop=True)
    combined["COUNTRY"] = combined["COUNTRY"].astype(str).str.title()
    return combined


def generate_demo_data(
    countries: list[str] | None = None,
    start_year: int = 2000,
    end_year: int = 2005,
    seed: int = 42,
) -> pd.DataFrame:
    """Generate deterministic demo data so the dashboard works without CSVs.

    This is useful for code-only submissions and for Streamlit Community Cloud
    deploys where `data/` is not committed.
    """
    rng = np.random.default_rng(seed)
    if not countries:
        countries = [name.title() for name in PREFERRED_COUNTRIES]

    dates = pd.date_range(f"{start_year}-01-01", f"{end_year}-12-01", freq="MS")

    rows: list[dict[str, object]] = []
    for country in countries:
        # Simple seasonal pattern + noise for visual realism.
        month = dates.month.values
        seasonal = np.sin((month - 1) / 12 * 2 * np.pi)

        t2m = 25 + 5 * seasonal + rng.normal(0, 1.2, size=len(dates))
        prectotcorr = np.clip(120 + 70 * seasonal + rng.normal(0, 25, size=len(dates)), 0, None)
        rh2m = np.clip(60 + 15 * seasonal + rng.normal(0, 6, size=len(dates)), 0, 100)

        for dt, t, p, h in zip(dates, t2m, prectotcorr, rh2m):
            rows.append(
                {
                    "COUNTRY": country,
                    "DATE": dt,
                    "SOURCE": "demo",
                    "YEAR_INT": int(dt.year),
                    "MONTH": int(dt.month),
                    "T2M": float(t),
                    "PRECTOTCORR": float(p),
                    "RH2M": float(h),
                }
            )

    return pd.DataFrame(rows)


def load_data_with_demo_fallback() -> pd.DataFrame:
    """Load real CSV data; if unavailable, fall back to deterministic demo data."""
    df = load_data()
    if df.empty:
        return generate_demo_data()
    return df


def get_country_options(df: pd.DataFrame) -> list[str]:
    """Return ordered country list with preferred countries first."""
    available = sorted(df["COUNTRY"].dropna().unique().tolist())
    preferred = [name.title() for name in PREFERRED_COUNTRIES if name.title() in available]
    remaining = [name for name in available if name not in preferred]
    return preferred + remaining


def filter_data(df: pd.DataFrame, countries: list[str], year_range: tuple[int, int]) -> pd.DataFrame:
    """Filter data by selected countries and year range."""
    if df.empty:
        return df

    filtered = df.copy()
    if countries:
        filtered = filtered[filtered["COUNTRY"].isin(countries)]

    start_year, end_year = year_range
    return filtered[(filtered["YEAR_INT"] >= start_year) & (filtered["YEAR_INT"] <= end_year)]


def get_monthly_trends(df: pd.DataFrame, variable: str) -> pd.DataFrame:
    """Aggregate selected variable to monthly mean by country."""
    if df.empty or variable not in df.columns:
        return pd.DataFrame()

    monthly = (
        df.groupby(["COUNTRY", "YEAR_INT", "MONTH"], as_index=False)[variable]
        .mean()
        .sort_values(["COUNTRY", "YEAR_INT", "MONTH"])
    )
    monthly["PLOT_DATE"] = pd.to_datetime(
        {"year": monthly["YEAR_INT"], "month": monthly["MONTH"], "day": 1}
    )
    return monthly