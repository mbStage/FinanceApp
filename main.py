import yfinance as yf
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from src.importPortfolio import get_portfolio

stocks = get_portfolio("c25")
print(f'stocks: {stocks}')

data = yf.download(stocks, start="2024-12-30", end="2026-01-15")
treading_days_by_year = data.groupby(data.index.year).size().to_dict()

cov_matrix =  data['Close'].pct_change().apply(lambda x: np.log(1+x)).cov()
corr_matrix =  data['Close'].pct_change().apply(lambda x: np.log(1+x)).corr()

w = {}
for stock in stocks:
    w[stock] = 1/len(stocks)

port_var = cov_matrix.mul(w, axis=0).mul(w, axis=1).sum().sum()
ind_er = data['Close'].resample('YE').last().pct_change().mean()

p_ret = []
p_vol = []
p_weights = []

num_assests = len(stocks)
num_portfolios = 100

for portfolio in range(num_portfolios):
    weights = np.random.random(num_assests)
    weights /= np.sum(weights)  
    p_weights.append(weights)
    returns = np.dot(weights, ind_er)

    p_ret.append(returns)
    var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()
    sd = np.sqrt(var)
    ann_sd = sd * np.sqrt(252)
    p_vol.append(ann_sd)

portfolio = {'Returns':p_ret, 'Volatility':p_vol}

for counter, symbol in enumerate(stocks):   
    portfolio[symbol+' Weight'] = [w[counter] for w in p_weights]   

df = pd.DataFrame(portfolio)

rf = 0.02 
optimal_risky_port = df.iloc[((df['Returns']-rf) / df['Volatility']).idxmax()]
print(optimal_risky_port)