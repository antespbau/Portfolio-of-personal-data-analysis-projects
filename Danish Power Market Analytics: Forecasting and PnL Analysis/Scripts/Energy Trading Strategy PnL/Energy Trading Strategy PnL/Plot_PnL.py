from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "outputs" / "plots"

INPUT_PATH = PROCESSED_DIR / "directional_backtest_results.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    df = pd.read_csv(INPUT_PATH)
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")
    df["net_pnl"] = pd.to_numeric(df["net_pnl"], errors="coerce")

    df = df.dropna(subset=["datetime", "price_area", "net_pnl"]).copy()
    df = df.sort_values(["price_area", "datetime"]).copy()
    return df


def build_daily_pnl(df):
    daily = (
        df.groupby(["price_area", pd.Grouper(key="datetime", freq="D")])["net_pnl"]
        .sum()
        .reset_index()
        .sort_values(["price_area", "datetime"])
    )

    daily["cum_pnl"] = daily.groupby("price_area")["net_pnl"].cumsum()
    daily["running_max"] = daily.groupby("price_area")["cum_pnl"].cummax()
    daily["drawdown"] = daily["cum_pnl"] - daily["running_max"]

    return daily


def plot_daily_cumulative_pnl(daily):
    plt.figure(figsize=(13, 6))

    for area in daily["price_area"].unique():
        area_df = daily[daily["price_area"] == area]
        plt.plot(area_df["datetime"], area_df["cum_pnl"], linewidth=2, label=area)

    plt.axhline(0, linestyle="--", linewidth=1)
    plt.title("Daily Cumulative PnL")
    plt.xlabel("Date")
    plt.ylabel("Cumulative PnL (€ / MWh)")
    plt.legend(frameon=False)
    plt.grid(alpha=0.3)
    plt.tight_layout()

    output_path = OUTPUT_DIR / "daily_cumulative_pnl.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved: {output_path}")


def plot_daily_drawdown(daily):
    plt.figure(figsize=(13, 5))

    for area in daily["price_area"].unique():
        area_df = daily[daily["price_area"] == area]
        plt.fill_between(
            area_df["datetime"],
            area_df["drawdown"],
            0,
            alpha=0.35,
            label=area
        )
        plt.plot(area_df["datetime"], area_df["drawdown"], linewidth=1.5)

    plt.axhline(0, linestyle="--", linewidth=1)
    plt.title("Daily Drawdown")
    plt.xlabel("Date")
    plt.ylabel("Drawdown (€ / MWh)")
    plt.legend(frameon=False)
    plt.grid(alpha=0.3)
    plt.tight_layout()

    output_path = OUTPUT_DIR / "daily_drawdown.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved: {output_path}")


def main():
    df = load_data()
    daily = build_daily_pnl(df)

    print("Hourly rows:", df.shape)
    print("Daily rows:", daily.shape)

    plot_daily_cumulative_pnl(daily)
    plot_daily_drawdown(daily)

    print("Done.")


if __name__ == "__main__":
    main()