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

# Backtest-Alpha

backtest_Alpha = pd.DataFrame(columns=['-3', '-4', '-5', '-6', '-7', '-8', '-9', '-10'], index=['+2', '+3', '+4', '+5', '+6', '+7', '+8', '+9'])


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
        revenue = np.zeros((221 - 60),np.float64)
        backtest_Alpha.iloc[k - 2][j - 3] = alpha

backtest_Alpha.to_csv('table6.csv')