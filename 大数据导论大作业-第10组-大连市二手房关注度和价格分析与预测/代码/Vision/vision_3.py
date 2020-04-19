import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import types
from math import isnan
import os
import sys

path = os.path.abspath(os.path.dirname(sys.argv[0]))
data = pd.read_csv(path + '/output.csv')
result = data.corr('spearman')
#result.to_csv('/Users/zhaowenbo/Desktop/result.csv', sep=',', index=True, header=True)
GGG = result['关注房源人数'][1:]
#print(GGG)
numCo = GGG.shape[0]
print(numCo)



plt.axes(polar=True)

# 数据：角度和极径
theta = np.arange(0, 2*np.pi, 2*np.pi/numCo)  # 角度数据

radii = GGG  #极径数据

# 作图, width表示极区所占的区域
plt.bar(theta,radii, width=(2*np.pi/numCo))

for i in range(0,numCo):
    #plt.text(theta[i], radii[i]+0.01,round(radii[i],2))
    plt.text(theta[i], radii[i]+0.01, i+1)

plt.show();
