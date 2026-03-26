import duckdb
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "energy.duckdb"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "dk1_dk2_price_evolution.png"

def main():
    con = duckdb.connect(str(DB_PATH))

    df = con.execute("""
        SELECT hour_utc, price_area, spot_price_eur
        FROM actuals
        WHERE price_area IN ('DK1', 'DK2')
        ORDER BY hour_utc, price_area
    """).df()

    con.close()

    if df.empty:
        print("No data found in actuals table.")
        return

    df["hour_utc"] = pd.to_datetime(df["hour_utc"], utc=True)

    # Pivot so we get one column for DK1 and one for DK2
    wide = (
        df.pivot(index="hour_utc", columns="price_area", values="spot_price_eur")
          .sort_index()
    )

    # Daily average to make the chart much cleaner
    daily = wide.resample("D").mean()

    plt.figure(figsize=(14, 6))
    plt.plot(daily.index, daily["DK1"], label="DK1")
    plt.plot(daily.index, daily["DK2"], label="DK2")

    plt.title("DK1 vs DK2 Daily Average Spot Price Evolution")
    plt.xlabel("Date")
    plt.ylabel("EUR/MWh")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=200)
    plt.close()

    print(f"Saved chart to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()