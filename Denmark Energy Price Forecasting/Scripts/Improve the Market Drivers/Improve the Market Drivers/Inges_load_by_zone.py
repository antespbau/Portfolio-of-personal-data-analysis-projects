from __future__ import annotations

from datetime import date, timedelta
import pandas as pd

from improve_helpers import (
    RAW_DIR,
    fetch_energidata,
    ensure_datetime,
    ensure_price_area,
    to_numeric,
    get_load_column,
    resample_hourly_by_area,
)

START_DATE = "2023-01-01"
END_DATE = (date.today() - timedelta(days=1)).isoformat()

DATASET = "ProductionConsumptionSettlement"
OUTPUT_PATH = RAW_DIR / "load_hourly_by_zone.csv"


def main() -> None:
    df = fetch_energidata(DATASET, START_DATE, END_DATE, sort_col="HourUTC")
    df = ensure_datetime(df)
    df = ensure_price_area(df)
    df = df[df["price_area"].isin(["DK1", "DK2"])].copy()

    load_col = get_load_column(df)
    if load_col is None:
        raise ValueError(f"No load/consumption column found. Available columns: {df.columns.tolist()}")

    df = to_numeric(df, [load_col])
    df = df.rename(columns={load_col: "load"})

    out = resample_hourly_by_area(df, ["load"])
    out.to_csv(OUTPUT_PATH, index=False)

    print(f"Load column used: {load_col}")
    print(f"Saved load by zone data to: {OUTPUT_PATH}")
    print(out.head())
    print(out.tail())
    print(out.shape)


if __name__ == "__main__":
    main()