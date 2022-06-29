"""
    程序功能：处理原始数据集
    时间：2021.12.15
"""
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import seaborn as sns

# 提取歌手信息和对应编号
def Songer_Infos():
    df = pd.read_table("data/artists.dat",quoting=csv.QUOTE_NONE)
    df[['id','name']].to_csv('data/歌手信息.csv')

# 判断听歌次数的频繁性
def Listen_Count():
    df = pd.read_table("data/user_artists.dat",quoting=csv.QUOTE_NONE)
    cond = df[(df['weight'] < 1000)]
    sns.set_style('whitegrid')
    plt.figure(1)
    sns.boxplot(cond['weight'])
    plt.figure(2)
    sns.boxplot(df['weight'])
    plt.show()

# 筛选数据 并生成符合数据格式的数据集
def DataTreatment():
    data = np.array(pd.read_table('data/user_artists.dat', quoting=csv.QUOTE_NONE))
    fabe = []
    with open('outputdata/SongList.csv', 'w', encoding='utf-8', newline='') as f:
        csv_write = csv.writer(f)
        for i in range(data.shape[0]):
            if i and (data[i,0] != data[i-1,0]):
                if len(fabe):
                    csv_write.writerow(fabe)
                fabe = []
            if data[i,2] > 89:
                fabe.append(data[i,1])

# 数据集的基本信息
def DataSta():
    df = pd.read_table('data/user_artists.dat', quoting=csv.QUOTE_NONE)
    df.describe().to_excel('data/Describe.xls')

if __name__ == '__main__':
    DataSta()
