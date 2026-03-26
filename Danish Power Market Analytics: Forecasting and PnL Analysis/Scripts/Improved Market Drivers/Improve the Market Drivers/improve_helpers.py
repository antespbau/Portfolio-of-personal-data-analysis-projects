from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence
import requests
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://api.energidataservice.dk/dataset"


def normalize_name(name: str) -> str:
    return (
        str(name)
        .strip()
        .lower()
        .replace(" ", "")
        .replace("_", "")
        .replace("-", "")
    )


def first_existing_column(df: pd.DataFrame, candidates: Sequence[str]) -> str | None:
    normalized = {normalize_name(c): c for c in df.columns}
    for candidate in candidates:
        found = normalized.get(normalize_name(candidate))
        if found is not None:
            return found
    return None


def find_column_by_token_groups(
    df: pd.DataFrame,
    token_groups: Sequence[Sequence[str]],
) -> str | None:
    for col in df.columns:
        ncol = normalize_name(col)
        for group in token_groups:
            if all(token in ncol for token in group):
                return col
    return None


def find_columns_by_token_groups(
    df: pd.DataFrame,
    token_groups: Sequence[Sequence[str]],
) -> list[str]:
    out: list[str] = []
    for col in df.columns:
        ncol = normalize_name(col)
        for group in token_groups:
            if all(token in ncol for token in group):
                out.append(col)
                break
    return out


def ensure_datetime(
    df: pd.DataFrame,
    candidates: Sequence[str] = ("HourUTC", "Minutes5UTC", "datetime"),
) -> pd.DataFrame:
    time_col = first_existing_column(df, candidates)
    if time_col is None:
        raise ValueError(
            f"Could not find datetime column. Available columns: {df.columns.tolist()}"
        )
    df = df.copy()
    df["datetime"] = pd.to_datetime(df[time_col], utc=True, errors="coerce")
    df = df.dropna(subset=["datetime"])
    return df


def ensure_price_area(
    df: pd.DataFrame,
    candidates: Sequence[str] = ("PriceArea", "price_area"),
) -> pd.DataFrame:
    area_col = first_existing_column(df, candidates)
    if area_col is None:
        raise ValueError(
            f"Could not find price area column. Available columns: {df.columns.tolist()}"
        )
    df = df.copy()
    df["price_area"] = df[area_col].astype(str).str.strip()
    return df


def to_numeric(df: pd.DataFrame, cols: Iterable[str]) -> pd.DataFrame:
    df = df.copy()
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def fetch_energidata(
    dataset: str,
    start_date: str,
    end_date: str,
    sort_col: str = "HourUTC",
    extra_params: dict | None = None,
) -> pd.DataFrame:
    url = f"{BASE_URL}/{dataset}"
    params = {
        "start": f"{start_date}T00:00",
        "end": f"{end_date}T23:59",
        "sort": f"{sort_col} asc",
        "limit": 0,
    }
    if extra_params:
        params.update(extra_params)

    response = requests.get(url, params=params, timeout=120)
    response.raise_for_status()
    payload = response.json()
    records = payload.get("records", [])

    if not records:
        raise ValueError(f"No records returned from dataset {dataset}.")

    return pd.DataFrame(records)


def resample_hourly_by_area(
    df: pd.DataFrame,
    value_cols: Sequence[str],
) -> pd.DataFrame:
    existing = [c for c in value_cols if c in df.columns]
    if not existing:
        raise ValueError("No value columns were found for hourly resampling.")

    out = (
        df[["datetime", "price_area"] + existing]
        .dropna(subset=["datetime", "price_area"])
        .set_index("datetime")
        .groupby("price_area")[existing]
        .resample("h")
        .mean()
        .reset_index()
        .sort_values(["price_area", "datetime"])
    )
    return out


def get_wind_columns(df: pd.DataFrame) -> list[str]:
    # Very defensive because naming varies across releases
    token_groups = [
        ("onshore", "wind"),
        ("offshore", "wind"),
        ("windpower",),
        ("wind",),
    ]
    cols = find_columns_by_token_groups(df, token_groups)

    # remove forecast/prognosis-style columns if they appear
    filtered = []
    for col in cols:
        ncol = normalize_name(col)
        if "forecast" in ncol or "progn" in ncol or "expected" in ncol:
            continue
        filtered.append(col)

    # de-duplicate while preserving order
    seen = set()
    unique = []
    for col in filtered:
        if col not in seen:
            seen.add(col)
            unique.append(col)
    return unique


def get_load_column(df: pd.DataFrame) -> str | None:
    priority_groups = [
        ("gross", "consumption"),
        ("consumption", "mwh"),
        ("consumption",),
        ("load",),
    ]
    return find_column_by_token_groups(df, priority_groups)


def get_exchange_columns(df: pd.DataFrame) -> dict[str, str | None]:
    return {
        "flow_DE": find_column_by_token_groups(df, [("exchange", "germany"), ("germany",)]),
        "flow_SE": find_column_by_token_groups(df, [("exchange", "sweden"), ("sweden",)]),
        "flow_NO": find_column_by_token_groups(df, [("exchange", "norway"), ("norway",)]),
        "flow_NL": find_column_by_token_groups(df, [("exchange", "netherlands"), ("netherlands",)]),
    }