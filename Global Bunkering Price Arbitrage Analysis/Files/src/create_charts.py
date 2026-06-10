import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


VLSFO_PATH = Path("data/processed/vlsfo_port_history.csv")
ARBITRAGE_PATH = Path("data/processed/route_arbitrage_europe_fujairah.csv")
OUTPUT_DIR = Path("outputs/charts")


def create_vlsfo_price_evolution(vlsfo: pd.DataFrame):
    plt.figure(figsize=(10, 6))

    for port in sorted(vlsfo["port"].unique()):
        port_df = vlsfo[vlsfo["port"] == port].sort_values("date")
        plt.plot(
            port_df["date"],
            port_df["price_usd_mt"],
            marker="o",
            label=port
        )

    plt.xlabel("Date")
    plt.ylabel("VLSFO price (USD/MT)")
    plt.title("VLSFO price evolution by port")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    output_path = OUTPUT_DIR / "vlsfo_price_evolution_by_port.png"
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"Saved: {output_path}")


def create_average_price_chart(vlsfo: pd.DataFrame):
    avg_prices = (
        vlsfo.groupby("port", as_index=False)["price_usd_mt"]
        .mean()
        .sort_values("price_usd_mt")
    )

    plt.figure(figsize=(9, 6))
    plt.bar(avg_prices["port"], avg_prices["price_usd_mt"])

    plt.xlabel("Port")
    plt.ylabel("Average VLSFO price (USD/MT)")
    plt.title("Average VLSFO price by port")
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path = OUTPUT_DIR / "average_vlsfo_price_by_port.png"
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"Saved: {output_path}")


def create_fujairah_rotterdam_spread_chart(vlsfo: pd.DataFrame):
    pivot = vlsfo.pivot_table(
        index="date",
        columns="port",
        values="price_usd_mt",
        aggfunc="mean"
    ).reset_index()

    if "Fujairah" not in pivot.columns or "Rotterdam" not in pivot.columns:
        print("Skipping Fujairah vs Rotterdam spread chart: missing port data.")
        return

    pivot["spread_fujairah_rotterdam"] = pivot["Fujairah"] - pivot["Rotterdam"]

    plt.figure(figsize=(10, 6))
    plt.plot(
        pivot["date"],
        pivot["spread_fujairah_rotterdam"],
        marker="o"
    )

    plt.xlabel("Date")
    plt.ylabel("Spread (USD/MT)")
    plt.title("Daily VLSFO spread: Fujairah vs Rotterdam")
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path = OUTPUT_DIR / "daily_spread_fujairah_vs_rotterdam.png"
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"Saved: {output_path}")


def create_net_saving_chart(arbitrage: pd.DataFrame):
    plt.figure(figsize=(10, 6))

    for alternative_port in sorted(arbitrage["alternative_port"].unique()):
        temp = arbitrage[
            arbitrage["alternative_port"] == alternative_port
        ].sort_values("date")

        plt.plot(
            temp["date"],
            temp["net_saving_usd"],
            marker="o",
            label=alternative_port
        )

    plt.xlabel("Date")
    plt.ylabel("Net saving (USD)")
    plt.title("Net saving by date and alternative bunker port")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    output_path = OUTPUT_DIR / "net_saving_by_date_and_alternative_port.png"
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"Saved: {output_path}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    vlsfo = pd.read_csv(VLSFO_PATH)
    arbitrage = pd.read_csv(ARBITRAGE_PATH)

    vlsfo["date"] = pd.to_datetime(vlsfo["date"])
    vlsfo["price_usd_mt"] = pd.to_numeric(
        vlsfo["price_usd_mt"],
        errors="coerce"
    )

    arbitrage["date"] = pd.to_datetime(arbitrage["date"])
    arbitrage["net_saving_usd"] = pd.to_numeric(
        arbitrage["net_saving_usd"],
        errors="coerce"
    )

    create_vlsfo_price_evolution(vlsfo)
    create_average_price_chart(vlsfo)
    create_fujairah_rotterdam_spread_chart(vlsfo)
    create_net_saving_chart(arbitrage)

    print("\nAll charts created successfully.")


if __name__ == "__main__":
    main()