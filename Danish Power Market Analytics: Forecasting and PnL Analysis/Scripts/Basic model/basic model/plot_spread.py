import duckdb
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "energy.duckdb"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "dk_spread_evolution.png"

def main():

    con = duckdb.connect(str(DB_PATH))

    df = con.execute("""
        SELECT hour_utc, price_area, spot_price_eur
        FROM actuals
        WHERE price_area IN ('DK1','DK2')
        ORDER BY hour_utc
    """).df()

    con.close()

    df["hour_utc"] = pd.to_datetime(df["hour_utc"], utc=True)

    # reshape to wide format
    wide = df.pivot(index="hour_utc", columns="price_area", values="spot_price_eur")

    # compute spread
    wide["spread"] = wide["DK2"] - wide["DK1"]

    # daily average to smooth noise
    daily = wide.resample("D").mean()

    plt.figure(figsize=(14,6))

    plt.plot(daily.index, daily["spread"])

    plt.axhline(0)

    plt.title("DK2 − DK1 Price Spread (Daily Average)")
    plt.xlabel("Date")
    plt.ylabel("EUR/MWh")

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=200)

    print("Spread chart saved:", OUTPUT_PATH)


if __name__ == "__main__":
    main()