# _*_ coding: UTF-8 _*_
'''courseData类: 一个课程的数据
'''
import numpy as np
import pandas as pd

from pandas import Series, DataFrame

def drawMovingAverage(data, N):
    '''移动平均
    data: 数据源，可以是列表或者Series
    N: 连续多少个数的平均'''
    n = np.ones(N)
    weights = n / N
    swp = np.convolve(data, weights)[N-1:-N+1]
    x = np.arange(len(data) - N + 1)
    plt.plot(x, swp, lw = 2)
    plt.plot(x, data[N-1:], lw = 1)

def cutDataByTime(data, bins):
    '''将data按照index的时间在bins中的哪个时间段分类，返回GroupBy对象
    另一种实现方式见cutDataByTime1'''
    cat = pd.cut(data.index, bins)
    return data.groupby(cat)

# def cutDataByTime1(data, bins):
#     import bisect
#     # bisect.bisect_left返回插入后仍保持顺序的位置，相同数据插到左边
#     return data.groupby(lambda ts: bisect.bisect_left(bins, ts))

def getBaseStats(d):
    '''获取基本的统计数据，最大值、最小值、数量、平均数'''
    return {'min': d.min(),'max': d.max(), 'count': d.count(), 'mean': d.mean()}

class courseData:
    def __init__(self, cleanedData):
        print('{} init start'.format(cleanedData['courseID']))
        self.courseID = cleanedData['courseID']

        self.s = {}
        self.t = {}
        self.parseData(self.s, cleanedData['s'])
        self.parseData(self.t, cleanedData['t'])

        self.tsMin = min(self.s['tsMin'], self.t['tsMin'])
        self.tsMax = max(self.s['tsMax'], self.t['tsMax'])
        self.modeTimes = cleanedData['modeTimes']
        # 插入起止点，方便对数据分片
        self.viewMode = Series('只看学生', index = [self.tsMin])
        for (ts, mode) in cleanedData['viewMode'].items():
             self.viewMode[int(float(ts))] = mode
        self.viewMode[self.tsMax] = ''

        self.sAnalyze = {}
        self.tAnalyze = {}
        self.analyzeData(self.sAnalyze, self.s)
        self.analyzeData(self.tAnalyze, self.t)

        print('{} init finished'.format(cleanedData['courseID']))

    def parseData(self, targetDict, sourceDict):
        '''解析s或者t的数据
        targetDict: 目标字典
        sourceDict: 源字典
        '''
        '''构造一个Series，并且把index变成int'''
        def seriesReindexToInt(d):
            return Series(list(d.values()), index = [int(x) for x in d.keys()])

        targetDict['bgTimes'] = sourceDict['bgTimes']
        targetDict['tsMin'] = sourceDict['tsMin']
        targetDict['tsMax'] = sourceDict['tsMax']


        targetDict['t'] = seriesReindexToInt(sourceDict['t'])
        targetDict['tBg'] = seriesReindexToInt(sourceDict['tBg'])
        targetDict['tIgnore'] = seriesReindexToInt(sourceDict['tIgnore'])
        targetDict['r'] = seriesReindexToInt(sourceDict['r'])
        targetDict['rBg'] = seriesReindexToInt(sourceDict['rBg'])
        targetDict['rIgnore'] = seriesReindexToInt(sourceDict['rIgnore'])

    def analyzeData(self, targetDict, sourceDict):
        '''一些基础的数据统计'''
        targetDict['rmean'] = sourceDict['r'].mean()
        targetDict['tmean'] = sourceDict['t'].mean()

    def cutDataByViewMode(self, data):
        '''根据viewmode对数据分片'''
        return cutDataByTime(data, self.viewMode.index)

    def analyzeByViewMode(self, data):
        '''输出viewmode分片以后的基本统计数据'''
        grouped = self.cutDataByViewMode(data)
        fr = grouped.apply(getBaseStats).unstack()
        fr['mode'] = self.viewMode.values[:-1]
        fr['duration(s)'] = [x.length for x in fr.index]
        return fr
