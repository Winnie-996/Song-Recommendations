from fp_pso_growth.FPGrowth import *
import numpy as np
from itertools import combinations


def fitness(x, userDict, gameNameList, minSupport, D):
    location = x[x <= 0]
    if location.shape[0] == D:
        return 0
    NowX = sigmoid(x) > 0.5  # 已转化为True-False布尔矩阵
    outGameName = set(np.array(gameNameList)[NowX].tolist())  # 将01矩阵对应的游戏名输出为set
    count = 0
    for item in userDict.values():
        if outGameName <= set(item):
            count += 1
    if count < minSupport:
        return 0
    else:
        return count


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def PSO(userDict, gameNameList, minSupport):
    """
    :param userDict: 用户购买记录
    :param gameNameList: 游戏列表
    :return:
    """
    frequentSet = []  # 候选频繁项集
    c1, c2, w = 0.6, 0.6, 0.8
    vMax, vMin = 3.0, -3.0
    xMax, xMin = 5.0, -5.0
    NP, G, D = 50, 10000, len(gameNameList)
    x = (np.random.rand(NP, D)) * np.array(xMax - xMin) + np.array(xMin) - 1.5
    v = (np.random.rand(NP, D)) * np.array(vMax - vMin) + np.array(vMin)
    xFit = np.zeros((1, NP), dtype=float)
    trace = np.zeros((1, G), dtype=float)

    pBest, pFit = x, np.zeros((1, NP), dtype=float)
    gBest, gFit = np.zeros((1, D), dtype=float), 0

    for i in range(NP):
        xFit[0, i] = fitness(x[i, :], userDict, gameNameList, minSupport, D)
        if xFit[0, i] != 0:
            frequentSet.append(x[i, :])
        pFit[0, i] = xFit[0, i]
        if pFit[0, i] > gFit:
            gFit = pFit[0, i]
            gBest = x[i, :]

    for g in range(G):
        for i in range(NP):
            v[i, :] = w * v[i, :] + c1 * np.random.rand(1, D) * (gBest - x[i, :]) \
                      + c2 * np.random.rand(1, D) * (pBest[i, :] - x[i, :])
            for j in range(D):
                if v[i, j] < vMin or v[i, j] > vMax:
                    v[i, j] = np.random.rand() * (vMax - vMin) + vMin
            x[i, :] = x[i, :] + v[i, :]
            for j in range(D):
                if x[i, j] < xMin or x[i, j] > xMax:
                    x[i, j] = np.random.rand() * (xMax - xMin) + xMin
            xFit[0, i] = fitness(x[i, :], userDict, gameNameList, minSupport, D)
            if pFit[0, i] < xFit[0, i]:
                pFit[0, i] = xFit[0, i]
                pBest[i, :] = x[i, :]
            if gFit < xFit[0, i]:
                gFit = xFit[0, i]
                gBest = x[i, :]
            if xFit[0, i] != 0:
                try:
                    frequentSet.index(x[i, :])
                except ValueError:
                    frequentSet.append(x[i, :])

        trace[0, g] = gFit
        # print("第 %d 次迭代完成，种群最大适应度值为%d" % (g + 1, gFit))
        print("第 %d 次迭代完成" % (g + 1))
    return trace, gBest, frequentSet


if __name__ == '__main__':
    minSupport = 50
    root, listHead, gameNameList, gameDict, userDict = fptree_create(minSupport)
    trace, _, frequentSet = PSO(userDict, gameNameList, minSupport)
    gameSet = []
    for item in frequentSet:
        NowX = sigmoid(item) > 0.5  # 已转化为True-False布尔矩阵
        gameSet.append((np.array(gameNameList)[NowX].tolist()))  # 将01矩阵对应的游戏名输出为set
    for item in gameSet:
        print(item)
