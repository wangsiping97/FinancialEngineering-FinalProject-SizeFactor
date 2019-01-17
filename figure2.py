# -*- coding: utf-8 -*-
import pandas as pd
import scipy.io as sio
import numpy as np
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

size = np.array(size)
ave_size = []
skews = []
kurts = []
for i in range(60, np.array(size).shape[0]):
    a = pd.Series(size[i])
    ave_size.append(a.mean())
    skews.append(a.skew())
    kurts.append(a.kurt())

df2 = pd.DataFrame({'month': np.arange(0, np.array(size).shape[0] - 60), 'skew': skews})

# Draw Plot
plt.figure(figsize=(16, 10), dpi=80)
plt.plot('month', 'skew', data=df2, color='tab:red')

# Decoration
plt.ylim(0, 30)
xtick_location = df2.index.tolist()[::12]
xtick_labels = [(x // 12) + 2005 for x in df2.month.tolist()[::12]]
plt.xticks(ticks=xtick_location, labels=xtick_labels, rotation=0, fontsize=12, horizontalalignment='center',
           alpha=.7)
plt.yticks(fontsize=12, alpha=.7)
plt.grid(axis='both', alpha=.3)

# Remove borders
plt.gca().spines["top"].set_alpha(0.0)
plt.gca().spines["bottom"].set_alpha(0.3)
plt.gca().spines["right"].set_alpha(0.0)
plt.gca().spines["left"].set_alpha(0.3)
plt.gca().set(xlabel='Year', ylabel='Monthly Skew of Size')
plt.savefig('figure2.png')