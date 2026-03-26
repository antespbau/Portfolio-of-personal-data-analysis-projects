# src/db.py
import duckdb
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "energy.duckdb"

def connect():
    return duckdb.connect(str(DB_PATH))

def init_db():
    con = connect()
    con.execute("""
        CREATE TABLE IF NOT EXISTS actuals (
            hour_utc TIMESTAMPTZ,
            price_area VARCHAR,
            spot_price_eur DOUBLE,
            PRIMARY KEY (hour_utc, price_area)
        );
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS features_hourly (
            hour_utc TIMESTAMPTZ,
            price_area VARCHAR,
            y DOUBLE,

            -- time features
            hour INT,
            dow INT,
            month INT,
            is_weekend INT,

            -- lags
            lag_1 DOUBLE,
            lag_24 DOUBLE,
            lag_168 DOUBLE,

            -- rolling stats (based on lag_1 history)
            roll_mean_24 DOUBLE,
            roll_std_24 DOUBLE,
            roll_mean_168 DOUBLE,
            roll_std_168 DOUBLE,

            PRIMARY KEY (hour_utc, price_area)
        );
    """)
    con.close()