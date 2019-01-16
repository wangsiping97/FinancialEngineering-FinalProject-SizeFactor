# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame,Series
import scipy.io as sio
import numpy as np
from datetime import datetime
import statsmodels.api as sm
from scipy.stats import mstats
import math

data = sio.loadmat("CaseDataAll.mat")
market_data = pd.read_csv('market.csv')

mon_yield = data['Mon_Yield']
mon_yield_1 = data['Mon_Yield_1']
sizeall = data['Mon_SizeAll']
sizeflt = data['Mon_SizeFlt']
code = np.squeeze(data['a_Code'])
market_return = market_data['Mkt_Rf']
lag_market = market_return.shift()
risk_free = market_data['rf']                          #读入数据

mon_return = DataFrame(mon_yield, columns = code)
sizeall = DataFrame(sizeall, columns = code)
sizeflt = DataFrame(sizeflt, columns = code)
mon_yield_1 = DataFrame(mon_yield_1, columns = code)   #整理成dataframe


label_size = ['size-%d' %x for x in range(1,11)]
label_beta = ['beta-%d' %x for x in range(1,11)]

port = []
for i in range(1,11):
	for j in range(1,11):
		x = ('size-%d' %i, 'beta-%d' %j) 
		port.append(x)                                 #100个size-β组合的标签
		
post_yield = DataFrame(columns = port)
post_beta = DataFrame(columns = mon_return.columns)

start = 78

for i in range(11):
	start += 12
	end = start + 12
	betas = []
	market = market_return[start-30:start]
	lagged = lag_market[start-30:start]
	rf = risk_free[start-30:start]                     #用前30个月份的数据进行回归
	x1 = market 
	x2 = lagged
	x1 = sm.add_constant(x1)
	x2 = sm.add_constant(x2)                      
	for j in range(len(mon_return.columns)):
		used = mon_return.iloc[start-30:start,j]
		if(used.dropna().count() < 8):
			betas.append(np.nan)
			continue                                   #如果前30个月份中有效数据少于8条则会导致结果不准确，跳过该条数据
		y = used - rf
		est1 = sm.OLS(y,x1,missing = 'drop').fit()
		est2 = sm.OLS(y,x2,missing = 'drop').fit()
		beta = est1.params[1] + est2.params[1]         #分别对市场收益及滞后一期的市场收益进行回归，相加得到最后结果
		betas.append(beta)
	betas = Series(betas,index = mon_return.columns)
	size_data = sizeall.ix[start]
	yield_data = mon_return[start:end]
	size_quantile = pd.qcut(size_data,10,labels = label_size)
	beta_quantile = pd.qcut(betas,10,labels = label_beta)
	grouped = yield_data.groupby([size_quantile,beta_quantile],axis = 1)  #按照size和β分组
	result = grouped.mean()                            #计算每组中股票月收益率的平均值
	piece = dict(list(grouped))
	for item in piece.keys():
		for stock in piece[item].columns:
			post_beta.loc[i,stock] = item              #记录每个时间点每只股票所在的组
			
	using = DataFrame(columns = port)
	for m in range(1,11):
		for n in range(1,11):
			index = ('size-%d' %m, 'beta-%d' %n)
			a = 'size-%d' %m
			b = 'beta-%d' %n
			using[index] = result[a][b]                
	post_yield = post_yield.append(using)              #记录每组的月收益率平均值
post_yield.to_csv('post_yield.csv')
post_beta.to_csv('post_beta.csv')



post_yield = pd.read_csv('post_yield.csv',index_col = 0)
post_beta = pd.read_csv('post_beta.csv',index_col = 0)

port = []
for i in range(1,11):
	for j in range(1,11):
		x = "('size-%d', 'beta-%d')" %(i,j) 
		port.append(x)
		
post_ranking = Series(index = port)

for m in range(1,11):
	for n in range(1,11):	
		index = "('size-%d', 'beta-%d')" %(m,n)
		rf = risk_free[90:222]
		y = post_yield[index] - rf
		x = market_return[90:222]
		x = sm.add_constant(x)
		est = sm.OLS(y,x,missing = 'drop').fit()
		post_ranking[index] = est.params[1]           #计算每组的post-ranking β
				
dic = post_ranking.to_dict()          
post_beta.replace(dic,inplace = True)                 #利用字典映射将post-ranking β分配给个股

post_betas = DataFrame(columns = post_beta.columns)
for i in range(11):
	for j in range(12):
		post_betas = post_betas.append(post_beta.ix[i],ignore_index = True)
post_betas.index = range(90,222)
post_betas.to_csv('post_betas.csv')







