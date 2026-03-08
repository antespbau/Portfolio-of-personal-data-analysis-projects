from __future__ import annotations

from datetime import timedelta
import pandas as pd
from xgboost import XGBRegressor

from improve_helpers import PROCESSED_DIR

MODEL_DATASET_PATH = PROCESSED_DIR / "improve_market_drivers_dataset.csv"
FORECAST_OUTPUT = PROCESSED_DIR / "forecast_next_week_improve_market_drivers.csv"

FEATURE_COLS = [
    "price_lag_1",
    "price_lag_24",
    "price_lag_168",
    "rolling_mean_24",
    "rolling_std_24",
    "temperature_2m",
    "gas_price",
    "wind_generation",
    "load",
    "flow_DE",
    "flow_SE",
    "flow_NO",
    "flow_NL",
    "hour",
    "day_of_week",
    "month",
    "is_weekend",
]

TARGET_COL = "price"
AREAS = ["DK1", "DK2"]


def train_model(df: pd.DataFrame) -> XGBRegressor:
    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    model = XGBRegressor(
        n_estimators=500,
        learning_rate=0.04,
        max_depth=6,
        min_child_weight=3,
        subsample=0.85,
        colsample_bytree=0.85,
        reg_alpha=0.0,
        reg_lambda=1.0,
        objective="reg:squarederror",
        random_state=42,
    )
    model.fit(X, y)
    return model


def seasonal_exog_value(df_area: pd.DataFrame, col: str, seasonal_lag: int = 24) -> float:
    if len(df_area) >= seasonal_lag:
        val = df_area[col].iloc[-seasonal_lag]
        if pd.notna(val):
            return float(val)

    recent = df_area[col].tail(24).dropna()
    if not recent.empty:
        return float(recent.mean())

    return 0.0


def forecast_one_area(model: XGBRegressor, df_area: pd.DataFrame, area: str) -> pd.DataFrame:
    df_area = df_area.sort_values("datetime").copy()
    forecasts = []

    for _ in range(168):
        last_time = df_area["datetime"].iloc[-1]
        new_time = last_time + timedelta(hours=1)

        row = {
            "datetime": new_time,
            "price_area": area,
            "price_lag_1": df_area["price"].iloc[-1],
            "price_lag_24": df_area["price"].iloc[-24],
            "price_lag_168": df_area["price"].iloc[-168],
            "rolling_mean_24": df_area["price"].tail(24).mean(),
            "rolling_std_24": df_area["price"].tail(24).std(),
            "temperature_2m": seasonal_exog_value(df_area, "temperature_2m"),
            "gas_price": seasonal_exog_value(df_area, "gas_price"),
            "wind_generation": seasonal_exog_value(df_area, "wind_generation"),
            "load": seasonal_exog_value(df_area, "load"),
            "flow_DE": seasonal_exog_value(df_area, "flow_DE"),
            "flow_SE": seasonal_exog_value(df_area, "flow_SE"),
            "flow_NO": seasonal_exog_value(df_area, "flow_NO"),
            "flow_NL": seasonal_exog_value(df_area, "flow_NL"),
            "hour": new_time.hour,
            "day_of_week": new_time.dayofweek,
            "month": new_time.month,
            "is_weekend": int(new_time.dayofweek >= 5),
        }

        X = pd.DataFrame([row])[FEATURE_COLS]
        pred = float(model.predict(X)[0])

        row["price"] = pred
        forecasts.append(row)

        df_area = pd.concat([df_area, pd.DataFrame([row])], ignore_index=True)

    return pd.DataFrame(forecasts)


def main() -> None:
    df = pd.read_csv(MODEL_DATASET_PATH)
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")
    df = df.dropna(subset=FEATURE_COLS + [TARGET_COL, "price_area"]).copy()

    all_forecasts = []

    for area in AREAS:
        print(f"\nTraining and forecasting improved model for {area}...")
        area_df = df[df["price_area"] == area].copy().sort_values("datetime")

        if len(area_df) < 200:
            raise ValueError(f"Not enough data for {area}.")

        model = train_model(area_df)
        forecast_area = forecast_one_area(model, area_df, area)
        all_forecasts.append(forecast_area)

    forecast_df = pd.concat(all_forecasts, ignore_index=True)
    forecast_df = forecast_df.rename(columns={"datetime": "hour_utc", "price": "pred_spot_price_eur"})
    forecast_df = forecast_df[["hour_utc", "price_area", "pred_spot_price_eur"]]
    forecast_df.to_csv(FORECAST_OUTPUT, index=False)

    print("\nForecast saved to:")
    print(FORECAST_OUTPUT)
    print(forecast_df.head())


if __name__ == "__main__":
    main()