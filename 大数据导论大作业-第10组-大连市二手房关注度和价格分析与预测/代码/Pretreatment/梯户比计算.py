import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import types
import C2N as c2n
import string
import os
import sys
import time

def pretreatment_2(s):

    # 如果用pandas打不开数据，可以使用记事本打开把编码格式改成utf-8另存
    data = s
    # type(data) = <class 'pandas.core.frame.DataFrame'>
    # print(data.shape)
    # print(data.keys())


    data['梯户比例'] = 0;
    data['梯户比例'] = data['梯户比例'].astype(float)
    numTHB = data['梯户比例'].shape[0]
    for p in range(0, numTHB):
        if(isinstance(data['梯'][p], float) and isinstance(data['户'][p], float)):
            data['梯户比例'][p] = data['梯'][p]/data['户'][p]
            if(data['梯户比例'][p] == 0.0):
                print(data['梯'][p]/data['户'][p])
            #print(data['梯户比例'][p])
        else:
            pass
        if(p%100 == 0):
            print(p)

    print("\n\n\n************Step2 is finished**********\nPlease waiting for seconds\n")
    time.sleep(5)

    return data
