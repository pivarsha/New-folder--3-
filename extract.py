import requests
import pandas as pd
import matplotlib.pyplot as plt

def fetch_stock_data(stock_list):
   
    url = 'https://api.nsepy.xyz/api/quote'
    stock_data = {}
    for stock in stock_list:
        params = {'symbol': stock, 'series': 'EQ'}
        response = requests.get(url, params=params)
        data = response.json()['data']
        stock_data[stock] = data
    return stock_data


def plot_stock_data(stock_data):
    """
    Plots the closing values of each stock in a dictionary of stock data.
    
    Args:
        stock_data (dict): A dictionary where each key is a stock symbol and the corresponding value
        is a list of dictionaries containing the stock data.
        
    Returns:
        None
    """
    fig, ax = plt.subplots()
    for stock in stock_data:
        data = stock_data[stock]
        dates = [x['Date'] for x in data]
        close_values = [x['Close'] for x in data]
        ax.plot(dates, close_values, label=stock)
    ax.set_xticks(ax.get_xticks()[::30])
    ax.legend()
    ax.set_title('Closing Values of Stocks')
    plt.show()


def concat_stock_data(stock_data):
    """
    Concatenates the data for all the stocks in a dictionary into a single Pandas DataFrame.
    
    Args:
        stock_data (dict): A dictionary where each key is a stock symbol and the corresponding value
        is a list of dictionaries containing the stock data.
        
    Returns:
        A Pandas DataFrame with the concatenated data, in the desired table format.
    """
    stock_data_list = []
    for stock in stock_data:
        data = stock_data[stock]
        df = pd.DataFrame(data)
        df['Stock'] = stock
        stock_data_list.append(df)
    table_value = pd.concat(stock_data_list, axis=0, ignore_index=True)
    table_value = table_value.pivot(index='Date', columns='Stock', values='Close')
    return table_value


# Fetch stock data
stock_list = ['SBIN', 'ASIANPAINT', 'AXISBANK']
stock_data = fetch_stock_data(stock_list)

# Plot stock data
plot_stock_data(stock_data)

# Concatenate stock data
table_value = concat_stock_data(stock_data)
print(table_value)