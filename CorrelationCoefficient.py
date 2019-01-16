# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame,Series
import scipy.io as sio
import numpy as np
import math

data = sio.loadmat("CaseDataAll.mat")
post_betas = pd.read_csv('post_betas.csv',index_col = 0)


sizeall = data['Mon_SizeAll']
code = np.squeeze(data['a_Code'])
sizeall = DataFrame(sizeall, columns = code).applymap(np.log)
post_betas.columns = sizeall.columns
label_size = ['size-%d' %x for x in range(1,11)]

betas = DataFrame(columns = label_size)
sizes = DataFrame(columns = label_size)

now = 78
for i in range(11):
	now += 12
	size_data = sizeall.ix[now]
	beta_data = post_betas.ix[now]
	size_quantile = pd.qcut(size_data,10,labels = label_size)
	grouped_beta = beta_data.groupby(size_quantile)  #将β按照size的大小分组聚合
	result_beta = grouped_beta.mean()
	grouped_size = size_data.groupby(size_quantile)  #将size按照size的大小分组聚合
	result_size = grouped_size.mean()
	betas = betas.append(result_beta,ignore_index = True)
	sizes = sizes.append(result_size,ignore_index = True)
mean_beta = betas.mean()                             #计算各组β的平均值
mean_size = sizes.mean()                             #计算各组size的平均值
print(mean_beta)
print(mean_size)
print(mean_beta.corr(mean_size))                     #计算size和beta的相关系数

	
	



	