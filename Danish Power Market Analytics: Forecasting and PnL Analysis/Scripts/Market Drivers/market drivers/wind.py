import requests
import pandas as pd
from datetime import date, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

START_DATE = "2023-03-05"
END_DATE = (date.today() - timedelta(days=1)).isoformat()

BASE_URL = "https://api.energidataservice.dk/dataset"
DATASET = "ProductionConsumptionSettlement"


def fetch_wind_data_by_zone(start_date: str, end_date: str) -> pd.DataFrame:
    url = f"{BASE_URL}/{DATASET}"

    params = {
        "start": f"{start_date}T00:00",
        "end": f"{end_date}T23:59",
        "sort": "HourUTC asc",
        "limit": 0
    }

    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    records = r.json().get("records", [])

    if not records:
        raise ValueError("No wind data returned from EnergiDataService.")

    df = pd.DataFrame(records)

    print("Columns returned from wind dataset:")
    print(df.columns.tolist())

    time_col = "HourUTC"
    area_col = "PriceArea"

    possible_wind_cols = [
        "OffshoreWindLt100MW_MWh",
        "OffshoreWindGe100MW_MWh",
        "OnshoreWindLt50kW_MWh",
        "OnshoreWindGe50kW_MWh"
    ]

    if time_col not in df.columns:
        raise ValueError(f"Expected time column '{time_col}' not found.")

    if area_col not in df.columns:
        raise ValueError(f"Expected area column '{area_col}' not found.")

    existing_wind_cols = [c for c in possible_wind_cols if c in df.columns]
    if not existing_wind_cols:
        raise ValueError(f"No wind columns found. Available columns: {df.columns.tolist()}")

    df["datetime"] = pd.to_datetime(df[time_col], utc=True, errors="coerce")
    df["price_area"] = df[area_col].astype(str)

    for col in existing_wind_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["wind_generation"] = df[existing_wind_cols].sum(axis=1, min_count=1)

    out = (
        df[["datetime", "price_area", "wind_generation"]]
        .dropna(subset=["datetime", "price_area", "wind_generation"])
        .query("price_area in ['DK1', 'DK2']")
        .sort_values(["price_area", "datetime"])
        .drop_duplicates(subset=["datetime", "price_area"])
        .reset_index(drop=True)
    )

    return out


def main() -> None:
    df = fetch_wind_data_by_zone(START_DATE, END_DATE)
    output_path = RAW_DIR / "wind_hourly_by_zone.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved wind by zone data to: {output_path}")
    print(df.head())
    print(df.tail())
    print(df.shape)


if __name__ == "__main__":
    main()