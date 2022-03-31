"""
    程序功能：获取不同参数下的运行时间,做出比较
            1. 记录不同最小支持度、最小置信度的运行时间
            2. 记录不同数据集相同的运行时间
    作者：覃瀚辉
    时间: 2021.12.15
"""
import pyfpgrowth
import csv
import time
import matplotlib.pyplot as plt
import numpy as np


class GuanRules():
    def __init__(self,min_sup,min_conf):
        # 最小支持度
        self.min_sup = min_sup
        # 最小置信度
        self.min_conf = min_conf
    def loadSimpDat(self):
        """
        生成数据
        :return: 返回生成的数据列表
        """
        dataSet = []
        with open('outputdata/SongList.csv', 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                dataSet.append(row)
        return dataSet

    def run(self):
        """
        求解频繁项集和关联规则
        :return: 返回长度
        """
        with open('outputdata/rules.csv','w',newline='',encoding='utf-8') as csv_file:
            # 创建csv写文件对象
            csv_writer = csv.writer(csv_file)
            # 写csv的标题
            csv_writer.writerow(['购买的游戏','可能会感兴趣的游戏','置信度'])
            # transactions 为数据集
            transactions = self.loadSimpDat()
            # patterns 为频繁项集
            patterns = pyfpgrowth.find_frequent_patterns(transactions, self.min_sup)
            # rules 为规则
            rules = pyfpgrowth.generate_association_rules(patterns, self.min_conf)
            for value in rules.items():
                if (value[1][1] <= 1):
                    print('{0} ======> {1} conf:{2}'.format(set(value[0]),set(value[1][0]),value[1][1]))
            """  写入文件 """
            for value in rules.items():
                # 因推导空集可产生大于1的置信度，因此在此进行筛选
                if (value[1][1] <= 1):
                    csv_writer.writerow([set(value[0]),set(value[1][0]),value[1][1]])
        return len(rules)

class TimeRecord():
    def defenceSup_Conf(self,min_sup,min_conf):
        """
        不同支持度、置信度的时间记录函数
        :param min_sup: 最小支持度
        :param min_conf: 最小置信度
        :return: 运行时间,不同支持度的列表
        """
        sup_list = []
        gr = GuanRules(min_sup,min_conf)
        # 时间记录程序
        Start_time = time.time()
        sup_list.append(gr.run())
        End_time = time.time()
        return End_time - Start_time,sup_list

    def plot_time(self,time_list,length_list):
        """
        画图函数
        :param time_list:数据列表
        :return: 数据图
        """
        fig = plt.figure(dpi=300)
        with plt.style.context(['ieee', 'grid']):
            x = np.array([row for row in range(low,up,10)])
            y1 = np.array(time_list)
            y2 = np.array(length_list)
            print(y2)
            ax1 = fig.add_subplot()
            ax1.plot(x, y1,color='brown',label="Runnnig time", marker='+')
            ax1.set_ylabel('Running time')
            ax1.legend(loc = 1,title='left', edgecolor='k')

            ax2 = ax1.twinx()
            ax2.plot(x, y2, label="size", marker='^')
            ax2.set_ylabel('Number of frequent item sets')
            ax2.legend(loc = 2,title='right', edgecolor='k')
            plt.autoscale(tight=True)
            plt.xlabel('support_num')

        # 局部图
        # fig2 = plt.figure()
        # with plt.style.context(['ieee', 'grid']):
        #     x = np.array([row for row in range(90, 140, 10)])
        #
        #     ax1 = fig2.add_subplot()
        #     ax1.plot(x, y1[2:7], label="Fp growth", marker='+')
        #     ax1.set_ylabel('Running time')
        #     ax1.legend(loc=1, title='left', edgecolor='k')
        #
        #     ax2 = ax1.twinx()
        #     ax2.plot(x, y2[2:7], label="size", marker='^')
        #     ax2.set_ylabel('Number of frequent item sets')
        #     ax2.legend(loc=2, title='right', edgecolor='k')
        #     plt.autoscale(tight=True)
        #     plt.xlabel('support_num')

        plt.show()

if __name__ == '__main__':
    Time_rec = TimeRecord()
    time_list,length_list,min_sup = [],[],40
    time_run,length = Time_rec.defenceSup_Conf(min_sup, 0.7)
    print('1.运行时间为：{:.3f}s\n2.关联规则数目为：{}个'.format(time_run,length[0]))
