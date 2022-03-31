import pyfpgrowth
import csv
import FPGrowth as fg


class FpDmax():
    def loadSimpDat(self):
        dataSet = []
        with open('outputdata/SongList.csv', 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                dataSet.append(row)
        return dataSet
    def Run(self):
        self.dataSet = self.loadSimpDat()
        patterns = pyfpgrowth.find_frequent_patterns(self.dataSet, 400)
        print(len(patterns))
        sys_copy = {}
        sys_list = list(patterns.keys())
        # 输出所有第一阶段的最大频繁项集
        for i in range(1,len(sys_list)):
            if len(sys_list[i]) == 1:
                sys_copy[sys_list[i-1]] = patterns[sys_list[i-1]]
        # print(len(sys_copy))
        fg.run()
        qin_list = list(sys_copy.keys())
        sun_list = list(sys_copy.keys())
        for i in range(len(qin_list)):
            qin_list[i] = set(qin_list[i])  #先转换成集合的形式

        #print(qin_list)
        qin_copy = {}
        slist = []

        for i in range(len(qin_list)):
            s = 0
            for j in range(len(qin_list)):
                if not(qin_list[i].issubset(qin_list[j])) and (i != j):
                    s += 1
            if(s == len(qin_list) - 1):
                qin_copy[sun_list[i]] = sys_copy[sun_list[i]]

        print("最大频繁项集：")
        # 最终的除去子集后的最大频繁项集
        for item in qin_copy.items():
            print(item)



if __name__ == '__main__':
    runer = FpDmax()
    runer.Run()