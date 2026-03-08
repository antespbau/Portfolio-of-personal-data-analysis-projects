from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PNG_DIR = BASE_DIR / "PNG"

PNG_DIR.mkdir(parents=True, exist_ok=True)

MODEL_DATASET_PATH = PROCESSED_DIR / "model_dataset.csv"
PREDICTIONS_PATH = PROCESSED_DIR / "market_drivers_predictions.csv"
MARKET_FORECAST_PATH = PROCESSED_DIR / "forecast_next_week_market_drivers.csv"
BASIC_FORECAST_PATH = BASE_DIR / "forecast_next_week_hourly.csv"

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
    "hour",
    "day_of_week",
    "month",
    "is_weekend",
]


def load_data():
    model_df = pd.read_csv(MODEL_DATASET_PATH)
    preds_df = pd.read_csv(PREDICTIONS_PATH)
    market_forecast_df = pd.read_csv(MARKET_FORECAST_PATH)
    basic_forecast_df = pd.read_csv(BASIC_FORECAST_PATH)

    model_df["datetime"] = pd.to_datetime(model_df["datetime"], utc=True, errors="coerce")

    preds_df["datetime"] = pd.to_datetime(preds_df["datetime"], utc=True, errors="coerce")
    preds_df["price"] = pd.to_numeric(preds_df["price"], errors="coerce")
    preds_df["prediction"] = pd.to_numeric(preds_df["prediction"], errors="coerce")

    market_forecast_df["hour_utc"] = pd.to_datetime(
        market_forecast_df["hour_utc"], utc=True, errors="coerce"
    )
    market_forecast_df["pred_spot_price_eur"] = pd.to_numeric(
        market_forecast_df["pred_spot_price_eur"], errors="coerce"
    )

    basic_forecast_df["hour_utc"] = pd.to_datetime(
        basic_forecast_df["hour_utc"], utc=True, errors="coerce"
    )
    basic_forecast_df["pred_spot_price_eur"] = pd.to_numeric(
        basic_forecast_df["pred_spot_price_eur"], errors="coerce"
    )

    return model_df, preds_df, market_forecast_df, basic_forecast_df


def make_correlation_heatmap(model_df: pd.DataFrame, area: str):

    area_df = model_df[model_df["price_area"] == area].copy()

    corr_cols = [
        "price",
        "price_lag_1",
        "price_lag_24",
        "price_lag_168",
        "rolling_mean_24",
        "rolling_std_24",
        "temperature_2m",
        "gas_price",
        "wind_generation",
        "hour",
        "day_of_week",
        "month",
        "is_weekend",
    ]

    area_df = area_df.dropna(subset=corr_cols)

    corr = area_df[corr_cols].corr()

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
        cbar=True
    )

    plt.title(f"Correlation with Electricity Price ({area})", fontsize=14)
    plt.tight_layout()

    output = PNG_DIR / f"price_correlation_{area}.png"

    plt.savefig(output, dpi=300)
    plt.close()

    print("Saved:", output)
    area_df = model_df[model_df["price_area"] == area].copy()

    corr_cols = [
        "price",
        "price_lag_1",
        "price_lag_24",
        "price_lag_168",
        "rolling_mean_24",
        "rolling_std_24",
        "temperature_2m",
        "gas_price",
        "wind_generation",
        "hour",
        "day_of_week",
        "month",
        "is_weekend",
    ]

    area_df = area_df.dropna(subset=corr_cols)

    corr = area_df[corr_cols].corr()

    plt.figure(figsize=(12, 10))

    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8}
    )

    plt.title(f"Correlation Matrix - Market Drivers ({area})", fontsize=16)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)

    plt.tight_layout()

    output = PNG_DIR / f"correlation_heatmap_{area}.png"
    plt.savefig(output, dpi=300)
    plt.close()

    print("Saved:", output)

def make_actual_vs_predicted(preds_df: pd.DataFrame, area: str):
    area_df = preds_df[preds_df["price_area"] == area].copy()
    area_df = area_df.dropna(subset=["datetime", "price", "prediction"])
    area_df = area_df.tail(24 * 7)

    plt.figure(figsize=(14, 6))
    plt.plot(area_df["datetime"], area_df["price"], label=f"Actual {area}")
    plt.plot(area_df["datetime"], area_df["prediction"], label=f"Predicted {area}")
    plt.title(f"Actual vs Predicted Electricity Prices - {area}")
    plt.xlabel("Datetime")
    plt.ylabel("Price EUR/MWh")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(PNG_DIR / f"actual_vs_predicted_{area}.png", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved: {PNG_DIR / f'actual_vs_predicted_{area}.png'}")


def make_forecast_comparison(
    model_df: pd.DataFrame,
    market_forecast_df: pd.DataFrame,
    basic_forecast_df: pd.DataFrame,
    area: str
):
    actual_area = model_df[model_df["price_area"] == area].copy()
    actual_area = actual_area.dropna(subset=["datetime", "price"]).tail(24 * 7)

    market_area = market_forecast_df[market_forecast_df["price_area"] == area].copy()
    market_area = market_area.dropna(subset=["hour_utc", "pred_spot_price_eur"])

    basic_area = basic_forecast_df[basic_forecast_df["price_area"] == area].copy()
    basic_area = basic_area.dropna(subset=["hour_utc", "pred_spot_price_eur"])

    plt.figure(figsize=(14, 6))

    plt.plot(
        actual_area["datetime"],
        actual_area["price"],
        label=f"Actual {area}",
        linewidth=2
    )

    plt.plot(
        basic_area["hour_utc"],
        basic_area["pred_spot_price_eur"],
        label=f"Basic Model Forecast {area}",
        linestyle="--"
    )

    plt.plot(
        market_area["hour_utc"],
        market_area["pred_spot_price_eur"],
        label=f"Market Drivers Forecast {area}",
        linestyle="--"
    )

    plt.title(f"Forecast Comparison - {area}")
    plt.xlabel("Datetime")
    plt.ylabel("Price EUR/MWh")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(PNG_DIR / f"forecast_comparison_{area}.png", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved: {PNG_DIR / f'forecast_comparison_{area}.png'}")


def main():
    model_df, preds_df, market_forecast_df, basic_forecast_df = load_data()

    for area in AREAS:
        print(f"\nGenerating plots for {area}...")
        make_correlation_heatmap(model_df, area)
        make_actual_vs_predicted(preds_df, area)
        make_forecast_comparison(model_df, market_forecast_df, basic_forecast_df, area)


if __name__ == "__main__":
    main()