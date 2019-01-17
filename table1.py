# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame,Series
import scipy.io as sio
import numpy as np

data = sio.loadmat("CaseDataAll.mat")

mon_yield = data['Mon_Yield']
mon_Illiq = data['Mon_Illiq']
mon_BM = data['Mon_BM']
sizeall = data['Mon_SizeAll']
code = np.squeeze(data['a_Code'])

mon_return = DataFrame(mon_yield, columns = code)
mon_Illiq = DataFrame(mon_Illiq, columns = code)
mon_BM = DataFrame(mon_BM, columns = code)
sizeall = DataFrame(sizeall, columns = code)

label_size = ['Group%d' %x for x in range(1,11)]

port = []
for i in range(1,11):
    x = ('Group%d' %i)
    port.append(x)


Rt_EWs = []
temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

start = 66
for i in range(13):
    end = start + 12
    size_data = sizeall.iloc[start]
    yield_data = mon_return[start:end]
    size_quantile = pd.qcut(size_data,10,labels = label_size)
    grouped = yield_data.groupby([size_quantile],axis = 1)
    Mon_port_Rt = grouped.mean() # equal-weighted
    for m in range(1, 11):
        Yr_port_return = Mon_port_Rt['Group%d'%m].mean()
        temp[m - 1] += Yr_port_return
    start += 12
for i in range(10):
    Rt_EWs.append(temp[i]/13 * 100)


# Compute Rt_VWs

Rt_VWs = []
temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

start = 66
for i in range(13):
    end = start + 12
    size_data = sizeall.iloc[start]
    yield_data = mon_return[start:end]
    size_quantile = pd.qcut(size_data,10,labels = label_size)
    grouped = yield_data.groupby([size_quantile],axis = 1)
    piece = dict(list(grouped))
    for j in range(1, 11):  # 遍历每一个portfolio
        sum_size = 0
        sum_yield = 0
        for k in piece['Group%d' % j].columns:  # 遍历portfolio内的股票
            sum_yield += dict(size_data)[k] * (yield_data[k].mean())
            sum_size += dict(size_data)[k]
        Yr_port_return = sum_yield / sum_size  # 每个portfolio每年的市值加权平均月收益
        temp[j - 1] += Yr_port_return
    start += 12
for i in range(10):
    Rt_VWs.append(temp[i]/13 * 100)


# Compute log-ME

log_MEs = []
temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

start = 66
for i in range(13):
    end = start + 12
    size_data = sizeall.iloc[start]
    size_quantile = pd.qcut(size_data,10,labels = label_size)
    grouped = size_data.groupby([size_quantile])
    Yr_port_ME = grouped.mean() # equal-weighted
    MEList = []
    for j in dict(Yr_port_ME).keys():
        MEList.append(dict(Yr_port_ME)[j])
    MEArray = np.array(MEList)
    MEArray = np.log(MEArray)
    for m in range(1, 11):
        temp[m - 1] += MEArray[m - 1]
    start += 12
for i in range(10):
    log_MEs.append(temp[i]/13)


# Compute log-BM

log_BMs = []
temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

start = 66
for i in range(13):
    end = start + 12
    size_data = sizeall.iloc[start]
    BM_data = mon_BM.iloc[start]
    size_quantile = pd.qcut(size_data,10,labels = label_size)
    grouped = BM_data.groupby([size_quantile])
    Yr_port_BM = grouped.mean() # equal-weighted
    BMList = []
    for j in dict(Yr_port_BM).keys():
        BMList.append(dict(Yr_port_BM)[j])
    BMArray = np.array(BMList)
    BMArray = np.log(BMArray)
    for m in range(1, 11):
        temp[m - 1] += BMArray[m - 1]
    start += 12
for i in range(10):
    log_BMs.append(temp[i]/13)


# Compute R_1 (returns on January) with equal-weighted porfolios

R_1s = []
temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

start = 66
for i in range(12):
    end = start + 12
    size_data = sizeall.iloc[start]
    yield_data = mon_return.iloc[start + 7]
    size_quantile = pd.qcut(size_data,10,labels = label_size)
    grouped = yield_data.groupby([size_quantile])
    Yr_port_Rt = grouped.mean() # equal-weighted
    for m in range(1, 11):
        temp[m - 1] += Yr_port_Rt['Group%d'%m]
    start += 12
for i in range(10):
    R_1s.append(temp[i]/12 * 100)


# Compute R_12 (returns on December) with equal-weighted porfolios

R_12s = []
temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

start = 66
for i in range(13):
    end = start + 12
    size_data = sizeall.iloc[start]
    yield_data = mon_return.iloc[start + 6]
    size_quantile = pd.qcut(size_data,10,labels = label_size)
    grouped = yield_data.groupby([size_quantile])
    Yr_port_Rt = grouped.mean() # equal-weighted
    for m in range(1, 11):
        temp[m - 1] += Yr_port_Rt['Group%d'%m]
    start += 12
for i in range(10):
    R_12s.append(temp[i]/13 * 100)


# Compute Mon_Illiq

Mon_Illiqs = []
temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

start = 66
for i in range(13):
    end = start + 12
    size_data = sizeall.iloc[start]
    Illiq_data = mon_Illiq[start:end]
    size_quantile = pd.qcut(size_data,10,labels = label_size)
    grouped = Illiq_data.groupby([size_quantile],axis = 1)
    Mon_port_lq = grouped.mean() # equal-weighted
    for m in range(1, 11):
        Yr_port_Illiq = Mon_port_lq['Group%d'%m].mean()
        temp[m - 1] += Yr_port_Illiq
    start += 12
for i in range(10):
    Mon_Illiqs.append(temp[i]/13)

table1 = {'Rt_EW': Rt_EWs, 'Rt_VW': Rt_VWs, 'log_ME': log_MEs, 'log_BM': log_BMs, 'R_1': R_1s, 'R_12': R_12s, 'Mon_Illiq': Mon_Illiqs}
table1 = pd.DataFrame(table1, index = port)
table1.to_csv('table1.csv')
