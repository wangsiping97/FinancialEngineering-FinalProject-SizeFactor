# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame, Series
import scipy.io as sio
import numpy as np
from scipy.optimize import leastsq
import math
import matplotlib.pyplot as plt

data = sio.loadmat('CaseDataAll.mat')
market_data = pd.read_csv('market.csv')
eom = data["a_EOM"]
mon = data["Mon_Yield"]
size = data["Mon_SizeAll"]
market_return = market_data['Mkt_Rf']
risk_free = market_data['rf']

for x in eom:
    x[0] = int(x[0] / 100)  # change the month in eom

# long 2, short 10

revenue = np.zeros((221 - 60),np.float64)
compound_return = []
max_comp_returns = []
drawdowns = []

for i in range(60, 221):
    a = pd.DataFrame(np.insert(mon[i - 3: i + 2], 1, values=size[i], axis=0))
    a = a.iloc[1:6].dropna(axis=1, how="any").T
    a = a.sort_values(by=1, ascending=True)
    unit = int(np.size(a[1]) / 10)
    unit_2 = a.iloc[unit:unit * 2]
    unit_2 = unit_2.loc[unit_2[4] >= -.1]
    unit_2 = unit_2.loc[unit_2[3] >= -.1]
    unit_2 = unit_2.loc[unit_2[2] >= -.1]
    unit_10 = a.iloc[unit * 9:]
    revenue[i - 60] = np.mean(unit_2[5]) - np.mean(unit_10[5]) # equal weighted

Ave_Rt = np.mean(revenue) * 100
Sharpe_Ratio = (Ave_Rt - np.mean(risk_free.dropna()))/np.std(revenue) * math.sqrt(12)

comp_ret = 1
cur_max = -1e18
for x in revenue:
    comp_ret *= (1 + x)

    compound_return.append(comp_ret)
    cur_max = max(cur_max, comp_ret)
    max_comp_returns.append(cur_max)

df = pd.DataFrame({'month': np.arange(0, 161), 'compound_return': compound_return})

# Draw Plot
plt.figure(figsize=(16, 10), dpi=80)
plt.plot('month', 'compound_return', data=df, color='tab:red')

# Decoration
plt.ylim(0, 20)
xtick_location = df.index.tolist()[::12]
xtick_labels = [(x // 12) + 2005 for x in df.month.tolist()[::12]]
plt.xticks(ticks=xtick_location, labels=xtick_labels, rotation=0, fontsize=12, horizontalalignment='center',
           alpha=.7)
plt.yticks(fontsize=12, alpha=.7)
plt.grid(axis='both', alpha=.3)

# Remove borders
plt.gca().spines["top"].set_alpha(0.0)
plt.gca().spines["bottom"].set_alpha(0.3)
plt.gca().spines["right"].set_alpha(0.0)
plt.gca().spines["left"].set_alpha(0.3)
plt.gca().set(xlabel='Year', ylabel='Compound Return(%)')
plt.savefig('figure5.png')

for x in range(len(compound_return)):
    drawdowns.append((compound_return[x] - max_comp_returns[x]) / max_comp_returns[x] * 100)

MaxDrawdown = min(drawdowns)


def func(_x, p):
    beta, alpha = p
    return beta * _x + alpha

def residuals(p, _y, _x):
    return _y - func(_x, p)

x = market_data['Mkt_Rf'][60:-1]
x = x.as_matrix()

y = []

for i in range(60, 221):
    a = pd.DataFrame(np.insert(mon[i - 3: i + 2], 1, values=size[i], axis=0))
    a = a.iloc[1:6].dropna(axis=1, how="any").T
    a = a.sort_values(by=1, ascending=True)
    unit = int(np.size(a[1]) / 10)
    unit_2 = a.iloc[unit:unit * 2]
    unit_2 = unit_2.loc[unit_2[4] >= -.1]
    unit_2 = unit_2.loc[unit_2[3] >= -.1]
    unit_2 = unit_2.loc[unit_2[2] >= -.1]
    unit_10 = a.iloc[unit * 9:]
    revenue[i - 60] = np.mean(unit_2[5]) - np.mean(unit_10[5]) # equal weighted
    y.append(revenue[i - 60] - risk_free[i])
y = np.array(y)
p = leastsq(residuals, [0, 0], args = (y, x))
beta, alpha = p[0]
revenue = np.zeros((221 - 60),np.float64)


table9 = {'Ave_Rt': Ave_Rt, 'Alpha': alpha, 'Sharpe Ratio': Sharpe_Ratio, 'Max Drawdown': MaxDrawdown}
table9 = pd.DataFrame(table9, index = ['+2 -10'])
table9.to_csv('table9.csv')
