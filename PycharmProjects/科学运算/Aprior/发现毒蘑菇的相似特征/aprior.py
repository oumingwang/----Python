#coding:utf8
from numpy import *


#加载数据
def loadData():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]

#选取频繁项集中所有的候选项
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return map(frozenset,C1)

#过滤支持率低的频繁项集
def scanD(D,Ck,minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not ssCnt.has_key(can):ssCnt[can] = 1
                else: ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0,key)
        supportData[key] = support
    return retList,supportData



#筛选出Ck频繁项候选值
def aprioriGen(Lk,k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1==L2:
                retList.append(Lk[i] | Lk[j])
    return retList


#频繁项集划分，输出筛选后的频繁项集和支持度
def apriori(dataSet,minSupport = 0.5):
    C1 = createC1(dataSet)
    D = map(set,dataSet)
    L1,supportData = scanD(D,C1,minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2],k)
        Lk,supK = scanD(D,Ck,minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L,supportData


'''
dataSet = loadData()

C1 = createC1(dataSet)

retList,supportData = scanD(dataSet,C1,0.5)

L,suppData = apriori(dataSet)
print L
print apriori(dataSet,0.1)[0]

'''

#生成包含可信度的规则列表
def generateResult(L,supportData,minConf = 0.7):
    bigRuleList = []
    for i in range(1,len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
            else:
                calcConf(freqSet,H1,supportData,bigRuleList,minConf)

    return bigRuleList


def calcConf(freqSet,H,supportData,br1,minConf = 0.7):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet - conseq]
        if conf >= minConf:
            print freqSet - conseq,'-->',conseq,'conf:',conf
            br1.append((freqSet-conseq,conseq,conf))
            prunedH.append(conseq)
    return prunedH


def rulesFromConseq(freqSet,H,supportData,br1,minConf=0.7):
    m = len(H[0])
    if (len(freqSet) > (m + 1)):
        Hmp1 = aprioriGen(H,m + 1)
        Hmp1 = calcConf(freqSet,Hmp1,supportData,br1,minConf)
        if (len(Hmp1) > 1):
            rulesFromConseq(freqSet,Hmp1,supportData,br1,minConf)


dataSet = loadData()

L,supportData = apriori(dataSet,0.5)

rules = generateResult(L,supportData,0.5)

print rules