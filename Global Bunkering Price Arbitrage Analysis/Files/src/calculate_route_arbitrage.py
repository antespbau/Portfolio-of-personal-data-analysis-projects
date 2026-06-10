import pandas as pd
from pathlib import Path

PRICE_PATH = Path("data/processed/vlsfo_port_history.csv")
OUTPUT_PATH = Path("data/processed/route_arbitrage_europe_fujairah.csv")


# Simple assumptions for first version
BUNKER_QUANTITY_MT = 1000
PORT_CALL_COST_USD = 8000
DAILY_VESSEL_COST_USD = 25000
RISK_BUFFER_PCT = 0.10

# Approximate route assumptions
# These represent additional operational assumptions for bunkering earlier
SCENARIOS = [
    {
        "route": "Europe to Fujairah",
        "expensive_port": "Fujairah",
        "alternative_port": "Rotterdam",
        "extra_days": 0.0,
        "notes": "Bunker at origin / Europe before sailing to Fujairah"
    },
    {
        "route": "Europe to Fujairah",
        "expensive_port": "Fujairah",
        "alternative_port": "Gibraltar",
        "extra_days": 0.2,
        "notes": "Bunker at Gibraltar as strategic Mediterranean/Atlantic hub"
    }
]


def main():
    prices = pd.read_csv(PRICE_PATH)

    prices["date"] = pd.to_datetime(prices["date"])
    prices["price_usd_mt"] = pd.to_numeric(prices["price_usd_mt"], errors="coerce")

    results = []

    for scenario in SCENARIOS:
        expensive_port = scenario["expensive_port"]
        alternative_port = scenario["alternative_port"]

        # Get only the two ports needed
        selected = prices[
            prices["port"].isin([expensive_port, alternative_port])
        ].copy()

        # Pivot so each date has both prices in one row
        pivot = selected.pivot_table(
            index="date",
            columns="port",
            values="price_usd_mt",
            aggfunc="mean"
        ).reset_index()

        # Only keep dates where both prices exist
        pivot = pivot.dropna(subset=[expensive_port, alternative_port])

        for _, row in pivot.iterrows():
            expensive_price = row[expensive_port]
            alternative_price = row[alternative_port]

            spread_usd_mt = expensive_price - alternative_price

            # Only positive arbitrage opportunities
            if spread_usd_mt <= 0:
                continue

            gross_saving = spread_usd_mt * BUNKER_QUANTITY_MT

            delay_cost = scenario["extra_days"] * DAILY_VESSEL_COST_USD
            risk_buffer = gross_saving * RISK_BUFFER_PCT

            total_extra_cost = PORT_CALL_COST_USD + delay_cost + risk_buffer

            net_saving = gross_saving - total_extra_cost

            results.append({
                "date": row["date"],
                "route": scenario["route"],
                "expensive_port": expensive_port,
                "alternative_port": alternative_port,
                "expensive_price_usd_mt": expensive_price,
                "alternative_price_usd_mt": alternative_price,
                "spread_usd_mt": spread_usd_mt,
                "bunker_quantity_mt": BUNKER_QUANTITY_MT,
                "gross_saving_usd": gross_saving,
                "port_call_cost_usd": PORT_CALL_COST_USD,
                "extra_days": scenario["extra_days"],
                "delay_cost_usd": delay_cost,
                "risk_buffer_usd": risk_buffer,
                "total_extra_cost_usd": total_extra_cost,
                "net_saving_usd": net_saving,
                "profitable": net_saving > 0,
                "notes": scenario["notes"]
            })

    result = pd.DataFrame(results)

    result = result.sort_values(
        ["date", "net_saving_usd"],
        ascending=[True, False]
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_PATH, index=False)

    print("Route arbitrage results:")
    print(result)

    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()