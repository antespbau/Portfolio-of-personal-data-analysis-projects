from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PNG_DIR = BASE_DIR / "PNG"

DATA_PATH = PROCESSED_DIR / "improve_market_drivers_dataset.csv"

FEATURES = [
    "price_lag_1",
    "price_lag_24",
    "price_lag_168",
    "rolling_mean_24",
    "rolling_std_24",
    "wind_generation",
    "flow_NO",
    "flow_DE",
    "flow_SE",
    "load",
    "hour",
    "day_of_week",
    "is_weekend"
]

TARGET = "price"

AREAS = ["DK1","DK2"]


def train_test_split(df, ratio=0.8):

    unique_times = np.sort(df["datetime"].unique())
    split_idx = int(len(unique_times)*ratio)
    split_time = unique_times[split_idx]

    train = df[df["datetime"] < split_time]
    test = df[df["datetime"] >= split_time]

    return train,test


def main():

    df = pd.read_csv(DATA_PATH)
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True)

    df = df.dropna(subset=FEATURES + [TARGET,"price_area"])

    for area in AREAS:

        print(f"\n===== {area} =====")

        area_df = df[df["price_area"]==area].copy()

        train,test = train_test_split(area_df)

        X_train = train[FEATURES]
        y_train = train[TARGET]

        X_test = test[FEATURES]
        y_test = test[TARGET]

        model = XGBRegressor(
            n_estimators=400,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42
        )

        model.fit(X_train,y_train)

        preds = model.predict(X_test)

        mae = mean_absolute_error(y_test,preds)
        rmse = np.sqrt(mean_squared_error(y_test,preds))

        print("MAE:",round(mae,3))
        print("RMSE:",round(rmse,3))

        plot_df = test.copy()
        plot_df["prediction"] = preds
        plot_df = plot_df.tail(24*7)

        plt.figure(figsize=(14,6))

        plt.plot(
            plot_df["datetime"],
            plot_df["price"],
            label="Actual"
        )

        plt.plot(
            plot_df["datetime"],
            plot_df["prediction"],
            label="Predicted"
        )

        plt.title(f"Actual vs Predicted Prices ({area})")
        plt.xlabel("Datetime")
        plt.ylabel("Price EUR/MWh")
        plt.legend()

        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.savefig(
            PNG_DIR / f"reduced_model_actual_vs_predicted_{area}.png",
            dpi=300
        )

        plt.close()


if __name__ == "__main__":
    main()