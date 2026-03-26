from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"

INPUT_PATH = PROCESSED_DIR / "model_dataset.csv"
OUTPUT_PATH = PROCESSED_DIR / "directional_dataset.csv"


def add_spread_features(df: pd.DataFrame) -> pd.DataFrame:
    pivot = (
        df.pivot(index="datetime", columns="price_area", values="price")
        .sort_index()
    )

    if {"DK1", "DK2"}.issubset(pivot.columns):
        spread = (pivot["DK1"] - pivot["DK2"]).rename("spread_dk1_dk2").reset_index()
        df = df.merge(spread, on="datetime", how="left")

        spread_df = (
            df[["datetime", "spread_dk1_dk2"]]
            .drop_duplicates()
            .sort_values("datetime")
            .copy()
        )
        spread_df["spread_lag_1"] = spread_df["spread_dk1_dk2"].shift(1)
        spread_df["spread_lag_24"] = spread_df["spread_dk1_dk2"].shift(24)
        spread_df["spread_change_1"] = spread_df["spread_dk1_dk2"].diff(1)
        spread_df["spread_change_24"] = spread_df["spread_dk1_dk2"].diff(24)

        df = df.merge(
            spread_df[
                [
                    "datetime",
                    "spread_lag_1",
                    "spread_lag_24",
                    "spread_change_1",
                    "spread_change_24",
                ]
            ],
            on="datetime",
            how="left",
        )
    else:
        df["spread_dk1_dk2"] = np.nan
        df["spread_lag_1"] = np.nan
        df["spread_lag_24"] = np.nan
        df["spread_change_1"] = np.nan
        df["spread_change_24"] = np.nan

    return df


def main() -> None:
    df = pd.read_csv(INPUT_PATH)
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")

    numeric_cols = [
        "price",
        "price_lag_1",
        "price_lag_24",
        "price_lag_168",
        "rolling_mean_24",
        "rolling_std_24",
        "temperature_2m",
        "gas_price",
        "wind_generation",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["datetime", "price_area", "price"]).copy()
    df = df.sort_values(["price_area", "datetime"]).copy()

    # Directional / change features
    grp = df.groupby("price_area", group_keys=False)

    df["price_change_1"] = grp["price"].diff(1)
    df["price_change_24"] = grp["price"].diff(24)
    df["price_change_168"] = grp["price"].diff(168)

    df["temp_change_1"] = grp["temperature_2m"].diff(1)
    df["temp_change_24"] = grp["temperature_2m"].diff(24)

    df["wind_change_1"] = grp["wind_generation"].diff(1)
    df["wind_change_24"] = grp["wind_generation"].diff(24)

    # Gas is daily, so 24h change is more meaningful than 1h
    df["gas_change_24"] = grp["gas_price"].diff(24)

    # Add cross-area spread features
    df = add_spread_features(df)

    # Targets
    df["target_change_1"] = grp["price"].shift(-1) - df["price"]
    df["target_dir_1"] = (df["target_change_1"] > 0).astype("float")

    df["target_change_24"] = grp["price"].shift(-24) - df["price"]
    df["target_dir_24"] = (df["target_change_24"] > 0).astype("float")

    # Clean impossible rows near boundaries
    df = df.dropna(
        subset=[
            "price_lag_1",
            "price_lag_24",
            "price_lag_168",
            "rolling_mean_24",
            "rolling_std_24",
            "temperature_2m",
            "gas_price",
            "wind_generation",
            "price_change_1",
            "price_change_24",
            "target_change_1",
            "target_dir_1",
        ]
    ).copy()

    df["target_dir_1"] = df["target_dir_1"].astype(int)
    df["target_dir_24"] = df["target_dir_24"].astype(int)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved directional dataset to: {OUTPUT_PATH}")
    print(df.head())
    print(df.shape)


if __name__ == "__main__":
    main()