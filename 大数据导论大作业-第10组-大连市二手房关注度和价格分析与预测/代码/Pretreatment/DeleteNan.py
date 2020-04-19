import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import types
import C2N as c2n
from math import isnan
import os
import sys
import time


def pretreatment_3(s):

    # 如果用pandas打不开数据，可以使用记事本打开把编码格式改成utf-8另存
    data = s

    #处理空值
    numJZLX = data['建筑类型'].shape[0]
    for j in range(0, numJZLX):
        if(isinstance(data['建筑类型'][j], float)):
            data['建筑类型'][j] = "未知$"
        else:
            pass
        if(j%100 == 0):
            print(j)

    numT = data['梯'].shape[0]
    for i in range(0, numT):
        if(isnan(data['梯'][i])):
            data['梯'][i] = 0.0
        else:
            pass
        if(i%100 == 0):
            print(i)

    numH = data['户'].shape[0]
    for j in range(0, numH):
        if(isnan(data['户'][j])):
            data['户'][j] = 0.0
        else:
            pass
        if(j%100 == 0):
            print(j)

    numTHB = data['梯户比例'].shape[0]
    for k in range(0, numTHB):
        if(isnan(data['梯户比例'][k])):
            data['梯户比例'][k] = 0.0
        else:
            pass
        if(k%100 == 0):
            print(k)

    numCQNX = data['产权年限'].shape[0]
    for k in range(0, numCQNX):
        if(isnan(data['产权年限'][k])):
            data['产权年限'][k] = '0.0'
        else:
            pass
        if(k%100 == 0):
            print(k)

    print("\n\n\n************Step3 is finished**********\nPlease waiting for seconds\n")
    time.sleep(5)


    return data
