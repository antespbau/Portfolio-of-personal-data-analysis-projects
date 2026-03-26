from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PNG_DIR = BASE_DIR / "PNG"

PNG_DIR.mkdir(parents=True, exist_ok=True)

BASIC_FORECAST = BASE_DIR / "forecast_next_week_hourly.csv"
MARKET_FORECAST = PROCESSED_DIR / "forecast_next_week_market_drivers.csv"
IMPROVE_FORECAST = PROCESSED_DIR / "forecast_next_week_improve_market_drivers.csv"
ACTUAL_DATA = PROCESSED_DIR / "model_dataset.csv"


def main():
    basic = pd.read_csv(BASIC_FORECAST)
    market = pd.read_csv(MARKET_FORECAST)
    improve = pd.read_csv(IMPROVE_FORECAST)
    actual = pd.read_csv(ACTUAL_DATA)

    basic["datetime"] = pd.to_datetime(basic["hour_utc"], utc=True, errors="coerce")
    basic["price"] = pd.to_numeric(basic["pred_spot_price_eur"], errors="coerce")

    market["datetime"] = pd.to_datetime(market["hour_utc"], utc=True, errors="coerce")
    market["price"] = pd.to_numeric(market["pred_spot_price_eur"], errors="coerce")

    improve["datetime"] = pd.to_datetime(improve["hour_utc"], utc=True, errors="coerce")
    improve["price"] = pd.to_numeric(improve["pred_spot_price_eur"], errors="coerce")

    actual["datetime"] = pd.to_datetime(actual["datetime"], utc=True, errors="coerce")
    actual["price"] = pd.to_numeric(actual["price"], errors="coerce")

    basic = basic.dropna(subset=["datetime", "price", "price_area"]).copy()
    market = market.dropna(subset=["datetime", "price", "price_area"]).copy()
    improve = improve.dropna(subset=["datetime", "price", "price_area"]).copy()
    actual = actual.dropna(subset=["datetime", "price", "price_area"]).copy()

    for area in ["DK1", "DK2"]:
        basic_area = basic[basic["price_area"] == area].copy()
        market_area = market[market["price_area"] == area].copy()
        improve_area = improve[improve["price_area"] == area].copy()
        actual_area = actual[actual["price_area"] == area].tail(24 * 7).copy()

        output_plot = PNG_DIR / f"forecast_comparison_models_{area}.png"

        plt.figure(figsize=(14,6))

        # Actual price
        plt.plot(
            actual_area["datetime"],
            actual_area["price"],
            label="Actual Price",
            color="#1f77b4",
            linewidth=2
        )

        # Basic model
        plt.plot(
            basic_area["datetime"],
            basic_area["price"],
            label="Basic Model",
            linestyle="--",
            color="#FFD700",
            linewidth=1.2,
            alpha=0.45
        )

        # Improve model
        plt.plot(
            improve_area["datetime"],
            improve_area["price"],
            label="Improve Market Drivers",
            linestyle="--",
            color="#FF8C00",
            linewidth=1.2,
            alpha=0.45
        )

        # Best model
        plt.plot(
            market_area["datetime"],
            market_area["price"],
            label="Market Drivers (Best Model)",
            color="#2ca02c",
            linewidth=1.6
        )

        plt.title(f"Electricity Price Forecast Comparison ({area})")
        plt.xlabel("Datetime")
        plt.ylabel("Price EUR/MWh")

        plt.legend(frameon=False)
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.savefig(output_plot, dpi=300, bbox_inches="tight")
        plt.close()

        print("Saved plot to:", output_plot)


if __name__ == "__main__":
    main()