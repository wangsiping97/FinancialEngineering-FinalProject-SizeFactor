# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame
import scipy.io as sio
import numpy as np
import statsmodels.api as sm


data = sio.loadmat("CaseDataAll.mat")
market_data = pd.read_csv('ThreeFactorData.csv',index_col = 0)
mon_yield = data['Mon_Yield']
sizeall = data['Mon_SizeAll']
sizeflt = data['Mon_SizeFlt']
code = np.squeeze(data['a_Code'])
mon_yield = DataFrame(mon_yield, columns = code)
sizeall = DataFrame(sizeall, columns = code)
sizeflt = DataFrame(sizeflt, columns = code)
mon_yield = mon_yield[60:222]
sizeall = sizeall[60:222]
sizeflt = sizeflt[60:222]
mon_yield.index = range(len(mon_yield.index))
sizeall.index = mon_yield.index
sizeflt.index = mon_yield.index
market_data.index = mon_yield.index                         #整理数据

label_size = ['size-%d' %x for x in range(1,11)]
return_all = DataFrame(columns = label_size)
return_flt = DataFrame(columns = label_size)
start = 0
for i in range(14):	
	end = start + 12                                            #每年调整一次组合
	if end > 156:
		end = 162
	size_all = sizeall.ix[i]
	yield_data = mon_yield[start:end]
	sizeall_quantile = pd.qcut(size_all,10,labels = label_size) #按照size划分投资组合
	grouped1 = yield_data.groupby(sizeall_quantile,axis = 1)    #此处为总市值
	result1 = grouped1.mean()                                   #计算每组的月收益率平均值
	return_all = return_all.append(result1)
	
	size_flt = sizeflt.ix[i]
	sizeflt_quantile = pd.qcut(size_flt,10,labels = label_size) #此处为流通市值
	grouped2 = yield_data.groupby(sizeflt_quantile,axis = 1)
	result2 = grouped2.mean()
	return_flt = return_flt.append(result2)
	start += 12

return_all['high-low'] = return_all['size-10']-return_all['size-1'] 
return_flt['high-low'] = return_flt['size-10']-return_flt['size-1']

label_size.append('high-low')

result_all = DataFrame(index = ['alpha','t-alpha','beta','t-beta'],columns = label_size)
result_flt = DataFrame(index = ['alpha','t-alpha','beta','t-beta'],columns = label_size)

x = market_data['Mkt_Rf']
x = sm.add_constant(x)
for i in range(11):
	y = return_all.iloc[:,i]
	est = sm.OLS(y,x,missing = 'drop').fit()            #对每个组合做一次回归
	result_all.iloc[0,i] = est.params[0]                #此处为用总市值的结果
	result_all.iloc[1,i] = est.params[0]/est.bse[0]
	result_all.iloc[2,i] = est.params[1]
	result_all.iloc[3,i] = est.params[1]/est.bse[1]

	
for i in range(11):
	y = return_flt.iloc[:,i]                            #此处为用流通市值的结果
	est = sm.OLS(y,x,missing = 'drop').fit()
	result_flt.iloc[0,i] = est.params[0]
	result_flt.iloc[1,i] = est.params[0]/est.bse[0]
	result_flt.iloc[2,i] = est.params[1]
	result_flt.iloc[3,i] = est.params[1]/est.bse[1]

result_all = result_all.applymap(lambda x: round(x,4))
result_flt = result_flt.applymap(lambda x: round(x,4))
result_all.to_csv('table3_all.csv')
result_flt.to_csv('table3_flt.csv')

	
	

