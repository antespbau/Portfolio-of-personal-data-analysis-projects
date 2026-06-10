import re
from datetime import datetime
from io import StringIO
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup


PORT_URLS = {
    "Singapore": "https://shipandbunker.com/prices/apac/sea/sg-sin-singapore",
    "Rotterdam": "https://shipandbunker.com/prices/emea/nwe/nl-rtm-rotterdam",
    "Houston": "https://shipandbunker.com/prices/am/usgac/us-hou-houston",
    "Fujairah": "https://shipandbunker.com/prices/emea/me/ae-fjr-fujairah",
    "Gibraltar": "https://shipandbunker.com/prices/emea/medabs/gi-gib-gibraltar",
}

OUTPUT_PATH = Path("data/raw/shipandbunker_port_history.csv")


def normalize_date(date_text: str, year: int = 2026) -> str:
    """
    Converts dates like:
    M Jun 8
    F Jun 5
    T Jun 4
    into:
    2026-06-08
    """
    date_text = str(date_text).strip()

    # Remove weekday letter at the beginning
    # Example: "M Jun 8" -> "Jun 8"
    parts = date_text.split()
    if len(parts) == 3:
        date_text = f"{parts[1]} {parts[2]} {year}"
    elif len(parts) == 2:
        date_text = f"{parts[0]} {parts[1]} {year}"

    parsed = pd.to_datetime(date_text, errors="coerce")

    if pd.isna(parsed):
        return None

    return parsed.strftime("%Y-%m-%d")


def clean_numeric(value):
    if pd.isna(value):
        return None

    text = str(value)
    text = text.replace("+", "")
    text = text.replace(",", "")
    text = re.sub(r"[^0-9.\-]", "", text)

    if text == "":
        return None

    return float(text)


def scrape_one_port(port_name: str, url: str) -> pd.DataFrame:
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    html = response.text

    # This reads all HTML tables on the page
    tables = pd.read_html(StringIO(html))

    valid_tables = []

    for table in tables:
        cols = [str(c).lower() for c in table.columns]
        table_text = table.to_string().lower()

        if "price" in table_text and "spread" in table_text and "change" in table_text:
            valid_tables.append(table)

    if not valid_tables:
        print(f"No historical price table found for {port_name}")
        return pd.DataFrame()

    all_rows = []

    # Usually the first table is VLSFO, then MGO, then IFO380
    fuel_order = ["VLSFO", "MGO", "IFO380"]

    for idx, table in enumerate(valid_tables[:3]):
        fuel_type = fuel_order[idx]

        table.columns = [str(c).strip() for c in table.columns]

        # Try to standardise columns
        rename_map = {}
        for col in table.columns:
            low = col.lower()
            if "date" in low:
                rename_map[col] = "date"
            elif "price" in low:
                rename_map[col] = "price_usd_mt"
            elif "change" in low:
                rename_map[col] = "change_usd_mt"
            elif "high" in low:
                rename_map[col] = "high_usd_mt"
            elif "low" in low:
                rename_map[col] = "low_usd_mt"
            elif "spread" in low:
                rename_map[col] = "spread_usd_mt"

        table = table.rename(columns=rename_map)

        needed = ["date", "price_usd_mt", "change_usd_mt", "high_usd_mt", "low_usd_mt", "spread_usd_mt"]
        missing = [c for c in needed if c not in table.columns]

        if missing:
            print(f"Skipping table for {port_name} {fuel_type}. Missing: {missing}")
            continue

        table = table[needed].copy()

        table["date"] = table["date"].apply(normalize_date)
        table["port"] = port_name
        table["fuel_type"] = fuel_type
        table["source"] = "Ship & Bunker"
        table["url"] = url
        table["scraped_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for col in ["price_usd_mt", "change_usd_mt", "high_usd_mt", "low_usd_mt", "spread_usd_mt"]:
            table[col] = table[col].apply(clean_numeric)

        table = table.dropna(subset=["date", "price_usd_mt"])

        all_rows.append(table)

    if not all_rows:
        return pd.DataFrame()

    return pd.concat(all_rows, ignore_index=True)


def main():
    all_ports = []

    for port, url in PORT_URLS.items():
        print(f"Scraping {port}...")
        df_port = scrape_one_port(port, url)

        if not df_port.empty:
            all_ports.append(df_port)

    if not all_ports:
        raise ValueError("No data scraped from any port.")

    result = pd.concat(all_ports, ignore_index=True)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.head(30))
    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()