from pathlib import Path
import pandas as pd
import duckdb

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = BASE_DIR / "energy.duckdb"
TEMPERATURE_PATH = RAW_DIR / "temperature_hourly.csv"
GAS_PATH = RAW_DIR / "gas_daily.csv"
WIND_PATH = RAW_DIR / "wind_hourly.csv"

OUTPUT_MARKET_DRIVERS = PROCESSED_DIR / "market_drivers_dataset.csv"
OUTPUT_MODEL_DATASET = PROCESSED_DIR / "model_dataset.csv"


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

    df = df.rename(columns={
        "hour_utc": "datetime",
        "spot_price_eur": "price"
    })

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
    df = df.dropna(subset=["datetime", "temperature_2m"])
    df = df.sort_values("datetime").drop_duplicates(subset=["datetime"])
    return df[["datetime", "temperature_2m"]]


def load_gas(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    df["gas_price"] = pd.to_numeric(df["gas_price"], errors="coerce")
    df = df.dropna(subset=["date", "gas_price"])
    df = df.sort_values("date").drop_duplicates(subset=["date"])
    return df[["date", "gas_price"]]


def load_wind(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")
    df["wind_generation"] = pd.to_numeric(df["wind_generation"], errors="coerce")
    df = df.dropna(subset=["datetime", "wind_generation"])
    df = df.sort_values("datetime").drop_duplicates(subset=["datetime"])
    return df[["datetime", "wind_generation"]]


def build_market_drivers_dataset(
    prices_df: pd.DataFrame,
    temp_df: pd.DataFrame,
    gas_df: pd.DataFrame,
    wind_df: pd.DataFrame,
) -> pd.DataFrame:
    df = prices_df.copy()

    df = df.merge(temp_df, on="datetime", how="left")
    df = df.merge(wind_df, on="datetime", how="left")

    df["date"] = df["datetime"].dt.date
    df = df.merge(gas_df, on="date", how="left")

    df["gas_price"] = df["gas_price"].ffill()
    df["wind_generation"] = df["wind_generation"].interpolate(limit_direction="both")

    return df


def build_model_dataset(df: pd.DataFrame) -> pd.DataFrame:
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
    prices_df = load_prices_from_duckdb(DB_PATH)
    temp_df = load_temperature(TEMPERATURE_PATH)
    gas_df = load_gas(GAS_PATH)
    wind_df = load_wind(WIND_PATH)

    market_df = build_market_drivers_dataset(prices_df, temp_df, gas_df, wind_df)
    market_df.to_csv(OUTPUT_MARKET_DRIVERS, index=False)

    model_df = build_model_dataset(market_df)
    model_df.to_csv(OUTPUT_MODEL_DATASET, index=False)

    print(f"Saved market drivers dataset to: {OUTPUT_MARKET_DRIVERS}")
    print(f"Saved model dataset to: {OUTPUT_MODEL_DATASET}")
    print(model_df.head())
    print(model_df.tail())
    print(model_df.shape)


if __name__ == "__main__":
    main()