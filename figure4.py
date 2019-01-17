# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame,Series
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
    x[0]=int(x[0]/100) #change the month in eom

backtest_return = pd.DataFrame(columns=['-3', '-4', '-5', '-6', '-7', '-8', '-9', '-10'], index=['+2', '+3', '+4', '+5', '+6', '+7', '+8', '+9'])

# Back test

revenue = np.zeros((221 - 60),np.float64)
revenues = []

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
        cur_max = -1e18
        for x in revenue:
            comp_ret *= (1 + x)
            compound_return.append(comp_ret)
            cur_max = max(cur_max, comp_ret)
            max_comp_returns.append(cur_max)

        if k == 2 and j == 10:
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
            plt.savefig('figure4.png')