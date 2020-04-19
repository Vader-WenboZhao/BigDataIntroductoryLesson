import os
import sys

from Pre import pretreatment_1
from 梯户比计算 import pretreatment_2
from DeleteNan import pretreatment_3
from temp import pretreatment_4

path = os.path.abspath(os.path.dirname(sys.argv[0]))
f=open(path + '/beike.csv')

data1 = pretreatment_1(f)
data2 = pretreatment_2(data1)
data3 = pretreatment_3(data2)
data4 = pretreatment_4(data3)


data4.to_csv(path + '/output.csv', sep=',', index=False, header=True)
f.close()
