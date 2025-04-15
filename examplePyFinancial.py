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
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Simulated stock data (replace this with your actual data from `fin_hist_data`)

# Prepare data for 3D plotting
stock_names = list(fin_hist_data.keys())
time_numeric = []
stock_indices = []
closing_prices = []

for i, stock in enumerate(stock_names):
    stock_data = fin_hist_data[stock]
    # CORRECTED CONVERSION: Convert index to numpy array first
    time_values = stock_data.index.to_numpy().astype('datetime64[s]').astype('int64')
    time_numeric.extend(time_values.tolist())
    stock_indices.extend([i] * len(stock_data))  # Stock index for y-axis
    closing_prices.extend(stock_data['Close'].values)  # Closing prices for z-axis

# Convert to numpy arrays for Plotly
time_numeric = np.array(time_numeric)
stock_indices = np.array(stock_indices)
closing_prices = np.array(closing_prices)

# Create a 3D scatter plot
fig = go.Figure()

fig.add_trace(go.Scatter3d(
    x=time_numeric,
    y=stock_indices,
    z=closing_prices,
    mode='markers',
    marker=dict(
        size=5,
        color=closing_prices,  # Color by closing price
        colorscale='Viridis',  # Colormap
        opacity=0.8
    )
))

# Customize layout
fig.update_layout(
    title="3D Stock Data Visualization",
    scene=dict(
        xaxis=dict(title="Time (numeric)"),
        yaxis=dict(title="Stock Name"),
        zaxis=dict(title="Closing Price (USD)")
    ),
)

# Add custom labels for stock names on y-axis
fig.update_layout(scene=dict(
    yaxis=dict(
        tickmode='array',
        tickvals=list(range(len(stock_names))),
        ticktext=stock_names
    )
))

fig.show()
