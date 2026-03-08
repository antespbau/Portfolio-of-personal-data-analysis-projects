from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
import pandas as pd

from improve_helpers import (
    RAW_DIR,
    fetch_energidata,
    ensure_datetime,
    ensure_price_area,
    to_numeric,
    get_wind_columns,
    resample_hourly_by_area,
)

START_DATE = "2023-01-01"
END_DATE = (date.today() - timedelta(days=1)).isoformat()

DATASET = "ProductionConsumptionSettlement"
OUTPUT_PATH = RAW_DIR / "wind_hourly_by_zone.csv"


def main() -> None:
    df = fetch_energidata(DATASET, START_DATE, END_DATE, sort_col="HourUTC")
    df = ensure_datetime(df)
    df = ensure_price_area(df)
    df = df[df["price_area"].isin(["DK1", "DK2"])].copy()

    wind_cols = get_wind_columns(df)
    if not wind_cols:
        raise ValueError(f"No wind columns found. Available columns: {df.columns.tolist()}")

    df = to_numeric(df, wind_cols)
    df["wind_generation"] = df[wind_cols].sum(axis=1, min_count=1)

    out = resample_hourly_by_area(df, ["wind_generation"])
    out.to_csv(OUTPUT_PATH, index=False)

    print(f"Wind columns used: {wind_cols}")
    print(f"Saved wind by zone data to: {OUTPUT_PATH}")
    print(out.head())
    print(out.tail())
    print(out.shape)


if __name__ == "__main__":
    main()