import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from pathlib import Path

from db import connect

BEST_WINDOWS = {
    "DK1": 12,
    "DK2": 12,
}

FEATURES = [
    "hour", "dow", "month", "is_weekend",
    "lag_1", "lag_24", "lag_168",
    "roll_mean_24", "roll_std_24",
    "roll_mean_168", "roll_std_168"
]

OUTPUT_CSV = Path(__file__).resolve().parent.parent / "forecast_next_week_hourly.csv"
OUTPUT_PNG = Path(__file__).resolve().parent.parent / "forecast_next_week_hourly.png"
OUTPUT_TABLE_PNG = Path(__file__).resolve().parent.parent / "table_forecast_summary.png"


def rolling_stats_from_history(hist_values, window):
    s = pd.Series(hist_values[-window:] if len(hist_values) >= window else hist_values)
    mean = float(s.mean())
    std = float(s.std())
    if np.isnan(std):
        std = 0.0
    return mean, std


def build_future_row(ts, hist_values):
    hour = ts.hour
    dow = ts.dayofweek
    month = ts.month
    is_weekend = 1 if dow >= 5 else 0

    lag_1 = hist_values[-1]
    lag_24 = hist_values[-24] if len(hist_values) >= 24 else hist_values[-1]
    lag_168 = hist_values[-168] if len(hist_values) >= 168 else lag_24

    roll_mean_24, roll_std_24 = rolling_stats_from_history(hist_values, 24)
    roll_mean_168, roll_std_168 = rolling_stats_from_history(hist_values, 168)

    return {
        "hour": hour,
        "dow": dow,
        "month": month,
        "is_weekend": is_weekend,
        "lag_1": lag_1,
        "lag_24": lag_24,
        "lag_168": lag_168,
        "roll_mean_24": roll_mean_24,
        "roll_std_24": roll_std_24,
        "roll_mean_168": roll_mean_168,
        "roll_std_168": roll_std_168,
    }


def forecast_area(df_area, area, months, horizon_hours=24 * 7):
    df_area = df_area.copy().sort_values("hour_utc")
    end_date = df_area["hour_utc"].max()
    start_date = end_date - pd.DateOffset(months=months)

    train = df_area[df_area["hour_utc"] >= start_date].copy()
    train = train.dropna(subset=FEATURES + ["y"]).sort_values("hour_utc")

    if train.empty:
        raise ValueError(f"No training data available for {area} with {months} months.")

    X_train = train[FEATURES].to_numpy(dtype=float)
    y_train = train["y"].to_numpy(dtype=float)

    model = Ridge(alpha=1.0)
    model.fit(X_train, y_train)

    history_values = train["y"].tolist()
    last_ts = train["hour_utc"].max()

    future_rows = []
    for h in range(1, horizon_hours + 1):
        ts = last_ts + pd.Timedelta(hours=h)
        x_row = build_future_row(ts, history_values)
        x = np.array([[x_row[c] for c in FEATURES]], dtype=float)
        yhat = float(model.predict(x)[0])

        future_rows.append({
            "hour_utc": ts,
            "price_area": area,
            "pred_spot_price_eur": yhat
        })

        history_values.append(yhat)

    return pd.DataFrame(future_rows)


def build_forecast_summary_table(forecast_df: pd.DataFrame) -> pd.DataFrame:
    summary = []

    for area in ["DK1", "DK2"]:
        d = forecast_df[forecast_df["price_area"] == area].copy()

        mean_price = d["pred_spot_price_eur"].mean()

        lowest = d.loc[d["pred_spot_price_eur"].idxmin()]
        highest = d.loc[d["pred_spot_price_eur"].idxmax()]

        hourly_profile = d.groupby(d["hour_utc"].dt.hour)["pred_spot_price_eur"].mean()

        usual_low = hourly_profile.idxmin()
        usual_high = hourly_profile.idxmax()

        summary.append([
            area,
            round(mean_price, 2),
            round(lowest["pred_spot_price_eur"], 2),
            lowest["hour_utc"].strftime("%Y-%m-%d %H:%M"),
            round(highest["pred_spot_price_eur"], 2),
            highest["hour_utc"].strftime("%Y-%m-%d %H:%M"),
            f"{usual_low:02d}:00",
            f"{usual_high:02d}:00"
        ])

    forecast_table = pd.DataFrame(summary, columns=[
        "Area",
        "Mean €/MWh",
        "Lowest Price",
        "Lowest Time",
        "Highest Price",
        "Highest Time",
        "Lowest Hour",
        "Highest Hour"
    ])

    return forecast_table


def save_forecast_summary_table_png(forecast_table: pd.DataFrame, output_file: Path):
    fig, ax = plt.subplots(figsize=(17, 3.2))
    fig.patch.set_facecolor("#e9e9e9")
    ax.set_facecolor("#e9e9e9")
    ax.axis("off")

    table = ax.table(
        cellText=forecast_table.values,
        colLabels=forecast_table.columns,
        cellLoc="center",
        colLoc="center",
        loc="center"
    )

    table.auto_set_font_size(False)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("black")
        cell.set_linewidth(1.2)
        cell.set_facecolor("#e9e9e9")

        if row == 0:
            cell.set_text_props(weight="bold", fontsize=17, color="black")
            cell.set_height(0.30)
        else:
            cell.set_text_props(fontsize=16, color="black")
            cell.set_height(0.28)

    plt.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.08)
    plt.savefig(output_file, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()


def main():
    con = connect()

    df = con.execute("""
        SELECT *
        FROM features_hourly
        ORDER BY price_area, hour_utc
    """).df()

    con.close()

    if df.empty:
        print("features_hourly is empty.")
        return

    df["hour_utc"] = pd.to_datetime(df["hour_utc"], utc=True)

    forecasts = []

    for area, months in BEST_WINDOWS.items():
        dfa = df[df["price_area"] == area].copy()
        fc = forecast_area(dfa, area=area, months=months, horizon_hours=24 * 7)
        forecasts.append(fc)
        print(f"{area} forecast generated using {months} months.")

    forecast_df = pd.concat(forecasts, ignore_index=True)
    forecast_df["hour_utc"] = pd.to_datetime(forecast_df["hour_utc"], utc=True)
    forecast_df.to_csv(OUTPUT_CSV, index=False)

    plt.figure(figsize=(14, 6))
    for area in ["DK1", "DK2"]:
        d = forecast_df[forecast_df["price_area"] == area].copy()
        plt.plot(d["hour_utc"], d["pred_spot_price_eur"], label=f"{area} forecast")

    plt.title("Next-Week Hourly Electricity Price Forecast")
    plt.xlabel("Datetime (UTC)")
    plt.ylabel("EUR/MWh")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=200)
    plt.close()

    forecast_table = build_forecast_summary_table(forecast_df)
    save_forecast_summary_table_png(forecast_table, OUTPUT_TABLE_PNG)

    print(f"Saved CSV: {OUTPUT_CSV}")
    print(f"Saved plot: {OUTPUT_PNG}")
    print(f"Saved forecast summary table: {OUTPUT_TABLE_PNG}")


if __name__ == "__main__":
    main()