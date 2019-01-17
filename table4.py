# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame
import scipy.io as sio
import numpy as np
import statsmodels.api as sm
from scipy.stats import mstats
import math

def dummy(x):
	if x < 0:
		return 1
	elif x >= 0:
		return 0
	else:
		return np.nan                        #计算EP dummy的函数

def EP(x):
	if x > 0:
		return x
	elif x <= 0:
		return 0
	else:
		return np.nan                        #计算EP的函数

data = sio.loadmat("CaseDataAll.mat")
market_data = pd.read_csv('market.csv')

mon_yield = data['Mon_Yield']
mon_yield_1 = data['Mon_Yield_1']
mon_BM = data['Mon_BM']
mon_EP = data['Mon_EP']
mon_turnover = data['Mon_TurnOver']
sizeall = data['Mon_SizeAll']
sizeflt = data['Mon_SizeFlt']
code = np.squeeze(data['a_Code'])
market_return = market_data['Mkt_Rf']
lag_market = market_return.shift()
risk_free = market_data['rf']

mon_return = DataFrame(mon_yield, columns = code)
sizeall = DataFrame(sizeall, columns = code)
sizeflt = DataFrame(sizeflt, columns = code)
mon_yield_1 = DataFrame(mon_yield_1, columns = code)
mon_BM = DataFrame(mon_BM, columns = code)
mon_EP = DataFrame(mon_EP, columns = code)
EP_dummy = mon_EP.applymap(dummy)
mon_EP = mon_EP.applymap(EP)
mon_turnover = DataFrame(mon_turnover, columns = code)  #将数据整理为dataframe格式

mon_BM = mon_BM.apply(mstats.winsorize,limits = [0.005,0.005],axis = 1)
mon_EP = mon_EP.apply(mstats.winsorize,limits = [0.005,0.005],axis = 1)  #缩尾处理

label_size = ['size-%d' %x for x in range(1,11)]
label_beta = ['beta-%d' %x for x in range(1,11)]


post_betas = pd.read_csv('post_betas.csv',index_col = 0)
post_betas.columns = code
size_data = sizeall.shift().ix[90:221].applymap(np.log)     #用市值的对数进行回归
BM_data = mon_BM.shift().ix[90:221]                         #所有解释变量均滞后一期
EP_data = mon_EP.shift().ix[90:221]
EPdummy_data = EP_dummy.shift().ix[90:221]
turnover_data = mon_turnover.shift().ix[90:221]
last_month = mon_yield_1.shift().ix[90:221]
monthly_return = mon_return.ix[90:221]
params = {'alpha':[],'beta':[],'size':[],'BM':[],'EP':[],'EPdummy':[],'turnover':[],'last_month':[]}
for i in range(90,222):
	beta = post_betas.ix[i]
	size = size_data.ix[i]
	BM = BM_data.ix[i]
	EP = EP_data.ix[i]
	EPdummy = EPdummy_data.ix[i]
	turnover = turnover_data.ix[i]
	last = last_month.ix[i]	
	y = monthly_return.ix[i]
	x = pd.concat([beta,size,BM,EP,EPdummy,turnover,last],axis = 1)
	x = sm.add_constant(x)
	est = sm.OLS(y,x,missing = 'drop').fit()           #每月进行横截面回归
	params['alpha'].append(est.params[0])
	params['beta'].append(est.params[1])
	params['size'].append(est.params[2])
	params['BM'].append(est.params[3])
	params['EP'].append(est.params[4])
	params['EPdummy'].append(est.params[5])
	params['turnover'].append(est.params[6])
	params['last_month'].append(est.params[7])

params = DataFrame(params)
mean = params.mean()
error = params.std()/math.sqrt(131)
t = mean/error
frame = pd.concat([mean,t],axis = 1)
frame.columns = ['mean','t-value']
frame.to_csv('table4.csv')









