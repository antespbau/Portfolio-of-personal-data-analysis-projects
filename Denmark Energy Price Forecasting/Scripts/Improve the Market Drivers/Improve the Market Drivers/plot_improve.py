from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from improve_helpers import BASE_DIR, PROCESSED_DIR

PNG_DIR = BASE_DIR / "PNG"
PNG_DIR.mkdir(parents=True, exist_ok=True)

MODEL_DATASET_PATH = PROCESSED_DIR / "improve_market_drivers_dataset.csv"
PREDICTIONS_PATH = PROCESSED_DIR / "improve_market_drivers_predictions.csv"
FORECAST_PATH = PROCESSED_DIR / "forecast_next_week_improve_market_drivers.csv"

AREAS = ["DK1", "DK2"]

CORR_COLS = [
    "price",
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


def load_data():
    model_df = pd.read_csv(MODEL_DATASET_PATH)
    preds_df = pd.read_csv(PREDICTIONS_PATH)
    forecast_df = pd.read_csv(FORECAST_PATH)

    model_df["datetime"] = pd.to_datetime(model_df["datetime"], utc=True, errors="coerce")

    preds_df["datetime"] = pd.to_datetime(preds_df["datetime"], utc=True, errors="coerce")
    preds_df["price"] = pd.to_numeric(preds_df["price"], errors="coerce")
    preds_df["prediction"] = pd.to_numeric(preds_df["prediction"], errors="coerce")

    forecast_df["hour_utc"] = pd.to_datetime(forecast_df["hour_utc"], utc=True, errors="coerce")
    forecast_df["pred_spot_price_eur"] = pd.to_numeric(forecast_df["pred_spot_price_eur"], errors="coerce")

    return model_df, preds_df, forecast_df


def make_price_correlation(model_df: pd.DataFrame, area: str) -> None:
    area_df = model_df[model_df["price_area"] == area].copy().dropna(subset=CORR_COLS)
    corr = area_df[CORR_COLS].corr()
    price_corr = corr["price"].drop("price").sort_values(ascending=False)
    heatmap_df = price_corr.to_frame(name="correlation")

    plt.figure(figsize=(6, 8))
    sns.heatmap(
        heatmap_df,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        linewidths=0.5,
        cbar=True,
    )
    plt.title(f"Correlation with Price - Improve Market Drivers ({area})")
    plt.tight_layout()
    plt.savefig(PNG_DIR / f"price_correlation_improve_market_drivers_{area}.png", dpi=300)
    plt.close()


def make_actual_vs_predicted(preds_df: pd.DataFrame, area: str) -> None:
    area_df = preds_df[preds_df["price_area"] == area].copy()
    area_df = area_df.dropna(subset=["datetime", "price", "prediction"]).tail(24 * 7)

    plt.figure(figsize=(14, 6))
    plt.plot(area_df["datetime"], area_df["price"], label=f"Actual {area}")
    plt.plot(area_df["datetime"], area_df["prediction"], label=f"Predicted {area}")
    plt.title(f"Actual vs Predicted - Improve Market Drivers - {area}")
    plt.xlabel("Datetime")
    plt.ylabel("Price EUR/MWh")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(
        PNG_DIR / f"actual_vs_predicted_improve_market_drivers_{area}.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()


def make_forecast_plot(model_df: pd.DataFrame, forecast_df: pd.DataFrame, area: str) -> None:
    actual_area = (
        model_df[model_df["price_area"] == area]
        .copy()
        .dropna(subset=["datetime", "price"])
        .tail(24 * 7)
    )

    forecast_area = (
        forecast_df[forecast_df["price_area"] == area]
        .copy()
        .dropna(subset=["hour_utc", "pred_spot_price_eur"])
    )

    plt.figure(figsize=(14, 6))
    plt.plot(actual_area["datetime"], actual_area["price"], label=f"Actual {area}", linewidth=2)
    plt.plot(
        forecast_area["hour_utc"],
        forecast_area["pred_spot_price_eur"],
        label=f"Forecast {area}",
        linestyle="--",
    )
    plt.title(f"Next Week Forecast - Improve Market Drivers - {area}")
    plt.xlabel("Datetime")
    plt.ylabel("Price EUR/MWh")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(
        PNG_DIR / f"forecast_next_week_improve_market_drivers_{area}.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()


def main() -> None:
    model_df, preds_df, forecast_df = load_data()

    for area in AREAS:
        print(f"\nGenerating plots for {area}...")
        make_price_correlation(model_df, area)
        make_actual_vs_predicted(preds_df, area)
        make_forecast_plot(model_df, forecast_df, area)


if __name__ == "__main__":
    main()