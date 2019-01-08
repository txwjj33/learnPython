# _*_ coding: UTF-8 _*_
'''必要的数据清洗工作
'''
import os
import sys
import json

curdir = os.path.split(__file__)[0]
viewModeType = {'只看学生': 1, '只看老师': 2, '双向视频': 3, '关闭视频': 4}

def isInTimes(ts, times):
    for time in times:
        if ts >= time[0] and ts <= time[1]:
            return True
    return False

def parseBgTimes(targetDict):
    '''解析前后台事件，筛选出应用处于后台的时间段
    targetDict: 老师或学生的字典
    '''
    targetDict['bgTimes'] = []
    bgStart = None
    for alarm in targetDict['data']['alarm']:
        if alarm['evt'] == 'userEnterBackground':
            if bgStart == None:
                bgStart = alarm['ts']
            # else:
            #     print('userEnterBackground again!')
        elif alarm['evt'] == 'userEnterForeground':
            if bgStart != None:
                targetDict['bgTimes'].append([bgStart, alarm['ts']])
                bgStart = None
            # else:
            #     print('userEnterForeground is not after userEnterBackground!')
    if bgStart != None:
        # print('userEnterBackground without end')
        targetDict['bgTimes'].append([bgStart, sys.maxsize])

def parseViewMode(dataCleaned):
    '''解析viewmode事件，筛选出只看老师或者只看学生的时间段
    只有老师能切换模式
    targetDict: 保存数据的目标字典
    '''
    def appendTime(preMode, startTime, endTime):
        if preMode == 4:
            # 由4切换到其他模式
            dataCleaned['modeTimes'][1].append([startTime, endTime])
            dataCleaned['modeTimes'][2].append([startTime, endTime])
        elif preMode == 1 or preMode == 2:
            # 由1或2切换到其他模式
            dataCleaned['modeTimes'][preMode].append([startTime, endTime])

    dataCleaned['modeTimes'] = {1: [], 2: []}  # 只看老师或者只看学生的时间段
    dataCleaned['viewMode'] = {}  # viewmode集合，初始是只看学生
    preTime = 0
    preMode = 1
    for alarm in dataCleaned['t']['data']['alarm']:
        if alarm['evt'] == 'switchVideoMode':
            mode = viewModeType[alarm['desc']]
            ts = alarm['ts']
            if mode == preMode: continue
            dataCleaned['viewMode'][ts] = alarm['desc']
            appendTime(preMode, preTime, ts)
            preTime = ts
            preMode = mode
    # 需要检查最后一次模式
    appendTime(preMode, preTime, sys.maxsize)

def parseStat(targetDict, rIgnoreTimes, tIgnoreTimes):
    '''解析网络数据
    targetDict: 保存数据的目标字典
    rIgnoreTimes: 应该忽略rxVR的时间段
    tIgnoreTimes: 应该忽略txVR的时间段
    '''
    targetDict['t'] = {}
    targetDict['tBg'] = {}
    targetDict['tIgnore'] = {}
    targetDict['r'] = {}
    targetDict['rBg'] = {}
    targetDict['rIgnore'] = {}
    stats = targetDict['data']['stat']
    if len(stats) > 0:
        targetDict['tsMin'] = stats[0]['ts']
        targetDict['tsMax'] = stats[-1]['ts']
    else:
        targetDict['tsMin'] = 0
        targetDict['tsMax'] = sys.maxsize
    for stat in stats:
        ts = stat['ts']
        # 是否处于后台
        if isInTimes(ts, targetDict['bgTimes']):
            targetDict['tBg'][ts] = stat['txVR']
            targetDict['rBg'][ts] = stat['rxVR']
        else:
            if isInTimes(ts, rIgnoreTimes):
                targetDict['rIgnore'][ts] = stat['rxVR']
            else:
                targetDict['r'][ts] = stat['rxVR']
            if isInTimes(ts, tIgnoreTimes):
                targetDict['tIgnore'][ts] = stat['txVR']
            else:
                targetDict['t'][ts] = stat['txVR']

def parseOriginData(dataCleaned):
    '''解析原始数据'''
    parseBgTimes(dataCleaned['s'])
    parseBgTimes(dataCleaned['t'])
    parseViewMode(dataCleaned)

    # 解析网络数据, 只看学生时学生不会接收数据，老师不发送数据，只看老师正好相反
    modeTimes = dataCleaned['modeTimes']
    parseStat(dataCleaned['s'], modeTimes[1], modeTimes[2])
    parseStat(dataCleaned['t'], modeTimes[2], modeTimes[1])

def cleanData(courseID, originData):
    # print('{} cleanData start'.format(courseID))
    dataCleaned = {}
    dataCleaned['courseID'] = courseID

    # 为了方便在s和t里面保存data，最后删除
    dataCleaned['s'] = {'data': originData['data']['s']}
    dataCleaned['t'] = {'data': originData['data']['t']}
    parseOriginData(dataCleaned)

    del dataCleaned['s']['data']
    del dataCleaned['t']['data']

    # print('{} cleanData finished'.format(courseID))
    return dataCleaned

def cleanAndSaveData(courseID, originData, path):
    with open(path, 'w', encoding = 'utf-8') as f:
        dataCleaned = cleanData(courseID, originData)
        f.write(json.dumps(dataCleaned))

def runClean():
    datas = json.load(open(os.path.join(curdir, 'datas.json')))
    count = 0
    datasCleaned = {}
    for (id, data) in datas.items():
        datasCleaned[id] = cleanData(id, data)
        count += 1
        if count % 20 == 0: print('clean finish count: {}'.format(count))
    with open(os.path.join(curdir, 'datasCleaned.json'), 'w', encoding = 'utf-8') as f:
        f.write(json.dumps(datasCleaned))
    print('clean finished!')

runClean()
