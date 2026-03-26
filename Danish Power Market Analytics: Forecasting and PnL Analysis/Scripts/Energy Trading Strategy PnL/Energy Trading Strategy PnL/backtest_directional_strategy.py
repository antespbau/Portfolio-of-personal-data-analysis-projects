from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"

INPUT_PATH = PROCESSED_DIR / "directional_signals.csv"
RESULTS_PATH = PROCESSED_DIR / "directional_backtest_results.csv"
SUMMARY_PATH = PROCESSED_DIR / "directional_backtest_summary.csv"

TRANSACTION_COST = 3.0


def max_drawdown(series: pd.Series) -> float:
    running_max = series.cummax()
    drawdown = series - running_max
    return float(drawdown.min())


def main():
    df = pd.read_csv(INPUT_PATH)
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")

    numeric_cols = ["signal", "target_change_1", "prob_up", "confidence"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["datetime", "price_area", "signal", "target_change_1"]).copy()
    df = df.sort_values(["price_area", "datetime"]).copy()

    # Actual next-hour movement
    df["pnl"] = df["signal"] * df["target_change_1"]
    df["net_pnl"] = df["pnl"] - (df["signal"].abs() * TRANSACTION_COST)
    df["cum_pnl"] = df.groupby("price_area")["net_pnl"].cumsum()

    trades = df[df["signal"] != 0].copy()

    summary = trades.groupby("price_area").agg(
        total_pnl=("net_pnl", "sum"),
        avg_trade_pnl=("net_pnl", "mean"),
        n_trades=("signal", "count"),
        win_rate=("net_pnl", lambda x: float((x > 0).mean())),
        pnl_std=("net_pnl", "std"),
    )

    summary["sharpe_like"] = summary["avg_trade_pnl"] / summary["pnl_std"].replace(0, np.nan)
    summary["max_drawdown"] = trades.groupby("price_area")["cum_pnl"].apply(max_drawdown)

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(RESULTS_PATH, index=False)
    summary.to_csv(SUMMARY_PATH)

    print(f"Saved results to: {RESULTS_PATH}")
    print(f"Saved summary to: {SUMMARY_PATH}")
    print("\nStrategy summary:\n")
    print(summary.round(4))


if __name__ == "__main__":
    main()

    