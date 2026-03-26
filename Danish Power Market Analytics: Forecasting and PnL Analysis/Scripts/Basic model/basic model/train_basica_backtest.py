from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"

MODEL_DATASET_PATH = PROCESSED_DIR / "model_dataset.csv"
OUTPUT_PATH = PROCESSED_DIR / "basic_model_predictions.csv"

FEATURE_COLS = [
    "price_lag_1",
    "price_lag_24",
    "price_lag_168",
    "rolling_mean_24",
    "rolling_std_24",
    "hour",
    "day_of_week",
    "month",
    "is_weekend",
]

TARGET_COL = "price"
AREAS = ["DK1", "DK2"]


def load_data() -> pd.DataFrame:
    df = pd.read_csv(MODEL_DATASET_PATH)
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")
    df = df.sort_values(["price_area", "datetime"]).copy()

    needed = FEATURE_COLS + [TARGET_COL, "price_area", "datetime"]
    df = df.dropna(subset=needed).copy()
    return df


def train_test_split_time_series(df: pd.DataFrame, train_ratio: float = 0.8):
    unique_times = np.sort(df["datetime"].unique())
    split_idx = int(len(unique_times) * train_ratio)
    split_time = unique_times[split_idx]

    train_df = df[df["datetime"] < split_time].copy()
    test_df = df[df["datetime"] >= split_time].copy()

    return train_df, test_df


def main():
    df = load_data()
    outputs = []

    for area in AREAS:
        print(f"\nTraining basic backtest for {area}...")

        area_df = df[df["price_area"] == area].copy()
        train_df, test_df = train_test_split_time_series(area_df, train_ratio=0.8)

        X_train = train_df[FEATURE_COLS]
        y_train = train_df[TARGET_COL]

        X_test = test_df[FEATURE_COLS]
        y_test = test_df[TARGET_COL]

        model = Ridge(alpha=1.0)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        print(f"{area} MAE: {mae:.4f}")
        print(f"{area} RMSE: {rmse:.4f}")

        out = test_df[["datetime", "price_area", "price"]].copy()
        out["prediction"] = y_pred
        outputs.append(out)

    final_df = pd.concat(outputs, ignore_index=True)
    final_df.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSaved basic model backtest predictions to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()