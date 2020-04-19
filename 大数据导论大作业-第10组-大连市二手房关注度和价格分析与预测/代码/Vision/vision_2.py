from folium.plugins import HeatMap
import folium
import webbrowser
import pandas as pd
import numpy as np
import plotly_express as px
import os
import sys

latitude = 38.9
longitude = 121.5

path = os.path.abspath(os.path.dirname(sys.argv[0]))
#  读取csv文件,以Dataframe形式保存
df = pd.read_csv(path + "/new.csv")
#  获取数据个数
num = df.shape[0]
#  获取纬度
lat = np.array(df["纬度"][0:num])
#  获取经度
lon = np.array(df["经度"][0:num])
#  获取数据，转化为numpy浮点型
price = np.array(df["平米价"][0:num], dtype=float)
people = np.array(df["关注房源人数"][0:num], dtype=float)
#  将数据制作成[lats, lons, weights]的形式
data1 = [[lat[i], lon[i], price[i]] for i in range(num)]
data2 = [[lat[i], lon[i], people[i]] for i in range(num)]
#  绘制Map
map_house1 = folium.Map(location=[latitude, longitude], zoom_start=11)
map_house2 = folium.Map(location=[latitude, longitude], zoom_start=11)

#  将热力图添加到前面建立的map里
HeatMap(data1, radius=7, gradient={.4: 'blue', .65: 'lime', 1: 'red'}).add_to(map_house1)
# 保存并显示热力图
map_house1.save(path + "1.html")
webbrowser.open("1.html")

#  将热力图添加到前面建立的map里
HeatMap(data2, radius=7, gradient={.2: 'lime', .5: 'orange', 1: 'red'}).add_to(map_house2)
# 保存并显示热力图
map_house2.save(path + "2.html")
webbrowser.open("2.html")

# 平行坐标图
df_simple = df[['关注房源人数', '总价', '平米价', '精简装', '建造时间', '室', '厅', '所在大区域', '建筑类型', '梯户比例']][0:100]
fig = px.parallel_categories(df_simple, color="关注房源人数", color_continuous_scale=px.colors.sequential.Inferno)
fig.show()

# 散点图
fig = px.scatter(df_simple, x="总价", y="关注房源人数", color="所在大区域", marginal_y="rug", marginal_x="histogram")
fig.show()

#
