"""
   程序功能： 将编号替换成歌手信息
   作者：覃瀚辉
   时间：2021.12.15
"""
import pandas as pd
import numpy as np
import csv
# 数据读入阶段
shop_game = np.array(pd.read_csv("outputdata/shop_game.csv",header=None))
possible = np.array(pd.read_csv("outputdata/possible.csv",header=None))
artist = np.array(pd.read_table('data/artists.dat',quoting=csv.QUOTE_MINIMAL))

## 把关联规则左边的替换
with open('outputdata/like_song.csv', 'w', encoding='utf-8', newline='') as f:
    csv_writer = csv.writer(f)
    for i in range(shop_game.shape[0]):
        data = []
        for j in range(shop_game.shape[1]):
            if np.isnan(shop_game[i,j]):
                break
            # 替换成名字
            else:
                data.append(artist[artist[:,0] == shop_game[i,j]][0, 1])
        print(i)
        csv_writer.writerow(data)

## 关联规则右边的替换
with open('outputdata/tuijian_song.csv', 'w', encoding='utf-8', newline='') as f:
    csv_writer = csv.writer(f)
    for i in range(possible.shape[0]):
        data = []
        for j in range(possible.shape[1]):
            if np.isnan(possible[i,j]):
                break
            # 替换成名字
            else:
                data.append(artist[artist[:,0] == possible[i,j]][0, 1])
        print(i)
        csv_writer.writerow(data)

# 默认推荐
possible = np.array(pd.read_csv("outputdata/tuijian2.csv",header=None))
with open('outputdata/tuijian_default.csv', 'w', encoding='utf-8', newline='') as f:
    csv_writer = csv.writer(f)
    for i in range(possible.shape[0]):
        data = []
        for j in range(possible.shape[1]):
            if np.isnan(possible[i,j]):
                break
            # 替换成名字
            else:
                data.append(artist[artist[:,0] == possible[i,j]][0, 1])
        print(i)
        csv_writer.writerow(data)