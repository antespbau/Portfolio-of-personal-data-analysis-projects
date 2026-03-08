import json
import requests
import pandas as pd
from datetime import datetime, timezone, timedelta
from pathlib import Path
import duckdb

# =========================
# CONFIG
# =========================
DB_FILE = Path(__file__).resolve().parent.parent / "energy.duckdb"

PRICE_AREAS = ["DK1", "DK2"]

START_DATE_UTC = datetime(2023, 3, 5, 0, 0, tzinfo=timezone.utc)
END_DATE_UTC = datetime.now(timezone.utc)

SWITCH_TO_DAYAHEAD_UTC = datetime(2025, 10, 1, 0, 0, tzinfo=timezone.utc)

WINDOW_DAYS = 14

BASE_URL = "https://api.energidataservice.dk/dataset"
ELSPOT_DATASET = "Elspotprices"
DAYAHEAD_DATASET = "DayAheadPrices"

DK_TZ = "Europe/Copenhagen"


# =========================
# DB
# =========================
def connect():
    return duckdb.connect(str(DB_FILE))


def init_db():
    con = connect()
    con.execute("""
        CREATE TABLE IF NOT EXISTS actuals (
            hour_utc TIMESTAMPTZ,
            price_area VARCHAR,
            spot_price_eur DOUBLE,
            PRIMARY KEY (hour_utc, price_area)
        )
    """)
    con.close()


def get_latest_hour_utc(con):
    row = con.execute("SELECT MAX(hour_utc) FROM actuals").fetchone()
    return row[0]


def upsert_actuals(con, df: pd.DataFrame) -> int:
    if df.empty:
        return 0

    df = df.copy()
    df["hour_utc"] = pd.to_datetime(df["hour_utc"], utc=True, errors="coerce")
    df["price_area"] = df["price_area"].astype(str)
    df["spot_price_eur"] = pd.to_numeric(df["spot_price_eur"], errors="coerce")

    df = df.dropna(subset=["hour_utc", "price_area", "spot_price_eur"])
    df = df[df["price_area"].isin(PRICE_AREAS)]

    df = (
        df.groupby(["hour_utc", "price_area"], as_index=False)["spot_price_eur"]
        .mean()
    )

    con.register("incoming_actuals", df)
    con.execute("""
        INSERT OR REPLACE INTO actuals
        SELECT hour_utc, price_area, spot_price_eur
        FROM incoming_actuals
    """)

    return len(df)


# =========================
# API FETCH
# =========================
def fetch_eds(dataset: str, start_utc: datetime, end_utc: datetime) -> pd.DataFrame:
    url = f"{BASE_URL}/{dataset}"

    sort_field = "HourUTC asc" if dataset == ELSPOT_DATASET else "TimeDK asc"

    params = {
        "start": start_utc.strftime("%Y-%m-%dT%H:%M"),
        "end": end_utc.strftime("%Y-%m-%dT%H:%M"),
        "filter": json.dumps({"PriceArea": PRICE_AREAS}),
        "sort": sort_field,
        "limit": 10000,
    }

    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()

    records = r.json().get("records", [])
    return pd.DataFrame(records)


# =========================
# PARSERS
# =========================
def parse_elspot_to_hourly_utc(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["hour_utc", "price_area", "spot_price_eur"])

    if "HourUTC" in df.columns:
        out = df[["HourUTC", "PriceArea", "SpotPriceEUR"]].copy()
        out.rename(columns={
            "HourUTC": "hour_utc",
            "PriceArea": "price_area",
            "SpotPriceEUR": "spot_price_eur"
        }, inplace=True)

        out["hour_utc"] = pd.to_datetime(out["hour_utc"], utc=True, errors="coerce").dt.floor("h")
        out["spot_price_eur"] = pd.to_numeric(out["spot_price_eur"], errors="coerce")
        out["price_area"] = out["price_area"].astype(str)

        out = out.dropna(subset=["hour_utc", "price_area", "spot_price_eur"])
        return out[["hour_utc", "price_area", "spot_price_eur"]]

    out = df[["HourDK", "PriceArea", "SpotPriceEUR"]].copy()
    out.rename(columns={
        "HourDK": "time_dk",
        "PriceArea": "price_area",
        "SpotPriceEUR": "spot_price_eur"
    }, inplace=True)

    out["time_dk"] = pd.to_datetime(out["time_dk"], errors="coerce")
    out["spot_price_eur"] = pd.to_numeric(out["spot_price_eur"], errors="coerce")
    out["price_area"] = out["price_area"].astype(str)
    out = out.dropna(subset=["time_dk", "price_area", "spot_price_eur"])

    frames = []

    for area, g in out.groupby("price_area", sort=False):
        g = g.sort_values("time_dk").copy()

        try:
            g["time_dk"] = g["time_dk"].dt.tz_localize(
                DK_TZ, ambiguous="infer", nonexistent="shift_forward"
            )
        except Exception:
            g["time_dk"] = g["time_dk"].dt.tz_localize(
                DK_TZ, ambiguous="NaT", nonexistent="shift_forward"
            )
            g = g.dropna(subset=["time_dk"])

        g["hour_utc"] = g["time_dk"].dt.tz_convert("UTC").dt.floor("h")
        frames.append(g[["hour_utc", "price_area", "spot_price_eur"]])

    if not frames:
        return pd.DataFrame(columns=["hour_utc", "price_area", "spot_price_eur"])

    out = pd.concat(frames, ignore_index=True)
    out["hour_utc"] = pd.to_datetime(out["hour_utc"], utc=True, errors="coerce")
    out["spot_price_eur"] = pd.to_numeric(out["spot_price_eur"], errors="coerce")
    out = out.dropna(subset=["hour_utc", "spot_price_eur"])

    return out[["hour_utc", "price_area", "spot_price_eur"]]


def parse_dayahead_15m_to_hourly_utc(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["hour_utc", "price_area", "spot_price_eur"])

    out = df[["TimeDK", "PriceArea", "DayAheadPriceEUR"]].copy()
    out.rename(columns={
        "TimeDK": "time_dk",
        "PriceArea": "price_area",
        "DayAheadPriceEUR": "price_15m_eur"
    }, inplace=True)

    out["time_dk"] = pd.to_datetime(out["time_dk"], errors="coerce")
    out["price_15m_eur"] = pd.to_numeric(out["price_15m_eur"], errors="coerce")
    out["price_area"] = out["price_area"].astype(str)
    out = out.dropna(subset=["time_dk", "price_area", "price_15m_eur"])

    frames = []

    for area, g in out.groupby("price_area", sort=False):
        g = g.sort_values("time_dk").copy()

        try:
            g["time_dk"] = g["time_dk"].dt.tz_localize(
                DK_TZ, ambiguous="infer", nonexistent="shift_forward"
            )
        except Exception:
            g["time_dk"] = g["time_dk"].dt.tz_localize(
                DK_TZ, ambiguous="NaT", nonexistent="shift_forward"
            )
            g = g.dropna(subset=["time_dk"])

        g["time_utc"] = g["time_dk"].dt.tz_convert("UTC")

        hourly = (
            g.set_index("time_utc")["price_15m_eur"]
            .resample("h")
            .mean()
            .reset_index()
            .rename(columns={"time_utc": "hour_utc", "price_15m_eur": "spot_price_eur"})
        )
        hourly["price_area"] = area
        frames.append(hourly)

    if not frames:
        return pd.DataFrame(columns=["hour_utc", "price_area", "spot_price_eur"])

    out = pd.concat(frames, ignore_index=True)
    out["hour_utc"] = pd.to_datetime(out["hour_utc"], utc=True, errors="coerce")
    out["spot_price_eur"] = pd.to_numeric(out["spot_price_eur"], errors="coerce")
    out = out.dropna(subset=["hour_utc", "spot_price_eur"])

    return out[["hour_utc", "price_area", "spot_price_eur"]]


# =========================
# WINDOW LOGIC
# =========================
def fetch_and_upsert_window(con, start_utc: datetime, end_utc: datetime) -> int:
    if end_utc <= SWITCH_TO_DAYAHEAD_UTC:
        raw = fetch_eds(ELSPOT_DATASET, start_utc, end_utc)
        hourly = parse_elspot_to_hourly_utc(raw)
        return upsert_actuals(con, hourly)

    if start_utc >= SWITCH_TO_DAYAHEAD_UTC:
        raw = fetch_eds(DAYAHEAD_DATASET, start_utc, end_utc)
        hourly = parse_dayahead_15m_to_hourly_utc(raw)
        return upsert_actuals(con, hourly)

    mid = SWITCH_TO_DAYAHEAD_UTC
    n1 = fetch_and_upsert_window(con, start_utc, mid)
    n2 = fetch_and_upsert_window(con, mid, end_utc)
    return n1 + n2


# =========================
# MAIN INGEST
# =========================
def run_ingest():
    init_db()
    con = connect()

    latest = get_latest_hour_utc(con)

    if latest is None:
        start_utc = START_DATE_UTC
    else:
        start_utc = pd.to_datetime(latest, utc=True).to_pydatetime() + timedelta(hours=1)

    end_utc = datetime.now(timezone.utc)

    if start_utc >= end_utc:
        print("Database already up to date.")
        con.close()
        return

    cur = start_utc
    total_upserted = 0

    while cur < end_utc:
        nxt = min(cur + timedelta(days=WINDOW_DAYS), end_utc)
        n = fetch_and_upsert_window(con, cur, nxt)
        total_upserted += n
        print(f"{cur} -> {nxt} | upserted={n}")
        cur = nxt

    total_rows = con.execute("SELECT COUNT(*) FROM actuals").fetchone()[0]
    mn, mx = con.execute("SELECT MIN(hour_utc), MAX(hour_utc) FROM actuals").fetchone()

    con.close()

    print("\nINGEST COMPLETE")
    print("Total upserted:", total_upserted)
    print("Actuals total:", total_rows)
    print("Range UTC:", mn, "->", mx)


if __name__ == "__main__":
    run_ingest()