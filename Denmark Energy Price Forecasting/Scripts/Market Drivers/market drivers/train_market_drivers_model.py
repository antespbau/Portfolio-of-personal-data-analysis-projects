from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PNG_DIR = BASE_DIR / "PNG"

PNG_DIR.mkdir(parents=True, exist_ok=True)

MODEL_DATASET_PATH = PROCESSED_DIR / "model_dataset.csv"
PREDICTIONS_OUTPUT = PROCESSED_DIR / "market_drivers_predictions.csv"

FEATURE_IMPORTANCE_PNG = PNG_DIR / "feature_importance_market_drivers.png"
FEATURE_IMPORTANCE_HEATMAP_PNG = PNG_DIR / "feature_importance_heatmap_market_drivers.png"

FEATURE_COLS = [
    "price_lag_1",
    "price_lag_24",
    "price_lag_168",
    "rolling_mean_24",
    "rolling_std_24",
    "temperature_2m",
    "gas_price",
    "wind_generation",
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
        raise ValueError(f"Missing columns in model dataset: {missing}")

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
        n_estimators=400,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="reg:squarederror",
        random_state=42,
    )
    model.fit(X_train, y_train)
    return model


def save_feature_importance(all_importance: pd.DataFrame):
    avg_importance = (
        all_importance.groupby("feature", as_index=False)["importance"]
        .mean()
        .sort_values("importance", ascending=False)
    )

    plot_df = avg_importance.sort_values("importance", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(plot_df["feature"], plot_df["importance"])
    plt.title("Average Feature Importance - Market Drivers Models")
    plt.xlabel("Importance")
    plt.tight_layout()
    plt.savefig(FEATURE_IMPORTANCE_PNG, dpi=300, bbox_inches="tight")
    plt.close()

    heatmap_df = avg_importance.set_index("feature")[["importance"]]
    plt.figure(figsize=(8, 5))
    sns.heatmap(
        heatmap_df,
        annot=True,
        fmt=".3f",
        cmap="YlGnBu",
        linewidths=0.5,
        cbar=True
    )
    plt.title("Average Market Drivers Importance Heatmap")
    plt.tight_layout()
    plt.savefig(FEATURE_IMPORTANCE_HEATMAP_PNG, dpi=300, bbox_inches="tight")
    plt.close()


def main():
    df = load_model_data(MODEL_DATASET_PATH)

    all_preds = []
    all_importance = []

    for area in AREAS:
        print(f"\nTraining model for {area}...")
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

        importance_df = pd.DataFrame({
            "feature": FEATURE_COLS,
            "importance": model.feature_importances_,
            "price_area": area
        })
        all_importance.append(importance_df)

        plot_df = out.tail(24 * 7)

        plt.figure(figsize=(14, 6))
        plt.plot(plot_df["datetime"], plot_df["price"], label=f"Actual {area}")
        plt.plot(plot_df["datetime"], plot_df["prediction"], label=f"Predicted {area}")
        plt.title(f"Actual vs Predicted Electricity Prices - {area}")
        plt.xlabel("Datetime")
        plt.ylabel("Price")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(PNG_DIR / f"actual_vs_predicted_market_drivers_{area}.png", dpi=300, bbox_inches="tight")
        plt.close()

    preds_df = pd.concat(all_preds, ignore_index=True)
    preds_df.to_csv(PREDICTIONS_OUTPUT, index=False)

    importance_all_df = pd.concat(all_importance, ignore_index=True)
    save_feature_importance(importance_all_df)

    print(f"\nSaved predictions to: {PREDICTIONS_OUTPUT}")
    print(f"Saved feature importance plot to: {FEATURE_IMPORTANCE_PNG}")
    print(f"Saved feature importance heatmap to: {FEATURE_IMPORTANCE_HEATMAP_PNG}")


if __name__ == "__main__":
    main()