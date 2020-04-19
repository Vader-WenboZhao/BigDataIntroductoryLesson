import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import types
import C2N as c2n
import string
from math import isnan
import os
import sys
import time

# '/Users/zhaowenbo/Downloads/beike.csv'
def pretreatment_4(s):

    # 如果用pandas打不开数据，可以使用记事本打开把编码格式改成utf-8另存
    data = s
    # type(data) = <class 'pandas.core.frame.DataFrame'>
    # print(data.shape)
    # print(data.keys())


    print(data.info())
    #print(data['房源特色'][11].find('银行'))


    data['精简装'] = data['精简装'].str.extract(r'/(.+?)')  # 提取关键字

    # 使用pd.get_dummies() 量化数据
    data_decoration = pd.get_dummies(data['精简装'])
    data_decoration.head()


    # 使用pd.concat矩阵拼接，axis=1：水平拼接
    data = pd.concat([data, data_decoration], axis=1)


    #data['房源特色'][i]

    print("\n\n\n************Step4 is finished**********\nPlease waiting for seconds\n")
    time.sleep(5)


    return data
