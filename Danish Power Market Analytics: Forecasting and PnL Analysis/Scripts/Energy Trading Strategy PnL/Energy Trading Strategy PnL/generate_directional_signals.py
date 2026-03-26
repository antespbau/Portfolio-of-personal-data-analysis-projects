from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"

INPUT_PATH = PROCESSED_DIR / "directional_predictions.csv"
OUTPUT_PATH = PROCESSED_DIR / "directional_signals.csv"

UPPER_PROB_THRESHOLD = 0.60
LOWER_PROB_THRESHOLD = 0.40


def main():
    df = pd.read_csv(INPUT_PATH)
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")

    numeric_cols = ["price", "target_change_1", "target_dir_1", "prob_up", "pred_dir"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["datetime", "price_area", "prob_up", "target_change_1"]).copy()
    df = df.sort_values(["price_area", "datetime"]).copy()

    df["signal"] = 0
    df.loc[df["prob_up"] >= UPPER_PROB_THRESHOLD, "signal"] = 1
    df.loc[df["prob_up"] <= LOWER_PROB_THRESHOLD, "signal"] = -1

    df["confidence"] = (df["prob_up"] - 0.5).abs()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved directional signals to: {OUTPUT_PATH}")
    print(df.head())
    print(df["signal"].value_counts(dropna=False))
    print(df.shape)


if __name__ == "__main__":
    main()