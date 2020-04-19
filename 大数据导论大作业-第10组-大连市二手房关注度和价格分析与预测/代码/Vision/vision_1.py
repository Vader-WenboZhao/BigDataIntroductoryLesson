import time
import pandas as pd
import requests
import json
import os
import sys

path = os.path.abspath(os.path.dirname(sys.argv[0]))
MyAk = '9gNwTYH6759sGn7e7nPtlYZuFQTTvZXd'
src = path + '/output.csv'


class Position:
    lng = 0.0
    lat = 0.0

    def __init__(self, lng, lat):
        self.lng = lng
        self.lat = lat


def get_mercator(addr):
    url = 'http://api.map.baidu.com/geocoding/v3/?address=%s&city=大连市&output=json&ak=9gNwTYH6759sGn7e7nPtlYZuFQTTvZXd' % (
        addr)
    response = requests.get(url)
    data = json.loads(response.text)
    # print(data)
    if data['status'] == 0:
        position = Position(data['result']['location']['lng'], data['result']['location']['lat'])
        return position
    else:
        position = Position(0, 0)
        return position


def csv_read_write():
    data = pd.read_csv(src)
    col = len(data.columns)
    data.insert(col, '经度', '')
    data.insert(col + 1, '纬度', '')

    for i in data.index:
        position = get_mercator(data.at[i, '小区名称'])
        data.at[i, '经度'] = position.lng
        data.at[i, '纬度'] = position.lat
        print(i)
    data.to_csv(path + "/new.csv", mode='a', index=False)
    # mode=a，以追加模式写入,header表示列名，默认为true,index表示行名，默认为true，再次写入不需要行名


csv_read_write()
