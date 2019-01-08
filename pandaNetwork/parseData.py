# _*_ coding: UTF-8 _*_
import os
import json
from courseData import *

def parseDatas():
    curdir = os.path.split(__file__)[0]
    path = os.path.join(curdir, 'datasCleaned.json')
    datas = json.load(open(path))
    courseDatas = {}
    count = 0
    for (ID, data) in datas.items():
        courseDatas[ID] = courseData(data)
        count += 1
        if count % 5 == 0:
            print('parseDatas finish count:{}'.format(count))

    return courseDatas

courseDatas = parseDatas()
print("finish")
