import sys
import os

import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

_data_dir = os.getenv("DATA_DIR", f"{os.path.dirname(os.path.dirname(__file__))}/data")

def main() -> int:
    numeric_columns = ["close", "open", "high", "low", "volume", "market_cap"]

    btc_df = pd.read_csv(f"{_data_dir}/bitcoin_daily_14112014.csv")
    btc_df[numeric_columns] = btc_df[numeric_columns].astype(float)
    btc_df["pct_change"] = btc_df["close"].pct_change()
    btc_df.dropna(inplace=True)

    rates_df = pd.read_csv(f"{_data_dir}/fed_rates_daily_14112014.csv")
    rates_df["rate"] = rates_df["rate"].astype(float)

    l = stats.linregress(btc_df["pct_change"], rates_df["rate"])

    print(l)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    ax1.scatter(btc_df["pct_change"], rates_df["rate"], color="blue", label="Data points")
    ax1.plot(btc_df["pct_change"], l.intercept + l.slope * btc_df["pct_change"], color="red", label="Regression line")
    ax1.set_xlabel("BTC Percent Change")
    ax1.set_ylabel("Fed Rate")
    ax1.set_title("BTC Percent Change vs Fed Rate with Linear Regression")
    ax1.legend()

    ax2.plot(btc_df.index, btc_df["close"], color="green", label="BTC Close Price")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("BTC Close Price", color="green")
    ax2.tick_params(axis='y', labelcolor="green")

    ax3 = ax2.twinx()
    ax3.plot(rates_df.index, rates_df["rate"], color="orange", label="Fed Rate")
    ax3.set_ylabel("Fed Rate", color="orange")
    ax3.tick_params(axis='y', labelcolor="orange")

    ax2.set_title("BTC Close Price and Fed Rate Over Time")
    ax2.legend(loc="upper left")
    ax3.legend(loc="upper right")

    plt.tight_layout()
    plt.savefig(f"{_data_dir}/btc_fed_rate_analysis.png")

    return 0

if __name__ == "__main__":
    sys.exit(main())