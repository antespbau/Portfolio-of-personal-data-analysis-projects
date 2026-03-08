from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor

from improve_helpers import BASE_DIR, PROCESSED_DIR

PNG_DIR = BASE_DIR / "PNG"
PNG_DIR.mkdir(parents=True, exist_ok=True)

MODEL_DATASET_PATH = PROCESSED_DIR / "improve_market_drivers_dataset.csv"
PREDICTIONS_OUTPUT = PROCESSED_DIR / "improve_market_drivers_predictions.csv"
FEATURE_IMPORTANCE_OUTPUT = PNG_DIR / "feature_importance_improve_market_drivers.png"

FEATURE_COLS = [
    "price_lag_1",
    "price_lag_24",
    "price_lag_168",
    "rolling_mean_24",
    "rolling_std_24",
    "temperature_2m",
    "gas_price",
    "wind_generation",
    "load",
    "flow_DE",
    "flow_SE",
    "flow_NO",
    "flow_NL",
    "hour",
    "day_of_week",
    "month",
    "is_weekend",
]

TARGET_COL = "price"
AREAS = ["DK1", "DK2"]


def load_model_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")
    df = df.sort_values(["price_area", "datetime"])

    needed = set(FEATURE_COLS + [TARGET_COL, "price_area", "datetime"])
    missing = needed - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in improved model dataset: {missing}")

    df = df.dropna(subset=FEATURE_COLS + [TARGET_COL, "price_area", "datetime"]).copy()
    return df


def train_test_split_time_series(df: pd.DataFrame, train_ratio: float = 0.8):
    unique_times = np.sort(df["datetime"].unique())
    split_idx = int(len(unique_times) * train_ratio)
    split_time = unique_times[split_idx]

    train_df = df[df["datetime"] < split_time].copy()
    test_df = df[df["datetime"] >= split_time].copy()
    return train_df, test_df


def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> XGBRegressor:
    model = XGBRegressor(
        n_estimators=500,
        learning_rate=0.04,
        max_depth=6,
        min_child_weight=3,
        subsample=0.85,
        colsample_bytree=0.85,
        reg_alpha=0.0,
        reg_lambda=1.0,
        objective="reg:squarederror",
        random_state=42,
    )
    model.fit(X_train, y_train)
    return model


def save_feature_importance(all_importance: pd.DataFrame) -> None:
    avg_importance = (
        all_importance.groupby("feature", as_index=False)["importance"]
        .mean()
        .sort_values("importance", ascending=True)
    )

    plt.figure(figsize=(10, 7))
    plt.barh(avg_importance["feature"], avg_importance["importance"])
    plt.title("Average Feature Importance - Improve Market Drivers")
    plt.xlabel("Importance")
    plt.tight_layout()
    plt.savefig(FEATURE_IMPORTANCE_OUTPUT, dpi=300, bbox_inches="tight")
    plt.close()


def main() -> None:
    df = load_model_data(MODEL_DATASET_PATH)

    all_preds = []
    all_importance = []

    for area in AREAS:
        print(f"\nTraining improved model for {area}...")
        area_df = df[df["price_area"] == area].copy()

        train_df, test_df = train_test_split_time_series(area_df, train_ratio=0.8)

        X_train = train_df[FEATURE_COLS]
        y_train = train_df[TARGET_COL]
        X_test = test_df[FEATURE_COLS]
        y_test = test_df[TARGET_COL]

        model = train_model(X_train, y_train)
        y_pred = model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        print(f"{area} train rows: {len(train_df)}")
        print(f"{area} test rows: {len(test_df)}")
        print(f"{area} MAE: {mae:.4f}")
        print(f"{area} RMSE: {rmse:.4f}")

        out = test_df[["datetime", "price_area", "price"]].copy()
        out["prediction"] = y_pred
        all_preds.append(out)

        importance_df = pd.DataFrame(
            {
                "feature": FEATURE_COLS,
                "importance": model.feature_importances_,
                "price_area": area,
            }
        )
        all_importance.append(importance_df)

        plot_df = out.tail(24 * 7)

        plt.figure(figsize=(14, 6))
        plt.plot(plot_df["datetime"], plot_df["price"], label=f"Actual {area}")
        plt.plot(plot_df["datetime"], plot_df["prediction"], label=f"Predicted {area}")
        plt.title(f"Actual vs Predicted - Improve Market Drivers - {area}")
        plt.xlabel("Datetime")
        plt.ylabel("Price EUR/MWh")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(
            PNG_DIR / f"actual_vs_predicted_improve_market_drivers_{area}.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.close()

    preds_df = pd.concat(all_preds, ignore_index=True)
    preds_df.to_csv(PREDICTIONS_OUTPUT, index=False)

    importance_all_df = pd.concat(all_importance, ignore_index=True)
    save_feature_importance(importance_all_df)

    print(f"\nSaved predictions to: {PREDICTIONS_OUTPUT}")
    print(f"Saved feature importance plot to: {FEATURE_IMPORTANCE_OUTPUT}")


if __name__ == "__main__":
    main()