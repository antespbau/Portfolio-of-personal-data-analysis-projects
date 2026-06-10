import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/processed/vlsfo_port_history.csv")
OUTPUT_SUMMARY = Path("data/processed/vlsfo_price_summary_by_port.csv")
OUTPUT_DAILY_RANKING = Path("data/processed/vlsfo_daily_ranking.csv")


def main():
    df = pd.read_csv(INPUT_PATH)

    df["date"] = pd.to_datetime(df["date"])
    df["price_usd_mt"] = pd.to_numeric(df["price_usd_mt"], errors="coerce")

    # Summary by port
    summary = (
        df.groupby("port")["price_usd_mt"]
        .agg(
            avg_price="mean",
            min_price="min",
            max_price="max",
            price_range=lambda x: x.max() - x.min(),
            volatility="std",
            observations="count"
        )
        .reset_index()
        .sort_values("avg_price")
    )

    # Daily ranking: cheapest to most expensive each day
    daily_ranking = df.copy()
    daily_ranking["daily_rank"] = daily_ranking.groupby("date")["price_usd_mt"].rank(
        method="dense",
        ascending=True
    )

    daily_ranking = daily_ranking.sort_values(["date", "daily_rank"])

    OUTPUT_SUMMARY.parent.mkdir(parents=True, exist_ok=True)

    summary.to_csv(OUTPUT_SUMMARY, index=False)
    daily_ranking.to_csv(OUTPUT_DAILY_RANKING, index=False)

    print("Summary by port:")
    print(summary)

    print("\nDaily ranking:")
    print(daily_ranking[["date", "port", "price_usd_mt", "daily_rank"]])

    print(f"\nSaved summary to: {OUTPUT_SUMMARY}")
    print(f"Saved daily ranking to: {OUTPUT_DAILY_RANKING}")


if __name__ == "__main__":
    main()