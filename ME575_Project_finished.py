##!/usr/bin/env python3
## -*- coding: utf-8 -*-
"""
Created on Sat Apr  5 15:34:38 2025

@author: addisonmcclure
"""
#%%
from turtle import color
import matplotlib
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
#%%
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
def organize_data(stock_names, period = "5y"):
    
    all_closing_prices = []
    dates = None
    
    for stock in stock_names:
        try:
            if os.path.exists(f"{stock}_hist.csv"):
                print(f"File {stock}_hist.csv already exists. Loading data...")
                fin_hist = pd.read_csv(f"{stock}_hist.csv", index_col=0, parse_dates=True)
                closing_prices = fin_hist['Close']
            else:
                print(f"{stock} data not found. Downloading historical data for the past 5 years...")
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
def buy(x, cash, data, R, stock_index, day_index):
    # find max number of shares you can buy
    n_max = int(np.floor(cash/data.iat[day_index, stock_index]))
    
    # buy a random number of stocks
    n = random.randint(0, n_max)
    
    # update portfolio
    x[stock_index] = x[stock_index] + n
    cash = cash - n*data.iat[day_index, stock_index]
    
    # don't buy if too much of portoflio is in one stock
    if x[stock_index]*data.iat[day_index, stock_index]/f(x, data, day_index) > R:
        x[stock_index] = x[stock_index] - n
        cash = cash + n*data.iat[day_index, stock_index]
    
    return x, cash

# sells all shares of a stock
def sell(x, cash, data, stock_index, day_index):
    # calculate total cash
    cash = cash + np.dot(x[stock_index], data.iat[day_index, stock_index])
    
    # set number of stocks to 0 because you sold
    x[stock_index] = 0
    
    return x, cash

"""
# Doesn't work very well, don't make as much money
# sells a random number of shares
def sell(x, cash, data, stock_index, day_index):
    # generate random number of stocks to sell
    n = random.randint(0, x[stock_index])
    
    # update portfolio
    x[stock_index] = x[stock_index] - n
    cash = cash - n*data.iat[day_index, stock_index]
    
    return x, cash
"""

"""
# goes in day_trading()
# slightly increases profit but makes code take forever to run
# buy if price increases rapidly, keep buying until you run out of cash
while buy_options.any() and any(cash >= data.iat[i, j] for j in range(len(data.columns)) if buy_options[j]):
    for j in range(len(data.columns)):
        if buy_options[j] and cash >= data.iat[i, j]:
            x, cash = buy(x, cash, data, R, j, i)
"""


def day_trading(cash_initial, data, time, R):
    
    # for tracking portfolio
    portfolio_history = np.zeros([time, len(data.columns)])
    portfolio_value_history = np.zeros([time,1])
    cash_history = np.zeros([time,1])
    
    # make initial investment
    x, cash = initial_investment(cash_initial, data)


    cash_history[0] = cash

    # every day, take derivative and decide what to buy and sell 
    for i in range(1, time):
        
        # calculate backwards difference derivative for each stock
        derivatives = data.iloc[i] - data.iloc[i-1]
        
        for j in range(data.shape[1]):
            
            # sell if stock rapidly increases
            if derivatives.iloc[j] > 2:
                x, cash = sell(x, cash, data, j, i)
                
            # buy if stock rapidly decreases
            elif derivatives.iloc[j] < -1:  
                x, cash = buy(x, cash, data, R, j, i)
            cash_history[i] = cash
                
        # record purchases and sales
        portfolio_history[i,:] = x
        portfolio_value_history[i] = f(x, data, i)
        
    # cash out at the end
    final_value = cash + f(x, data, i)
    profit = final_value - cash_initial

    return profit, portfolio_history, portfolio_value_history, cash_history


# exploring the design space
explorations_to_run = ['single_long_run'] # 'time', 'cash', 'risk', 'numStocks'
#%%
if 'time' in explorations_to_run:
    n = 30
    # vary time in market
    time = [90, 180, 270, 365, 600, 800, 1095] 
    profit_time = np.zeros(len(time))
    profit_values = np.zeros(n)
    profit_sd_time = np.zeros(len(time))

    # constants
    cash_initial = 1000
    R = 1
    stock_names = ["TSLA", "AAPL", "MSFT", "AMZN", "GOOGL"]
    data = organize_data(stock_names)

    # for each time, run day_trading() 30 times and calculate average profit
    for i in range(len(time)):
        for j in range(n):
            a, b, c = day_trading(cash_initial, data, time[i], R)
            profit_values[j] = a
        print("completed iteration ", i+1, " of ", len(time))
        profit_time[i] = np.mean(profit_values)
        profit_sd_time[i] = np.std(profit_values)
    
    # plot results
    plt.figure(1)
    plt.errorbar(time, profit_time, yerr=profit_sd_time, fmt='o', capsize=5, label='Error Bars represent 1 SD for 30 iterations')
    plt.xlabel('Time (Days)')
    plt.ylabel('Average Profit ($)')
    plt.legend()
    plt.title('Effect of Time in the Market on Average Profit')
    plt.show()

#%%
if 'cash' in explorations_to_run:
    n = 30
    # vary initial cash investment
    cash = [100, 500, 1000, 2200, 5000, 7500, 10000]
    profit_cash = np.zeros(len(cash))
    profit_values = np.zeros(n)
    profit_sd_cash = np.zeros(len(cash))

    # constants
    time = 365
    R = 1
    stock_names = ["TSLA", "AAPL", "MSFT", "AMZN", "GOOGL"]
    data = organize_data(stock_names)

    # for each cash, run day_trading() 30 times and calculate average profit
    for i in range(len(cash)):
        for j in range(n):
            a, b, c, d = day_trading(cash[i], data, time, R)
            profit_values[j] = a
        print("completed iteration ", i+1, " of ", len(cash))
        profit_sd_cash[i] = np.std(profit_values)
        profit_cash[i] = np.mean(profit_values)
     
    # plot results
    plt.figure(2)
    plt.xlabel('Initial Investment ($)')
    plt.ylabel('Average Profit ($)')
    plt.errorbar(cash, profit_cash, yerr=profit_sd_cash, fmt='o', capsize=5, label='Error Bars represent 1 SD for 30 iterations')
    plt.legend()
    plt.title('Effect of Initial Investment Amount on Average Profit')
    plt.show()
#%%
if 'risk' in explorations_to_run:
    n = 30
    # vary risk
    R = [0.5, 0.625, 0.75, 0.875, 1]
    profit_risk = np.zeros(len(R))
    profit_values = np.zeros(n)
    profit_sd_risk = np.zeros(len(R))

    # constants
    time = 365
    cash = 1000
    stock_names = ["NVDA", "MSFT", "MRNA", "GOOGL", "ZION"]
    data = organize_data(stock_names)

    # for each risk, run day_trading() 30 times and calculate average profit
    for i in range(len(R)):
        for j in range(n):
            a, b, c, d = day_trading(cash, data, time, R[i])
            profit_values[j] = a
        print("completed iteration ", i+1, " of ", len(R))
        profit_sd_risk[i] = np.std(profit_values)
        profit_risk[i] = np.mean(profit_values)
    
    # plot results
    plt.figure(2)
    plt.errorbar(R, profit_risk, yerr=profit_sd_risk, fmt='o', capsize=5, label='Error Bars represent 1 SD for 30 iterations')
    plt.xlabel('Risk')
    plt.ylabel('Average Profit ($)')
    plt.title('Effect of Risk on Average Profit')
    plt.legend()
    plt.show()

#%%
if 'numStocks' in explorations_to_run:
    n = 30
    # vary number of stocks
    profit_stocks = np.zeros(5)
    profit_values = np.zeros(n)
    profit_sd_stocks = np.zeros(5)

    # constants
    cash = 10000
    time = 365
    R = 1

    # 1 stock
    stock_names = ["TSLA"]
    data = organize_data(stock_names)

    for j in range(n):
        a, b, c, d = day_trading(cash, data, time, R)
        profit_values[j] = a
    profit_sd_stocks[0] = np.std(profit_values)
    profit_stocks[0] = np.mean(profit_values)

    # 3 stocks
    stock_names = ["TSLA", "AAPL", "MSFT"]
    data = organize_data(stock_names)

    for j in range(n):
        a, b, c, d = day_trading(cash, data, time, R)
        profit_values[j] = a
        
    profit_stocks[1] = np.mean(profit_values)
    profit_sd_stocks[1] = np.std(profit_values)

    # 5 stocks
    stock_names = ["TSLA", "AAPL", "MSFT", "AMZN", "GOOGL"]
    data = organize_data(stock_names)

    for j in range(n):
        a, b, c, d = day_trading(cash, data, time, R)
        profit_values[j] = a
        
    profit_stocks[2] = np.mean(profit_values)
    profit_sd_stocks[2] = np.std(profit_values)

    # 7 stocks
    stock_names = ["TSLA", "AAPL", "MSFT", "AMZN", "GOOGL", "NVDA", "ZION"]
    data = organize_data(stock_names)

    for j in range(n):
        a, b, c, d = day_trading(cash, data, time, R)
        profit_values[j] = a
        
    profit_stocks[3] = np.mean(profit_values)
    profit_sd_stocks[3] = np.std(profit_values)

    # 10 stocks
    stock_names = ["TSLA", "AAPL", "MSFT", "AMZN", "GOOGL", "NVDA", "ZION", "MRNA", "NFLX", "DIS"]
    data = organize_data(stock_names)

    for j in range(n):
        a, b, c, d = day_trading(cash, data, time, R)
        profit_values[j] = a
        
    profit_sd_stocks[4] = np.std(profit_values)
    profit_stocks[4] = np.mean(profit_values)

    # plot results
    plt.figure(3)
    number = [1, 3, 5, 7, 10]
    plt.errorbar(number, profit_stocks, yerr=profit_sd_stocks, fmt='o', capsize=5, label='Error Bars represent 1 SD for 30 iterations')
    plt.legend()
    plt.title("Effect of Number of Stocks on Average Profit")
    plt.xlabel("Number of Stocks in Portfolio")
    plt.ylabel("Average Profit ($)")
    plt.show()

# %%
# Experiment with returning the portfolio history and value history of a single run with 5 years of data on all possible stocks, and 10,000 initial investment.
# This will allow us to visualize the portfolio's performance over time.
if 'single_long_run' in explorations_to_run:
    cash = 10000
    stock_names = ["TSLA", "AAPL", "MSFT", "AMZN", "GOOGL", "NVDA", "ZION", "MRNA", "NFLX", "DIS"]
    data = organize_data(stock_names)
    time = 700  # 5 years in days
    R = 0.76 # Risk factor
    profits, portfolio_history, value_history, cash_history = day_trading(cash, data, time, R)
    #%%
    # plt.figure(4)
    # plt.plot(value_history, label='Portfolio Value Over Time')
    # plt.xlabel('Days')
    # plt.ylabel('Portfolio Value ($)')
    # plt.title('Portfolio Performance Over 5 Years')
    # plt.legend()
    # plt.show()
    #%%
    # Assuming you have these from your simulation:
# portfolio_history, data, cash_history, stock_names

    stock_values = portfolio_history * data.values[:time]
    cash_history_flat = cash_history.flatten()
    stack_data = np.vstack((cash_history_flat, stock_values.T))

    num_areas = len(stock_names) + 1  # +1 for cash
    # cmap = plt.get_cmap("tab20")
    # colors = [cmap(i) for i in range(num_areas)]

    # plt.figure(figsize=(12, 6))
    # plt.stackplot(
    #     np.arange(stock_values.shape[0]),
    #     stack_data,
    #     labels=['Cash'] + stock_names,
    #     alpha=0.8,
    #     colors=colors
    # )
    # plt.xlabel('Days')
    # plt.ylabel('Value ($)')
    # plt.title('Portfolio Value Over Time (Including Cash)')
    # plt.legend(loc='upper left', ncol=2)
    # plt.tight_layout()
    # plt.show()

#%%
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from matplotlib import cm

    # Assuming you have these from your simulation:
    # - stock_values: portfolio_history * data.values
    # - cash_history_flat: cash_history.flatten()
    # - stock_names: list of your stock tickers

    # 1. Set up the figure and axes
    fig, ax = plt.subplots(figsize=(12, 6))

    # 2. Prepare data for stacked plot
    combined_data = np.vstack((cash_history_flat, stock_values.T))
    labels = ['Cash'] + stock_names

    # 3. Choose a colormap with many distinct colors
    n_components = len(labels)
    cmap = plt.get_cmap('tab20', n_components)
    colors = [cmap(i) for i in range(n_components)]

    # 4. Create static legend patches that we'll reuse
    patches = [plt.Rectangle((0,0), 1, 1, color=colors[i]) for i in range(n_components)]

    # 5. Define update function for animation
    def update(frame):
        ax.clear()
        
        # Only plot data up to the current frame
        days = np.arange(frame)
        data_to_plot = combined_data[:, :frame]
        
        # Create stacked plot for this frame
        if frame > 0:
            ax.stackplot(days, data_to_plot, colors=colors, alpha=0.8)
        
        # Re-add the legend after clearing axes (this ensures legend persistence)
        ax.legend(patches, labels, loc='upper left', ncol=2)
        
        # Dynamically update x-axis limit
        ax.set_xlim(0, frame + 50)
        
        # Set y-axis limit based on maximum portfolio value
        if frame > 0:
            total_value = np.sum(data_to_plot, axis=0)
            max_value = np.max(total_value) if len(total_value) > 0 else 30000
            ax.set_ylim(0, max_value * 1.1)  # 10% padding
        else:
            ax.set_ylim(0, 35000)  # Initial view
        
        # Labels and title
        ax.set_xlabel('Days')
        ax.set_ylabel('Value ($)')
        ax.set_title(f'Portfolio Value Over Time - Day {frame}')
        
        # # Add annotation for market crash around day 450
        # if 440 <= frame <= 460:
        #     ax.annotate('Portfolio liquidation event', 
        #             xy=(450, 5000), xytext=(300, 20000),
        #             arrowprops=dict(facecolor='red', shrink=0.05),
        #             bbox=dict(boxstyle="round", fc="yellow", alpha=0.8))
        
        return ax

    # 6. Create animation
    # Use a subset of frames for better performance
    step = 5  # Every 5th day (adjust for smoothness vs. speed)
    frames = range(1, combined_data.shape[1], step)
    ani = FuncAnimation(fig, update, frames=frames, interval=50, blit=False)

    # Display the animation
    plt.tight_layout(pad=2.0)
    plt.show()

    # 7. Save the animation (uncomment to save)
    ani.save('portfolio_animation.gif', writer='pillow', fps=20, dpi=100)
    # For higher quality: 
    # ani.save('portfolio_animation.mp4', writer='ffmpeg', fps=30, dpi=100)

# %%
