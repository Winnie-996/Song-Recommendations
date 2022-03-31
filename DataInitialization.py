import pandas as pd
import numpy as np


def DataOperate(minSupport):
    """
    :param minSupport:最小支持度
    :return:gameDict：去除小于最小支持度数目的游戏购买数量信息：结构为 --> 游戏名称：购买数量
            userDict: 去除小于最小支持度数目的用户购买记录：结构为 --> 用户名：[游戏1，游戏2，......]
    """
    a = np.array(pd.read_csv("outputdata/SongList.csv"))
    boolean = np.all((a[:, 2] == "play").reshape((-1, 1)), axis=1)

    # 记录play的索引
    indexList = []
    for i in range(a.shape[0]):
        if boolean[i]:
            indexList.append(i)
    buyData = np.delete(a, indexList, axis=0)
    # 至此，play条目已被完全移除，数据集仅剩游戏购买条目，即buyData

    ''' 转换为userId:[gameName1,gameName2,...]的字典 '''
    userDict = {}
    for i in range(buyData.shape[0]):
        if str(buyData[i, 0]) not in userDict:
            userDict[str(buyData[i, 0])] = [buyData[i, 1]]
        else:
            userDict[str(buyData[i, 0])].append(buyData[i, 1])
    # set去重并list
    for item in userDict.keys():
        userDict[item] = list(set(userDict[item]))
    # userDict：userId:[gameName1,gameName2,...]的字典

    ''' 统计游戏购买数量 '''
    gameDict = {}
    for item in userDict.values():
        for i in item:
            # i = i.replace(',', ' ')
            if i not in gameDict:
                gameDict[i] = 1
            else:
                gameDict[i] += 1
    # gameDict：游戏名：购买数量 的字典
    print("###########################################")
    print("去除小于最小支持度条目前的购物记录条目数：%d"%(len(userDict)))
    ''' 处理小于最小支持度的条目 '''
    for key,values in userDict.copy().items():
        count = []
        for item in values.copy():
            if gameDict[item] < minSupport:
                values.remove(item)
            else:
                count.append(gameDict[item])
        if not values:
            userDict.pop(key)
            continue
        else:
            userDict[key] = [x for y, x in sorted(zip(count, values),reverse=True)]
    # 当前的userDict 为去除小于最小支持度条目并按count排序后的
    print("去除小于最小支持度条目后的购物记录条目数：%d" % (len(userDict)))
    print("-------------------------------------------")
    print("去除小于最小支持度条目前的游戏条目数：%d" % (len(gameDict)))
    gameDict = {key:value for key,value in gameDict.items() if value >= minSupport}
    print("去除小于最小支持度条目后的游戏条目数：%d" % (len(gameDict)))
    print("###########################################")
    return gameDict,userDict


if __name__ == '__main__':
    DataOperate(3)
    gameDict,userDict = DataOperate(3)
    print(list(userDict.values())[1:6])

