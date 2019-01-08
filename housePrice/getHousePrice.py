# _*_ coding: UTF-8 _*_
import urllib
import urllib2
import re
import codecs
import json
import time

DEBUG = False

def writeJsonFile(name, data):
    with codecs.open(name, "w", "utf-8") as jsonFile:
        jsonFile.write(json.dumps(data, ensure_ascii = False, indent = 4))
        jsonFile.close()

#获取网页数据
def getData(url):
    userAgent = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    headers = {"User-Agent": userAgent}
    maxTryNum = 10
    for tryNum in range(0, maxTryNum):
        try:
            request = urllib2.Request(url, headers = headers)
            response = urllib2.urlopen(request)
            return response.read().decode("utf-8")
        except:
            if tryNum < maxTryNum - 1:
                # 暂停一段时间重试
                time.sleep(1)
                continue
            else:
                print("getData error: try max times, url: %s" % url)
                break

# 解析某个页面的价格数据
def parsePrice(content, pricesDict):
    pattern = re.compile('xyear: {(.*?)},.*?ydata.*?"data":\[(.*?)\]}\]', re.S)
    items = re.findall(pattern, content)
    if len(items) > 1:
        print("parsePrice error: items length more than 1")
        exit()
    if len(items) == 0:
        print("parsePrice error, no data")
        return
    times = items[0][0].split(",")
    prices = items[0][1].split(",")
    if len(times) != len(prices):
        print("parsePrice error: length not the same")
        exit()
    for i in range(0, len(times)):
        p = re.compile('"(\d+).*?(\d+)')
        timeData = re.findall(p, times[i])[0]
        # 年 + 月
        pricesDict[timeData[1] + timeData[0]] = int(prices[i])

# 解析各个街道的名字和链接
def parseStreets(sectionContent, streetsDict):
    pattern = re.compile('<span class="sub-letter-item">.</span>.*?<a href="(.*?)">(.*?)</a>', re.S)
    items = re.findall(pattern, sectionContent)
    for item in items:
        url = item[0]
        name = item[1]
        if url == "": continue
        print("parse street %s, url: %s" % (name, url))
        streetsDict.setdefault(name, {})
        streetResult = streetsDict[name]
        streetContent = getData(url)
        parsePrice(streetContent, streetResult)
        if DEBUG: break

# 解析各个区的名字和链接
def parseSections(cityContent, sectionsDict):
    pattern = re.compile('<span class="selected-item">.*?</span>(.*?)</span>', re.S)
    searchResult = re.search(pattern, cityContent).group()
    pattern = re.compile('<a href="(.*?)">(.*?)</a>', re.S)
    items = re.findall(pattern, searchResult)
    for item in items:
        url = item[0]
        name = item[1]
        if url == "": continue
        print("parse section %s, url: %s" % (name, url))
        if name not in sectionsDict.keys():
            sectionResult = {}
            sectionResult["prices"] = {}
            sectionResult["streets"] = {}
            sectionsDict[name] = sectionResult
        else:
            sectionResult = sectionsDict[name]
        sectionContent = getData(url)
        parsePrice(sectionContent, sectionResult["prices"])
        # 以下的print后面必须加空格，不然报错，猜想跟sectionName是中文有关
        print("get streets of %s " % (name))
        parseStreets(sectionContent, sectionResult["streets"])
        if DEBUG: break

# 获取某个城市的所有数据
def getCityData(city):
    print("start parse " + city)
    result = {}
    result["prices"] = {}
    result["sections"] = {}

    for year in range(2009, 2019):
        cityURL = "https://www.anjuke.com/fangjia/%s%d/" % (city, year)
        print("parse city %s %d, url: %s" % (city, year, cityURL))
        content = getData(cityURL)
        parsePrice(content, result["prices"])
        print("get sections of %s %d" % (city, year))
        parseSections(content, result["sections"])

    print("all done!")
    return result

writeJsonFile(u"天津房价.json", getCityData("tianjin"))
# writeJsonFile(u"北京房价.json", getCityData("beijing"))
