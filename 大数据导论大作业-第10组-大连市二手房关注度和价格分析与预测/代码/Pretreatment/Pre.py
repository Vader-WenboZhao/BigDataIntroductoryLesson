import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import types
import C2N as c2n
import string
import jieba
from math import isnan
import os
import sys
import time

def pretreatment_1(s):

    # 如果用pandas打不开数据，可以使用记事本打开把编码格式改成utf-8另存
    data = pd.read_csv(s, encoding="'utf-8'")
    print(type(data['户型']))
      # type(data) = <class 'pandas.core.frame.DataFrame'>
    # print(data.shape)
    # print(data.keys())

    # Series的extract支持正则匹配抽取，返回的值是字符串
    data[['室', '厅']] = data['户型'].str.extract(r'(\d+)室(\d+)厅')
    # 把字符串格式转化为float，并删除户型
    data['室'] = data['室'].astype(float)
    data['厅'] = data['厅'].astype(float)
    del data['户型']

    # print(data.keys())
    # print(data)

    # 将建筑面积后的平方米去除，并将数据类型改成浮点型
    data['面积'] = data['面积'].map(lambda e: e.replace('平米', ''))  # Series中的map
    data['面积'] = data['面积'].astype(float)

    # print(data['面积'])

    # 将单价后的元/平米去除，并将数据类型改成浮点型
    data['平米价'] = data['平米价'].map(lambda e: e.replace(r'元/平米', ''))
    data['平米价'] = data['平米价'].astype(float)

    # print(data['平米价'])

    # 将房屋总价后的万去除，并将数据类型改成浮点型
    data['总价'] = data['总价'].map(lambda e: e.replace('万', ''))
    data['总价'] = data['总价'].astype(float)

    # print(data['总价'])

    data['建造时间'] = data['建造时间'].str.extract(r'(.+?)年建')  # 提取关键字
    data['建造时间'] = data['建造时间'].astype(float)


    data['小区名称'] = data['小区'].str.extract(r':(.+?)所在区域')
    #print(data['小区名称'])

    data['所在大区域'] = data['小区'].str.extract(r'所在区域:(.+?) ')
    #print(data['所在大区域'])

    data['所在小区域'] = data['小区'].str.extract(r' (.+?)看房时间')
    #print(data['所在小区域'])

    data[['所在大区域', '所在小区域', '小区名称']] = data['小区'].str.extract(r'小区名称:(.+?)所在区域:(.+?) (.+?)')


    data['建筑类型'] = data['房屋补充信息'].str.extract(r'建筑类型:(.+?)房屋朝向')
    data['建筑结构'] = data['房屋补充信息'].str.extract(r'建筑结构:(.+?)结构')


    data['梯户比例'] = data['房屋补充信息'].str.extract(r'梯户比例:(.+?)供暖方式')
    data['梯'] = data['房屋补充信息'].str.extract(r'梯户比例:(.+?)梯')
    data['户'] = data['梯户比例'].str.extract(r'梯(.+?)户')

    numHu = data['户'].shape[0]
    for i in range(0, numHu):
        if(isinstance(data['户'][i], float)):
            pass
        else:
            data['户'][i] = c2n.chinese2digits(data['户'][i])
        if(i%100 == 0):
            print(i)

    numTi = data['梯'].shape[0]
    for j in range(0, numTi):
        if(isinstance(data['梯'][j], float)):
            pass
        else:
            data['梯'][j] = c2n.chinese2digits(data['梯'][j])
        if(j%100 == 0):
            print(j)


    data['产权年限'] = data['房屋补充信息'].str.extract(r'产权年限:(.+?)年.挂牌时间')
    data['产权年限'] = data['产权年限'].astype(float)
    #print(data.shape)
    #print(data.shape)

    #df[(True-df['产权年限'].isin([2]))]
    #data['产权年限'] = data['产权年限'].astype(float)

    data['楼层'] = data['楼层'].str.extract(r'(.+?)楼层')  # 提取关键字

    # print(data['楼层'])



    data['户型结构'] = data['精简装'].str.extract(r'(.+?)/')
    data['精简装'] = data['精简装'].str.extract(r'/(.+?)')  # 提取关键字

    #print (data['装修'])


    data['海景'] = 0
    data['地铁'] = 0
    data['公交'] = 0
    data['轻轨'] = 0
    data['购物'] = 0
    data['银行'] = 0
    data['饭店'] = 0
    data['学区'] = 0
    data['采光'] = 0
    data['休闲'] = 0
    numFT = data['房源特色'].shape[0]
    for i in range(0, numFT):
        if(isinstance(data['房源特色'][i], float)):
            pass
        else:
            if(data['房源特色'][i].find('海景')!=-1):
                data['海景'][i] = 1
            if(data['房源特色'][i].find('地铁')!=-1):
                data['地铁'][i] = 1
            if(data['房源特色'][i].find('公交')!=-1):
                data['公交'][i] = 1
            if(data['房源特色'][i].find('轻轨')!=-1):
                data['轻轨'][i] = 1
            if(data['房源特色'][i].find('商场')!=-1 or data['房源特色'][i].find('市场')!=-1
                or data['房源特色'][i].find('超市')!=-1 or data['房源特色'][i].find('早市')!=-1
                or data['房源特色'][i].find('夜市')!=-1):
                data['购物'][i] = 1
            if(data['房源特色'][i].find('银行')!=-1):
                data['银行'][i] = 1
            if(data['房源特色'][i].find('饭店')!=-1 or data['房源特色'][i].find('酒店')!=-1):
                data['饭店'][i] = 1
            if(data['房源特色'][i].find('小学')!=-1 or data['房源特色'][i].find('初中')!=-1
                or data['房源特色'][i].find('高中')!=-1 or data['房源特色'][i].find('大学')!=-1
                or data['房源特色'][i].find('学院')!=-1 or data['房源特色'][i].find('学校')!=-1):
                data['学区'][i] = 1
            if(data['房源特色'][i].find('采光')!=-1 or data['房源特色'][i].find('阳光')!=-1
                or data['房源特色'][i].find('光线')!=-1):
                data['采光'][i] = 1
            if(data['房源特色'][i].find('广场')!=-1 or data['房源特色'][i].find('公园')!=-1):
                data['休闲'][i] = 1

        if(i%100 == 0):
            print(i)


    #del data['其']
    del data['小区']
    del data['朝向']
    #del data['精简装']
    del data['楼层']
    del data['网页标题']
    del data['房源标题']
    del data['标题补充']
    del data['在原网站的位置']
    del data['房源特色']
    del data['各房间信息']
    del data['房屋补充信息']

    print("\n\n\n************Step1 is finished**********\nPlease waiting for seconds\n")
    time.sleep(5)


    return data
