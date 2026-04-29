from pathlib import Path
from typing import Iterable

import pandas as pd

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