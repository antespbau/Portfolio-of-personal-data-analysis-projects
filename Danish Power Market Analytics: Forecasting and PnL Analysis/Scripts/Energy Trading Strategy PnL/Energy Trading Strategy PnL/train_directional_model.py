from pathlib import Path
import json
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
MODELS_DIR = BASE_DIR / "models" / "trained"

INPUT_PATH = PROCESSED_DIR / "directional_dataset.csv"
PREDICTIONS_PATH = PROCESSED_DIR / "directional_predictions.csv"
METRICS_PATH = PROCESSED_DIR / "directional_metrics.csv"

MODELS_DIR.mkdir(parents=True, exist_ok=True)

FEATURE_COLS = [
    # Original price-level features
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
    # New directional features
    "price_change_1",
    "price_change_24",
    "price_change_168",
    "temp_change_1",
    "temp_change_24",
    "wind_change_1",
    "wind_change_24",
    "gas_change_24",
    "spread_dk1_dk2",
    "spread_lag_1",
    "spread_lag_24",
    "spread_change_1",
    "spread_change_24",
]

TARGET_COL = "target_dir_1"
AREAS = ["DK1", "DK2"]


def train_test_split_time_series(df: pd.DataFrame, train_ratio: float = 0.8):
    unique_times = np.sort(df["datetime"].unique())
    split_idx = int(len(unique_times) * train_ratio)
    split_time = unique_times[split_idx]

    train_df = df[df["datetime"] < split_time].copy()
    test_df = df[df["datetime"] >= split_time].copy()
    return train_df, test_df, split_time


def build_model() -> XGBClassifier:
    return XGBClassifier(
        n_estimators=400,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="binary:logistic",
        eval_metric="logloss",
        random_state=42,
    )


def safe_auc(y_true, y_prob):
    if len(pd.Series(y_true).dropna().unique()) < 2:
        return np.nan
    return roc_auc_score(y_true, y_prob)


def main():
    df = pd.read_csv(INPUT_PATH)
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")

    needed = set(FEATURE_COLS + [TARGET_COL, "datetime", "price_area", "price", "target_change_1"])
    missing = needed - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in directional dataset: {missing}")

    for col in FEATURE_COLS + [TARGET_COL, "price", "target_change_1"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=FEATURE_COLS + [TARGET_COL, "datetime", "price_area", "price", "target_change_1"]).copy()

    all_predictions = []
    all_metrics = []

    for area in AREAS:
        print(f"\nTraining directional model for {area}...")
        area_df = df[df["price_area"] == area].copy().sort_values("datetime")

        train_df, test_df, split_time = train_test_split_time_series(area_df, train_ratio=0.8)

        X_train = train_df[FEATURE_COLS]
        y_train = train_df[TARGET_COL].astype(int)

        X_test = test_df[FEATURE_COLS]
        y_test = test_df[TARGET_COL].astype(int)

        model = build_model()
        model.fit(X_train, y_train)

        prob_up = model.predict_proba(X_test)[:, 1]
        pred_dir = (prob_up >= 0.5).astype(int)

        metrics = {
            "price_area": area,
            "split_time": str(split_time),
            "train_rows": len(train_df),
            "test_rows": len(test_df),
            "accuracy": accuracy_score(y_test, pred_dir),
            "precision": precision_score(y_test, pred_dir, zero_division=0),
            "recall": recall_score(y_test, pred_dir, zero_division=0),
            "f1": f1_score(y_test, pred_dir, zero_division=0),
            "auc": safe_auc(y_test, prob_up),
        }
        all_metrics.append(metrics)

        print(json.dumps(metrics, indent=2))

        preds = test_df[
            ["datetime", "price_area", "price", "target_change_1", "target_dir_1"]
        ].copy()
        preds["prob_up"] = prob_up
        preds["pred_dir"] = pred_dir

        all_predictions.append(preds)

        model_path = MODELS_DIR / f"directional_xgb_{area}.joblib"
        joblib.dump(model, model_path)
        print(f"Saved model to: {model_path}")

    pred_df = pd.concat(all_predictions, ignore_index=True)
    pred_df.to_csv(PREDICTIONS_PATH, index=False)

    metrics_df = pd.DataFrame(all_metrics)
    metrics_df.to_csv(METRICS_PATH, index=False)

    print(f"\nSaved predictions to: {PREDICTIONS_PATH}")
    print(f"Saved metrics to: {METRICS_PATH}")


if __name__ == "__main__":
    main()