#%% this line here lets me run the code as a jupyter notebook cell by hitting ctrl+enter or cmd+enter on mac.
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
from matplotlib.ticker import FuncFormatter
from matplotlib import cm 
from matplotlib import rcParams
from cycler import cycler
# now we will practice getting stock data!!
#%% ## Lets start off by downloading the stock data for Tesla (TSLA) for the past 5 years and storing it locally
# we will use the yfinance library to do this
#check to see if the historical data has already been downloaded and saved locally
stock_names = [
    "TSLA", # Tesla Inc.
    "AAPL", # Apple Inc.
    "MSFT", # Microsoft Corporation
    "AMZN", # Amazon.com Inc.
    "GOOGL", # Alphabet Inc. (Google)
    "TERA", # Teradyne Inc.
    "PWR", # Quanta Services Inc.
    "NVDA", # NVIDIA Corporation *note: more of a volatile stock apparently.
    "ZION", # Zions Bancorporation
    "RIVN", # Rivian Automotive Inc. * Emerging sector company
    "PLTR", # Palantir Technologies Inc.
    "MRNA", # Moderna Inc. * note the covid bumb?
]
#%%
def load_or_download_stock_data(stock_names, period="5y"):
    """
    Load stock data from local files if available, otherwise download it.
    Returns a dictionary with stock names as keys and DataFrames as values.
    """
    fin_hist_data = {}
    for stock in stock_names:
        try:
            if os.path.exists(f"{stock}_hist.csv"):
                print(f"File {stock}_hist.csv already exists. Loading data...")
                fin_hist = pd.read_csv(f"{stock}_hist.csv", index_col=0, parse_dates=True)
                fin_hist_data[stock] = fin_hist
            else:
                print(f"{stock} data not found. Downloading historical data...")
                ticker = yf.Ticker(stock)
                ticker_history = ticker.history(period=period)
                ticker_history.to_csv(f"{stock}_hist.csv")
                fin_hist_data[stock] = ticker_history
                print(f"Historical data for {stock} downloaded and saved to file.")
        except Exception as e:
            print(f"Error processing {stock}: {e}")
    return fin_hist_data

def plot_stock_data(fin_hist_data, stock_names):
    """
    Plot the closing prices of stocks over time.
    """
    num_colors = len(stock_names)
    color_map = mpl.colormaps.get_cmap('tab20')
    colors = [color_map(i / (num_colors - 1)) for i in range(num_colors)]
    rcParams['axes.prop_cycle'] = cycler(color=colors)
    
    plt.figure(1)
    for stock in stock_names:
        plt.plot(fin_hist_data[stock].index, fin_hist_data[stock]['Close'], label=stock)
    plt.xticks(rotation=45)
    plt.title("Comparing Stock Prices Over the Last 5 Years")
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Stock Price (USD)")
    plt.show()
#%% 
# Main execution
fin_hist_data = load_or_download_stock_data(stock_names)
plot_stock_data(fin_hist_data, stock_names)

# %%
