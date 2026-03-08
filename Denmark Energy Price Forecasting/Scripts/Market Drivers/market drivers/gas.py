from pathlib import Path
from datetime import date, timedelta
import pandas as pd
import yfinance as yf


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

START_DATE = "2023-01-01"
END_DATE = (date.today() - timedelta(days=1)).isoformat()

# Natural gas futures proxy
TICKER = "NG=F"


def fetch_gas_prices(start_date: str, end_date: str) -> pd.DataFrame:
    gas = yf.download(
        TICKER,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
    )

    if gas.empty:
        raise ValueError("No gas price data was returned from yfinance.")

    df = gas.reset_index()[["Date", "Close"]].rename(
        columns={"Date": "date", "Close": "gas_price"}
    )

    df["date"] = pd.to_datetime(df["date"]).dt.date
    return df


def main() -> None:
    df = fetch_gas_prices(START_DATE, END_DATE)
    output_path = RAW_DIR / "gas_daily.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved gas data to: {output_path}")
    print(df.head())
    print(df.tail())
    print(df.shape)


if __name__ == "__main__":
    main()