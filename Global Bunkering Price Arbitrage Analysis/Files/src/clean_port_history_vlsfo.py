import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/raw/shipandbunker_port_history.csv")
OUTPUT_PATH = Path("data/processed/vlsfo_port_history.csv")


def main():
    df = pd.read_csv(INPUT_PATH)

    # Keep only VLSFO
    vlsfo = df[df["fuel_type"] == "VLSFO"].copy()

    # Convert date and price
    vlsfo["date"] = pd.to_datetime(vlsfo["date"], errors="coerce")
    vlsfo["price_usd_mt"] = pd.to_numeric(vlsfo["price_usd_mt"], errors="coerce")

    # Remove bad rows
    vlsfo = vlsfo.dropna(subset=["date", "port", "price_usd_mt"])

    # Remove duplicates
    vlsfo = vlsfo.drop_duplicates(
        subset=["date", "port", "fuel_type"],
        keep="last"
    )

    # Sort properly
    vlsfo = vlsfo.sort_values(["port", "date"])

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    vlsfo.to_csv(OUTPUT_PATH, index=False)

    print("Clean VLSFO historical port dataset:")
    print(vlsfo)

    print("\nRows:", len(vlsfo))
    print("Ports:", vlsfo["port"].unique())
    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()