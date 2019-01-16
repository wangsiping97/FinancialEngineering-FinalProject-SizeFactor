import pandas as pd
from pandas import DataFrame,Series
import scipy.io as sio
import numpy as np
from scipy.optimize import leastsq
import math

data = sio.loadmat('CaseDataAll.mat')
market_data = pd.read_csv('market.csv')
eom = data["a_EOM"]
mon = data["Mon_Yield"]
size = data["Mon_SizeAll"]
market_return = market_data['Mkt_Rf']
risk_free = market_data['rf']

for x in eom:
    x[0]=int(x[0]/100) #change the month in eom

backtest_return = pd.DataFrame(columns=['-3', '-4', '-5', '-6', '-7', '-8', '-9', '-10'], index=['+2', '+3', '+4', '+5', '+6', '+7', '+8', '+9'])

# Back test

# Backtest-Ave Return

revenue = np.zeros((223 - 60),np.float64)
revenues = []
stds = []

for k in range(2, 10): # buy-ins
    for j in range(k + 1, 11): # buy-outs
        for i in range(60, 221):
            a = pd.DataFrame(np.insert(mon[i: i + 2], 1, values=size[i], axis=0))
            a = a.iloc[1:3].dropna(axis=1, how="any").T
            a = a.sort_values(by=1, ascending=True)
            unit = int(np.size(a[1]) / 10)

            # Strategy: buy-in port_k, but-out port_j
            revenue[i - 60] = np.mean((a.iloc[unit * (k - 1):unit * k])[2]) - np.mean((a.iloc[unit * (j - 1): unit * j])[2])
        revenues.append(np.mean(revenue))
        stds.append(np.std(revenue))
        revenue = np.zeros((223 - 60),np.float64)

    for j in range(k + 1, 11):
        backtest_return.iloc[k - 2][j - 3] = revenues[j - k - 1]
    revenues = []

backtest_return.to_csv('backtest_Return.csv')

# Backtest-Sharpe Ratio

backtest_sharpe = pd.DataFrame(columns=['-3', '-4', '-5', '-6', '-7', '-8', '-9', '-10'], index=['+2', '+3', '+4', '+5', '+6', '+7', '+8', '+9'])


stds = []

for k in range(2, 10): # buy-ins
    for j in range(k + 1, 11): # buy-outs
        for i in range(60, 221):
            a = pd.DataFrame(np.insert(mon[i: i + 2], 1, values=size[i], axis=0))
            a = a.iloc[1:3].dropna(axis=1, how="any").T
            a = a.sort_values(by=1, ascending=True)
            unit = int(np.size(a[1]) / 10)

            # Strategy: buy-in port_k, but-out port_j
            revenue[i - 60] = np.mean((a.iloc[unit * (k - 1):unit * k])[2]) - np.mean((a.iloc[unit * (j - 1): unit * j])[2])
        revenues.append(np.mean(revenue))
        stds.append(np.std(revenue))
        revenue = np.zeros((223 - 60),np.float64)

    # Compute Sharpe Ratio
    sharpe = []
    for j in range(k + 1, 11):
        backtest_sharpe.iloc[k - 2][j - 3] = (revenues[j - k - 1] - np.mean(risk_free.dropna()))/stds[j - k - 1] * math.sqrt(12)
    revenues = []

backtest_sharpe.to_csv('backtest_sharpe.csv')

# Compute Max-Drawdown

backtest_MDrawdown = pd.DataFrame(columns=['-3', '-4', '-5', '-6', '-7', '-8', '-9', '-10'],
                                  index=['+2', '+3', '+4', '+5', '+6', '+7', '+8', '+9'])

# Back test

for k in range(2, 10):  # buy-ins
    for j in range(k + 1, 11):  # buy-outs
        compound_return = []
        drawdowns = []
        max_comp_returns = []
        for i in range(60, 221):
            a = pd.DataFrame(np.insert(mon[i: i + 2], 1, values=size[i], axis=0))
            a = a.iloc[1:3].dropna(axis=1, how="any").T
            a = a.sort_values(by=1, ascending=True)
            unit = int(np.size(a[1]) / 10)

            # Strategy: buy-in port_k, but-out port_j
            revenue[i - 60] = np.mean((a.iloc[unit * (k - 1):unit * k])[2]) - np.mean(
                (a.iloc[unit * (j - 1): unit * j])[2])
        comp_ret = 1
        #         print(revenue)
        cur_max = -1e18
        for x in revenue:
            comp_ret *= (1 + x)

            compound_return.append(comp_ret)
            cur_max = max(cur_max, comp_ret)
            max_comp_returns.append(cur_max)
        # print(compound_return)
        for x in range(len(compound_return)):
            drawdowns.append((compound_return[x] - max_comp_returns[x]) / max_comp_returns[x] * 100)
        # print(drawdowns)
        backtest_MDrawdown.iloc[k - 2][j - 3] = min(drawdowns)

        revenue = np.zeros((223 - 60), np.float64)

backtest_MDrawdown.to_csv('backtest_MDrawdown.csv')

# Compute Alpha

backtest_Alpha = pd.DataFrame(columns=['-3', '-4', '-5', '-6', '-7', '-8', '-9', '-10'], index=['+2', '+3', '+4', '+5', '+6', '+7', '+8', '+9'])

# Back test

def func(_x, p):
    beta, alpha = p
    return beta * _x + alpha

def residuals(p, _y, _x):
    return _y - func(_x, p)

x = market_data['Mkt_Rf'][60:-1]
x = x.as_matrix()

for k in range(2, 10): # buy-ins
    for j in range(k + 1, 11): # buy-outs
        y = []
        for i in range(60, 221):
            a = pd.DataFrame(np.insert(mon[i: i + 2], 1, values=size[i], axis=0))
            a = a.iloc[1:3].dropna(axis=1, how="any").T
            a = a.sort_values(by=1, ascending=True)
            unit = int(np.size(a[1]) / 10)

            # Strategy: buy-in port_k, but-out port_j
            revenue[i - 60] = np.mean((a.iloc[unit * (k - 1):unit * k])[2]) - np.mean((a.iloc[unit * (j - 1): unit * j])[2])
            y.append(revenue[i - 60] - risk_free[i])
        y = np.array(y)
        p = leastsq(residuals, [0, 0], args = (y, x))
        beta, alpha = p[0]
        revenue = np.zeros((223 - 60),np.float64)
        backtest_Alpha.iloc[k - 2][j - 3] = alpha

backtest_Alpha.to_csv('backtest_Alpha.csv')
