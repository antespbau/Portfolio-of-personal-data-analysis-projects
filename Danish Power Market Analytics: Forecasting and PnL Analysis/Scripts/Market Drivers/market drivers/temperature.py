from pathlib import Path
from datetime import date, timedelta
import requests
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

START_DATE = "2023-01-01"
END_DATE = (date.today() - timedelta(days=1)).isoformat()

# Copenhagen coordinates
LATITUDE = 55.6761
LONGITUDE = 12.5683

URL = "https://archive-api.open-meteo.com/v1/archive"


def fetch_temperature(start_date: str, end_date: str) -> pd.DataFrame:
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m",
        "timezone": "Europe/Copenhagen",
    }

    response = requests.get(URL, params=params, timeout=60)
    response.raise_for_status()
    data = response.json()

    if "hourly" not in data or "time" not in data["hourly"]:
        raise ValueError("Unexpected response from Open-Meteo API.")

    df = pd.DataFrame(
        {
            "datetime": pd.to_datetime(data["hourly"]["time"]),
            "temperature_2m": data["hourly"]["temperature_2m"],
        }
    )

    return df


def main() -> None:
    df = fetch_temperature(START_DATE, END_DATE)
    output_path = RAW_DIR / "temperature_hourly.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved temperature data to: {output_path}")
    print(df.head())
    print(df.tail())
    print(df.shape)


if __name__ == "__main__":
    main()