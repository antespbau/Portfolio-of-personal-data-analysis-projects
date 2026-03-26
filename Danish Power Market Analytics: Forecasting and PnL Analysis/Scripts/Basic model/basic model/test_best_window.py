import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from db import connect

WINDOWS = [36, 24, 12, 9, 6, 3]
TEST_DAYS = 7

FEATURES = [
    "hour", "dow", "month", "is_weekend",
    "lag_1", "lag_24", "lag_168",
    "roll_mean_24", "roll_std_24",
    "roll_mean_168", "roll_std_168"
]

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_CSV = BASE_DIR / "window_results.csv"
OUTPUT_PNG = BASE_DIR / "window_results_plot.png"


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

    all_results = []

    for area in ["DK1", "DK2"]:
        print(f"\nAREA: {area}")
        dfa = df[df["price_area"] == area].copy()

        results = []

        for months in WINDOWS:
            end_date = dfa["hour_utc"].max()
            start_date = end_date - pd.DateOffset(months=months)

            data = dfa[dfa["hour_utc"] >= start_date].copy()
            data = data.dropna(subset=FEATURES + ["y"]).sort_values("hour_utc")

            cut = end_date - pd.Timedelta(days=TEST_DAYS)
            train = data[data["hour_utc"] < cut].copy()
            test = data[data["hour_utc"] >= cut].copy()

            if len(train) < 200 or len(test) < 24:
                print(f"{months} months -> skipped")
                continue

            X_train = train[FEATURES].to_numpy(dtype=float)
            y_train = train["y"].to_numpy(dtype=float)
            X_test = test[FEATURES].to_numpy(dtype=float)
            y_test = test["y"].to_numpy(dtype=float)

            model = Ridge(alpha=1.0)
            model.fit(X_train, y_train)
            preds = model.predict(X_test)

            mae = mean_absolute_error(y_test, preds)
            rmse = np.sqrt(mean_squared_error(y_test, preds))

            results.append((months, mae, rmse))
            all_results.append({
                "Area": area,
                "WindowMonths": months,
                "MAE": round(mae, 4),
                "RMSE": round(rmse, 4),
                "Best": ""
            })

            print(f"{months} months -> MAE={mae:.2f} RMSE={rmse:.2f}")

        if results:
            best = min(results, key=lambda x: x[2])
            print(f"BEST {area}: {best[0]} months | RMSE={best[2]:.2f}")

    results_df = pd.DataFrame(all_results)

    if results_df.empty:
        print("No valid results to save or plot.")
        return

    # Mark best window per area
    best_idx = results_df.groupby("Area")["RMSE"].idxmin()
    results_df.loc[best_idx, "Best"] = "✔"

    # Save CSV
    results_df.to_csv(OUTPUT_CSV, index=False)
    print(f"\nSaved CSV: {OUTPUT_CSV}")

    # Plot
    plt.figure(figsize=(12, 6))

    for area in ["DK1", "DK2"]:
        d = results_df[results_df["Area"] == area].sort_values("WindowMonths", ascending=False)
        plt.plot(
            d["WindowMonths"],
            d["RMSE"],
            marker="o",
            linewidth=2,
            label=f"{area} RMSE"
        )

    plt.gca().invert_xaxis()  # so 36 -> 3 reads left to right
    plt.title("RMSE by Training Window")
    plt.xlabel("Training Window (Months)")
    plt.ylabel("RMSE")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=300)
    plt.close()

    print(f"Saved plot: {OUTPUT_PNG}")


if __name__ == "__main__":
    main()