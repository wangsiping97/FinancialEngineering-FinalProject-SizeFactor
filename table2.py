# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame,Series
import scipy.io as sio
import numpy as np
import math

data = sio.loadmat("CaseDataAll.mat")
market_data = pd.read_csv('market.csv')
post_yield = pd.read_csv('post_yield.csv',index_col = 0)
post_betas = pd.read_csv('post_betas.csv',index_col = 0)

sizeall = data['Mon_SizeAll']
mon_yield = data['Mon_Yield']
code = np.squeeze(data['a_Code'])
market_return = market_data['Mkt_Rf']
lag_market = market_return.shift()
risk_free = market_data['rf']
sizeall = DataFrame(sizeall, columns = code).applymap(np.log)
mon_return = DataFrame(mon_yield, columns = code)             #整理数据

label_size = ['size-%d' %x for x in range(1,11)]
label_beta = ['beta-%d' %x for x in range(1,11)]

mean = post_yield.mean()*100
stdev = post_yield.std()
t_value = mean*math.sqrt(132)/(100*stdev)
mean.index = range(100)
t_value.index=range(100)
frame1 = pd.DataFrame(columns = label_size,index = label_beta) #用于记录月回报率
frame2 = pd.DataFrame(columns = label_size,index = label_beta) #用于记录t值
frame1['max_min'] = 0
frame2['max_min'] = 0
for i in range(10):
	for j in range(10):
		frame1.iloc[j,i] = mean[10*i+j]                        #将文件post_yield.csv中的数据记录到dataframe中
		frame2.iloc[j,i] = t_value[10*i+j]
for i in range(10):
	max_min = post_yield.iloc[:,90+i]-post_yield.iloc[:,i] #计算size最大和最小组的月回报率的差
	average = max_min.mean()
	t = average*math.sqrt(132)/max_min.std()
	frame1.iloc[i,10] = average*100
	frame2.iloc[i,10] = t

start = 78
m = DataFrame(columns = label_size)	
for i in range(11):                                #计算只用size分组时的月回报率，即average over beta一行
	start += 12
	end = start + 12
	size_data = sizeall.ix[start]
	yield_data = mon_return[start:end]
	size_quantile = pd.qcut(size_data,10,labels = label_size) #根据size大小分为10组
	grouped = yield_data.groupby(size_quantile,axis = 1) #按照size进行分组
	result = grouped.mean()
	m = m.append(result)
m['max_min'] = m['size-10']-m['size-1']
mean = m.mean()
m_std = m.std()
mean_t = mean*math.sqrt(132)/m_std
frame1 = frame1.append(mean*100,ignore_index = True)
frame2 = frame2.append(mean_t,ignore_index = True)
frame1 = frame1.applymap(lambda x: round(x,4))           #保留4位小数
frame2 = frame2.applymap(lambda x: round(x,3))           #保留3位小数
label_beta.append('Average over beta')
frame1.index = label_beta
frame2.index = label_beta
frame1.to_csv('table2_return.csv')
frame2.to_csv('table2_tvalue.csv')