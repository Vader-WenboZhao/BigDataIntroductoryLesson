# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 22:06:20 2019

@author: Han_y1
"""

import pandas as pd
import numpy as npy
import matplotlib.pylab as pyl
import os
import sys

from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO


from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB

from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


path = os.path.abspath(os.path.dirname(sys.argv[0]))
data = pd.read_csv(path + "/output.csv")
dataT = data.T
#print(data.values[0])

sr = data['关注房源人数']

#去掉$符号
data['建筑类型'] = data['建筑类型'].str.replace('$','')
data['小区名称'] = data['小区名称'].str.replace('$','')
data['所在小区域'] = data['所在小区域'].str.replace('$','')
#print(data.iloc[:,[9,11,12]])


#用K-means聚类算法把连续数据离散化
#把关注房源人数离散化 分成4类：极少，少，一般，多
data_people_num = data['关注房源人数'].copy()

k = 4

kmodel = KMeans(n_clusters = k, n_jobs = 1)#n_jobs是并行数，一般等于CPU数
kmodel.fit(data_people_num.values.reshape(len(data_people_num), 1))
c = pd.DataFrame(kmodel.cluster_centers_).sort_values(by=0)
#rolling_mean表示移动平均，即用当前值和前2个数值取平均数，
#由于通过移动平均，会使得第一个数变为空值，因此需要使用.iloc[1:]过滤掉空值。
w = c.rolling(2).mean().iloc[1:] #相邻两项求中点，作为边界点

w = [0] + list(w[0]) + [data_people_num.max()] #把首末边界点加上

dPNum = pd.cut(data_people_num,w,labels=range(k))


def cluster_plot_Pnum(d,k):
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize = (12,4))
    for j in range(0,k):
        plt.plot(data_people_num[d==j], [j for i in d[d==j]],'o')

    plt.ylim(-0.5, k-0.5)
    return plt

cluster_plot_Pnum(dPNum, k).show()

#用等宽离散处理关注房源人数
#k = 5
#d1 = pd.cut(data_people_num,k,labels = range(k))


#def cluster_plot(d,k):
#    import matplotlib.pyplot as plt
#    plt.rcParams['font.sans-serif'] = ['SimHei']
#    plt.rcParams['axes.unicode_minus'] = False

#    plt.figure(figsize = (12,4))
#    for j in range(0,k):
#        plt.plot(data_people_num[d==j], [j for i in d[d==j]],'o')

#    plt.ylim(-0.5, k-0.5)
#    return plt

#cluster_plot(d1, k).show()

#把分类结果修改到原数据中

data['关注房源人数'] = dPNum.map(lambda x:x)
#print(data)

#用K-means聚类法 把平米价离散化

data_price = data['平米价'].copy()

k = 6

kmodel = KMeans(n_clusters = k, n_jobs = 1)
kmodel.fit(data_price.values.reshape(len(data_price), 1))
c = pd.DataFrame(kmodel.cluster_centers_).sort_values(by=0)

w = c.rolling(2).mean().iloc[1:] #相邻两项求中点，作为边界点
w = [0] + list(w[0]) + [data_price.max()] #把首末边界点加上

dPrice = pd.cut(data_price,w,labels=range(k))

def cluster_plot_price(d,k):
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize = (12,4))
    for j in range(0,k):
        plt.plot(data_price[d==j], [j for i in d[d==j]],'o')

    plt.ylim(-0.5, k-0.5)
    return plt

cluster_plot_price(dPrice, k).show()

data['平米价'] = dPrice.map(lambda x:x)


#对面积进行离散化

data_area = data['面积'].copy()

k = 6

kmodel = KMeans(n_clusters = k, n_jobs = 1)
kmodel.fit(data_area.values.reshape(len(data_area), 1))
c = pd.DataFrame(kmodel.cluster_centers_).sort_values(by=0)

w = c.rolling(2).mean().iloc[1:] #相邻两项求中点，作为边界点
w = [0] + list(w[0]) + [data_area.max()] #把首末边界点加上

dArea = pd.cut(data_area,w,labels=range(k))

def cluster_plot_area(d,k):
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize = (12,4))
    for j in range(0,k):
        plt.plot(data_area[d==j], [j for i in d[d==j]],'o')

    plt.ylim(-0.5, k-0.5)
    return plt

cluster_plot_area(dArea, k).show()

data['面积'] = dArea.map(lambda x:x)


#把梯户比分成高低两类 高为1，低为0
def change(x):
    if (x >= 0.9):
        return 10
    elif x >= 0.8:
        return 9
    elif x >= 0.7:
        return 8
    elif x >= 0.6:
        return 7
    elif x >= 0.5:
        return 6
    elif x >= 0.4:
        return 5
    elif x >= 0.3:
        return 4
    elif x >= 0.2:
        return 3
    elif x >= 0.1:
        return 2
    elif x >= 0:
        return 1
    else:
        return 0
data['梯户比例'] = data['梯户比例'].map(lambda x:change(x))

#把建造时间分成长和短 短为1 长为0
def change_buildTime(x):
    if (x >= 2000):
        return 1
    else:
        return 0
data['建造时间'] = data['建造时间'].map(lambda x:change_buildTime(x))

#把精简装分用数字表示 精0 简1 毛2 其3
def change_decorate(x):
    if x == "精":
        return 0
    elif x == "简":
        return 1
    elif x == "毛":
        return 2
    else:
        return 3

data['精简装'] = data['精简装'].map(lambda x:change_decorate(x))
#print(data['精简装'].value_counts())

#把建筑类型用数字表示 板楼0 塔楼1 板塔结合2


def change_buildType(x):
    if x == "板楼":
        return 0
    elif x == "塔楼":
        return 1
    else:
        return 2
data['建筑类型'] = data['建筑类型'].map(lambda x:change_buildType(x))
#print(data['建筑类型'].value_counts())

#把地铁公交轻轨合并成交通
data['交通'] = data['地铁'] + data['公交'] + data['轻轨']
#print(data['交通'])

#把海景购物银行饭店休闲合并成娱乐
data['娱乐'] = data['海景'] + data['购物'] + data['银行'] + data['饭店'] + data['休闲']
#print(data['娱乐'])

#把户型结构用数字表示 平0 跃1 复2 错3

def change_familyStruc(x):
    if x == "平层":
        return 0
    elif x == "跃层":
        return 1
    elif x == "复式":
        return 2
    elif x == "错层":
        return 3
    else:
        return 0
data['户型结构'] = data['户型结构'].map(lambda x:change_familyStruc(x))
#print(data['户型结构'].value_counts())

#把产权年限转换成数字 70 0 50 1 40 2


def change_propertyYear(x):
    if x == 70:
        return 0
    elif x == 50:
        return 1
    else:
        return 2

data['产权年限'] = data['产权年限'].map(lambda x:change_propertyYear(x))
#print(data['产权年限'].value_counts())

#把所在大区域用数字表示 甘井子0 沙河口1 中山2 高新园区3 金州4 西岗5 旅顺口6 普兰店7 开发区 8

def change_local(x):
    if x == "甘井子":
        return 0
    elif x == "沙河口":
        return 1
    elif x == "中山":
        return 2
    elif x == "高新园区":
        return 3
    elif x == "金州":
        return 4
    elif x == "西岗":
        return 5
    elif x == "旅顺口":
        return 6
    elif x == "普兰店":
        return 7
    elif x == "开发区":
        return 8

data['所在大区域'] = data['所在大区域'].map(lambda x:change_local(x))

#print(data['所在大区域'].value_counts())

#去掉有nan的行
data = data.dropna(axis = 0)


#把处理好的数据输出
data.to_csv("C:\\Users\\Han_y1\\Desktop\\data.csv",sep = ',', index = False, header = True)



#用平米价，精简装，面积，建造时间，所在大区域，建筑类型，户型结构，产权年限，交通，梯户比例，
#休闲，学区这几个属性进行数据挖掘，找到对关注房源人数影响最大的因素


x = data.iloc[:, [2,3,4,5,9,11,13,16,17,28,29,25]].as_matrix()
y = data.iloc[:,0].as_matrix()


xf = pd.DataFrame(x)
yf = pd.DataFrame(y)


x2 = xf.as_matrix().astype(int)
y2 = yf.as_matrix().astype(int)

#建立决策树

dtc = DTC(criterion="entropy")
dtc.fit(x2, y2)


with open("C:\\Users\\Han_y1\\Desktop\\dtc.dot", "w") as file:
    # 参数为：模式、特征值（实战、课时数、是否促销、是否提供配套资料）
    export_graphviz(dtc, feature_names=["平米价", "精简装", "面积", "建造时间", "所在大区域"
                                        , "建筑类型", "梯户类型", "产权年限", "户型结构", "交通"
                                        , "休闲", "学区"], out_file=file)

#print(data)


#使用贝叶斯分类器


Alldata=[]
traffic_feature=[]
traffic_target=[]


x = data.iloc[:, [0,2,3,4,5,9,11,13,16,17,28,29,25]].as_matrix()

xFrame = pd.DataFrame(x)

for indexs in xFrame.index:
    Alldata.append(xFrame.loc[indexs].values[0:-1])
    traffic_feature.append(xFrame.loc[indexs].values[1:13])
    traffic_target.append(xFrame.loc[indexs].values[0])

#print('data=',Alldata)
#print('traffic_feature=',traffic_feature)
#print('traffic_target=',traffic_target)



scaler = StandardScaler() # 标准化转换
scaler.fit(traffic_feature)  # 训练标准化对象
traffic_feature= scaler.transform(traffic_feature)   # 转换数据集

feature_train, feature_test, target_train, target_test = train_test_split(
        traffic_feature, traffic_target, test_size=0.3,random_state=0)


NB=BernoulliNB()
NB.fit(feature_train,target_train)

predict_results=NB.predict(feature_test)


print(NB.score(feature_test,target_test)) #预测结果与实际结果准确程度

#print('------------')
#print(accuracy_score(predict_results, target_test))
conf_mat = confusion_matrix(target_test, predict_results) #混淆矩阵 表明类别是否被混淆 对角线上的元素是被正确识别的数量
print(conf_mat)
#print('------------')
#print(classification_report(target_test, predict_results))





#print(xFrame)
