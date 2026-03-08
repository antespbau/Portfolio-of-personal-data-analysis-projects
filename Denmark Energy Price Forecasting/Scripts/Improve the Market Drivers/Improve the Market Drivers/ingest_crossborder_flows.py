from __future__ import annotations

from datetime import date, timedelta
import pandas as pd

from improve_helpers import (
    RAW_DIR,
    fetch_energidata,
    ensure_datetime,
    ensure_price_area,
    to_numeric,
    resample_hourly_by_area,
)

START_DATE = "2023-01-01"
END_DATE = (date.today() - timedelta(days=1)).isoformat()

DATASET = "ProductionConsumptionSettlement"
OUTPUT_PATH = RAW_DIR / "crossborder_flows_hourly.csv"


def main() -> None:
    df = fetch_energidata(DATASET, START_DATE, END_DATE, sort_col="HourUTC")
    df = ensure_datetime(df)
    df = ensure_price_area(df)
    df = df[df["price_area"].isin(["DK1", "DK2"])].copy()

    exchange_map = {
        "flow_NO": "ExchangeNO_MWh",
        "flow_SE": "ExchangeSE_MWh",
        "flow_DE": "ExchangeGE_MWh",
        "flow_NL": "ExchangeNL_MWh",
    }

    for new_col, old_col in exchange_map.items():
        if old_col in df.columns:
            df[new_col] = pd.to_numeric(df[old_col], errors="coerce")
        else:
            df[new_col] = 0.0

    out = resample_hourly_by_area(df, ["flow_DE", "flow_SE", "flow_NO", "flow_NL"])
    out.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved cross-border flows data to: {OUTPUT_PATH}")
    print(out.head())
    print(out.tail())
    print(out.shape)


if __name__ == "__main__":
    main()