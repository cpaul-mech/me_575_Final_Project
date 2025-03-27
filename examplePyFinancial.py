#%% this line here lets me run the code as a jupyter notebook cell by hitting ctrl+enter or cmd+enter on mac.
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# now we will practice getting stock data!!
#%% ## Lets start off by downloading the stock data for Tesla (TSLA) for the past 5 years and storing it locally
# we will use the yfinance library to do this
tsla = yf.Ticker("TSLA") # Create a Ticker object to access Tesla stock data
tsla_hist = tsla.history(period="5y") # Get the historical stock data for the past 5 years
tsla_hist.to_csv("tsla_hist.csv") # Save the data to a csv file

#%% ## Now let's go ahead and graph the data over the last 5 years.
plt.plot(tsla_hist.index, tsla_hist["Close"]) 
# The "Close" column contains the closing price of the stock for each day.
plt.title("Tesla Stock Price Over the Last 5 Years")
plt.xlabel("Date")
plt.ylabel("Stock Price (USD)")
plt.show()
