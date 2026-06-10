import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/processed/vlsfo_port_history.csv")
OUTPUT_PATH = Path("data/processed/vlsfo_price_spreads.csv")


def main():
    df = pd.read_csv(INPUT_PATH)

    df["date"] = pd.to_datetime(df["date"])
    df["price_usd_mt"] = pd.to_numeric(df["price_usd_mt"], errors="coerce")

    results = []

    for date, day_data in df.groupby("date"):
        ports = day_data[["port", "price_usd_mt"]].dropna()

        for _, expensive in ports.iterrows():
            for _, cheap in ports.iterrows():

                if expensive["port"] == cheap["port"]:
                    continue

                spread = expensive["price_usd_mt"] - cheap["price_usd_mt"]

                if spread <= 0:
                    continue

                results.append({
                    "date": date,
                    "expensive_port": expensive["port"],
                    "cheap_port": cheap["port"],
                    "expensive_price_usd_mt": expensive["price_usd_mt"],
                    "cheap_price_usd_mt": cheap["price_usd_mt"],
                    "spread_usd_mt": spread,
                    "theoretical_saving_1000mt_usd": spread * 1000,
                })

    spreads = pd.DataFrame(results)

    spreads = spreads.sort_values(
        ["date", "spread_usd_mt"],
        ascending=[True, False]
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    spreads.to_csv(OUTPUT_PATH, index=False)

    print("Top price spreads:")
    print(spreads.head(30))

    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()