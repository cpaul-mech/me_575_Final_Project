#%% this line here lets me run the code as a jupyter notebook cell by hitting ctrl+enter or cmd+enter on mac.
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# now we will practice getting stock data!!
#%%
tsla = yf.Ticker("TSLA")