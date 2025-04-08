#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  5 15:34:38 2025

@author: addisonmcclure
"""

import numpy as np
import random
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
from matplotlib.ticker import FuncFormatter
from matplotlib import cm 
from matplotlib import rcParams
from cycler import cycler

# downloading stock data
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


# plots stock data
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


# organizes all closing data for relevant stocks into a dataframe
def organize_data(stock_names, period = "10d"):
    
    all_closing_prices = []
    dates = None
    
    for stock in stock_names:
        try:
            if os.path.exists(f"{stock}_hist.csv"):
                print(f"File {stock}_hist.csv already exists. Loading data...")
                fin_hist = pd.read_csv(f"{stock}_hist.csv", index_col=0, parse_dates=True)
                closing_prices = fin_hist['Close']
            else:
                print(f"{stock} data not found. Downloading historical data for the past 10 days...")
                ticker = yf.Ticker(stock)
                ticker_history = ticker.history(period=period)
                ticker_history.to_csv(f"{stock}_hist.csv")
                closing_prices = ticker_history['Close']
                print(f"Historical data for {stock} downloaded and saved to file.")

            # Ensure the first stock defines the dates for the DataFrame
            if dates is None:
                dates = closing_prices.index
            
            # Add closing prices to the list, aligning by dates
            all_closing_prices.append(closing_prices)

        except Exception as e:
            print(f"Error processing {stock}: {e}")

    # Combine the closing prices into a DataFrame
    closing_prices_df = pd.DataFrame(all_closing_prices, index=stock_names).T
    closing_prices_df.index = dates

    return closing_prices_df


# objective function, calculates total value of portfolio
def f(x, data, day_index):
    return np.sum(x*data.iloc[day_index]) 


# initial investment
def initial_investment(cash, data): 
    
    n = len(data.columns)                       # number of companies
    x = np.zeros(n)                             # number of stocks for each company
    
    # evenly distirbute the cash over all stocks
    for i in range(n):
        x[i] = np.floor((cash / n) / data.iat[0, i])
    
    cash = cash - np.dot(x, data.iloc[0])       # remaining cash
    
    return x, cash


# buy stocks
def buy(x, cash, data, stock_index, day_index):
    # find max number of shares you can buy
    n_max = np.floor(cash/data.iat[day_index, stock_index])
    
    # buy a random number of stocks
    n = random.randint(0, n_max)
    
    # add a constraint to not buy if too much of your portfolio is in one stock
    
    # update portfolio
    x[stock_index]=x[stock_index] + n
    cash = cash - n*data.iat[day_index, stock_index]
    
    
    return x, cash

# sells all shares of a stock
def sell(x, cash, data, stock_index, day_index):
    # calculate total cash
    cash = cash + np.dot(x[stock_index], data.iat[day_index, stock_index])
    
    # set number of stocks to 0 because you sold
    x[stock_index] = 0
    
    return x, cash

"""
# sells a random number of shares
def sell(x, cash, data, stock_index, day_index):
    # generate random number of stocks to sell
    n = random.randint(0, x[stock_index])
    
    # update portfolio
    x[stock_index] = x[stock_index] - n
    cash = cash - n*data.iat[day_index, stock_index]
    
    return x, cash
"""


# main algorithm
def day_trading(cash_initial, data):
    
    # make initial investment
    x, cash = initial_investment(cash_initial, data)
    
    # every day, take derivative and decide what to buy and sell
    for i in range(1,100):
        # calculate backwards difference derivative for each stock price
        derivatives = (data.iloc[i] - data.iloc[i-1])/1
        
        # for every stock decide to buy or sell
        for j in range(data.shape[1]):
            
            # sell if stock rapidly increases
            if derivatives[j] > 2:
                x, cash = sell(x, cash, data, j, i)
            
            # buy if stock rapidly decreases
            elif derivatives[j] < -1:
                x, cash = buy(x, cash, data, j, i)
            
            print(cash)

    # cash out at the end
    cash = cash + f(x, data, i)
    profit = cash - cash_initial
    
    return profit


stock_names = [
    "TSLA", # Tesla Inc.
    "AAPL", # Apple Inc.
    "MSFT", # Microsoft Corporation
    "AMZN", # Amazon.com Inc.
    # "GOOGL", # Alphabet Inc. (Google)
    # "TERA", # Teradyne Inc.
    # "PWR", # Quanta Services Inc.
    # "NVDA", # NVIDIA Corporation *note: more of a volatile stock apparently.
    # "ZION", # Zions Bancorporation
    # "MRNA", # Moderna Inc. * note the covid bump
]

#fin_hist_data = load_or_download_stock_data(stock_names)
# plot_stock_data(fin_hist_data, stock_names)

data = organize_data(stock_names)

# how much money you have not in stocks
cash_initial = 1000

a = day_trading(cash_initial, data)
print(a)


"""
Things to Add
- Risk constraint (what percentage of portfolio can be one company)
- Cash constraint (if you have a bunch of cash, use it)
"""