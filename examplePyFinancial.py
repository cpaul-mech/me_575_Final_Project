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
#%% load data from file if it exists, otherwise download it.
fin_hist_data = {} # Initialize an empty dictionary to store the historical data for each stock
# key is stock name, value is the historical data (DataFrame)
for stock in stock_names:
    if os.path.exists(f"{stock}_hist.csv"):
        print(f"File {stock}_hist.csv already exists. Loading data...")
        fin_hist = pd.read_csv(f"{stock}_hist.csv", index_col=0, parse_dates=True)
        fin_hist_data[stock] = fin_hist
    else:
        print(f"{stock} data not found. Downloading historical data...")
        ticker = yf.Ticker(stock) # Create a Ticker object to access stock data
        ticker_history = ticker.history(period="5y")
        ticker_history.to_csv(f"{stock}_hist.csv") # Save the data to a csv file
        fin_hist_data[stock] = ticker_history
        print(f"Historical data for {stock} downloaded and saved to file.")

#%% ## Now let's go ahead and graph the data over the last 5 years.
# Define a larger set of colors using a colormap
num_colors = len(stock_names)
color_map = mpl.colormaps.get_cmap('tab20')  # 'tab20' provides 20 distinct colors
colors = [color_map(i / (num_colors - 1)) for i in range(num_colors)]  # Normalize indices to [0, 1]
# Set the color cycle for the plot
rcParams['axes.prop_cycle'] = cycler(color=colors)
plt.figure(1)
for stock in stock_names:
    plt.plot(fin_hist_data[stock].index, fin_hist_data[stock]['Close'], label=stock)
# The "Close" column contains the closing price of the stock for each day. The closing price is the last price at which the stock traded on that day.
plt.xticks(rotation=45) # Rotate x-axis labels for better readability
plt.title("Comparing Stock Prices Over the Last 5 Years")
plt.legend()
plt.xlabel("Date")
plt.ylabel("Stock Price (USD)")
plt.show() #

# %%
