from __future__ import annotations

from pathlib import Path
import duckdb
import pandas as pd

from improve_helpers import BASE_DIR, RAW_DIR, PROCESSED_DIR

DB_PATH = BASE_DIR / "energy.duckdb"

TEMPERATURE_PATH = RAW_DIR / "temperature_hourly.csv"
GAS_PATH = RAW_DIR / "gas_daily.csv"
WIND_PATH = RAW_DIR / "wind_hourly_by_zone.csv"
LOAD_PATH = RAW_DIR / "load_hourly_by_zone.csv"
FLOW_PATH = RAW_DIR / "crossborder_flows_hourly.csv"

OUTPUT_DATASET = PROCESSED_DIR / "improve_market_drivers_dataset.csv"


def load_prices_from_duckdb(db_path: Path) -> pd.DataFrame:
    con = duckdb.connect(str(db_path))
    query = """
        SELECT
            hour_utc,
            price_area,
            spot_price_eur
        FROM actuals
        WHERE price_area IN ('DK1', 'DK2')
        ORDER BY price_area, hour_utc
    """
    df = con.execute(query).fetchdf()
    con.close()

    if df.empty:
        raise ValueError("No price data found in DuckDB table 'actuals'.")

    df = df.rename(columns={"hour_utc": "datetime", "spot_price_eur": "price"})
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["price_area"] = df["price_area"].astype(str)
    df = df.dropna(subset=["datetime", "price", "price_area"])
    df = df.sort_values(["price_area", "datetime"]).drop_duplicates(subset=["datetime", "price_area"])

    return df[["datetime", "price_area", "price"]]


def load_temperature(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")
    df["temperature_2m"] = pd.to_numeric(df["temperature_2m"], errors="coerce")
    df = df.dropna(subset=["datetime"]).sort_values("datetime").drop_duplicates(subset=["datetime"])
    return df[["datetime", "temperature_2m"]]


def load_gas(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    df["gas_price"] = pd.to_numeric(df["gas_price"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date").drop_duplicates(subset=["date"])
    return df[["date", "gas_price"]]


def load_area_file(path: Path, expected_cols: list[str]) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")
    df["price_area"] = df["price_area"].astype(str)

    for col in expected_cols:
        if col not in df.columns:
            df[col] = pd.NA
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["datetime", "price_area"]).copy()
    df = df.sort_values(["price_area", "datetime"]).drop_duplicates(subset=["datetime", "price_area"])

    return df[["datetime", "price_area"] + expected_cols]


def build_base_dataset() -> pd.DataFrame:
    prices_df = load_prices_from_duckdb(DB_PATH)
    temp_df = load_temperature(TEMPERATURE_PATH)
    gas_df = load_gas(GAS_PATH)
    wind_df = load_area_file(WIND_PATH, ["wind_generation"])
    load_df = load_area_file(LOAD_PATH, ["load"])
    flow_df = load_area_file(FLOW_PATH, ["flow_DE", "flow_SE", "flow_NO", "flow_NL"])

    df = prices_df.copy()
    df = df.merge(temp_df, on="datetime", how="left")
    df = df.merge(wind_df, on=["datetime", "price_area"], how="left")
    df = df.merge(load_df, on=["datetime", "price_area"], how="left")
    df = df.merge(flow_df, on=["datetime", "price_area"], how="left")

    df["date"] = df["datetime"].dt.date
    df = df.merge(gas_df, on="date", how="left")

    df = df.sort_values(["price_area", "datetime"]).copy()

    # Fill exogenous series carefully
    df["gas_price"] = df["gas_price"].ffill()

    for col in ["temperature_2m", "wind_generation", "load"]:
        df[col] = (
            df.groupby("price_area")[col]
            .transform(lambda s: s.interpolate(limit_direction="both"))
        )

    for col in ["flow_DE", "flow_SE", "flow_NO", "flow_NL"]:
        df[col] = (
            df.groupby("price_area")[col]
            .transform(lambda s: s.fillna(0.0))
        )

    return df


def add_model_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["price_area", "datetime"]).copy()

    df["price_lag_1"] = df.groupby("price_area")["price"].shift(1)
    df["price_lag_24"] = df.groupby("price_area")["price"].shift(24)
    df["price_lag_168"] = df.groupby("price_area")["price"].shift(168)

    shifted = df.groupby("price_area")["price"].shift(1)

    df["rolling_mean_24"] = (
        shifted.groupby(df["price_area"])
        .rolling(24)
        .mean()
        .reset_index(level=0, drop=True)
    )

    df["rolling_std_24"] = (
        shifted.groupby(df["price_area"])
        .rolling(24)
        .std()
        .reset_index(level=0, drop=True)
    )

    df["hour"] = df["datetime"].dt.hour
    df["day_of_week"] = df["datetime"].dt.dayofweek
    df["month"] = df["datetime"].dt.month
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

    return df


def main() -> None:
    df = build_base_dataset()
    df = add_model_features(df)

    df.to_csv(OUTPUT_DATASET, index=False)

    print(f"Saved improved model dataset to: {OUTPUT_DATASET}")
    print(df.head())
    print(df.tail())
    print(df.shape)


if __name__ == "__main__":
    main()