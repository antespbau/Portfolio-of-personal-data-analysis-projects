import pandas as pd
from db import connect, init_db

PRICE_AREAS = ["DK1", "DK2"]

def build_features():
    init_db()
    con = connect()

    df = con.execute("""
        SELECT hour_utc, price_area, spot_price_eur
        FROM actuals
        ORDER BY price_area, hour_utc
    """).df()

    if df.empty:
        print("No data in actuals.")
        con.close()
        return

    df["hour_utc"] = pd.to_datetime(df["hour_utc"], utc=True)
    df["spot_price_eur"] = pd.to_numeric(df["spot_price_eur"], errors="coerce")
    df = df.dropna(subset=["hour_utc", "price_area", "spot_price_eur"])

    all_frames = []

    for area in PRICE_AREAS:
        d = df[df["price_area"] == area].copy().sort_values("hour_utc")
        d = d.rename(columns={"spot_price_eur": "y"})

        d["hour"] = d["hour_utc"].dt.hour
        d["dow"] = d["hour_utc"].dt.dayofweek
        d["month"] = d["hour_utc"].dt.month
        d["is_weekend"] = (d["dow"] >= 5).astype(int)

        d["lag_1"] = d["y"].shift(1)
        d["lag_24"] = d["y"].shift(24)
        d["lag_168"] = d["y"].shift(168)

        d["roll_mean_24"] = d["y"].shift(1).rolling(24).mean()
        d["roll_std_24"] = d["y"].shift(1).rolling(24).std()
        d["roll_mean_168"] = d["y"].shift(1).rolling(168).mean()
        d["roll_std_168"] = d["y"].shift(1).rolling(168).std()

        d = d.dropna(subset=[
            "lag_1", "lag_24", "lag_168",
            "roll_mean_24", "roll_std_24",
            "roll_mean_168", "roll_std_168"
        ])

        all_frames.append(d)

    feats = pd.concat(all_frames, ignore_index=True)

    con.execute("DELETE FROM features_hourly")
    con.register("feats_in", feats[[
        "hour_utc", "price_area", "y",
        "hour", "dow", "month", "is_weekend",
        "lag_1", "lag_24", "lag_168",
        "roll_mean_24", "roll_std_24",
        "roll_mean_168", "roll_std_168"
    ]])

    con.execute("""
        INSERT INTO features_hourly
        SELECT * FROM feats_in
    """)

    print(con.execute("""
        SELECT price_area, COUNT(*) AS rows, MIN(hour_utc), MAX(hour_utc)
        FROM features_hourly
        GROUP BY price_area
    """).fetchdf())

    con.close()

if __name__ == "__main__":
    build_features()