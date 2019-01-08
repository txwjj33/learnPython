# _*_ coding: UTF-8 _*_
import codecs
import json
import xlrd
import xlsxwriter

def getJsonFile(name):
    with codecs.open(name, "r", "utf-8") as jsonFile:
        result = json.load(jsonFile)
        jsonFile.close()
        return result

# 计算涨幅数据
def getRiseData(name, prices):
    firstPrice, lastPrice = None, None
    firstStr, lastStr = "", ""
    for year in range(2009, 2019):
        for month in range(1, 13):
            timeStr = "%d%02d" % (year, month)
            if timeStr not in prices: continue
            if not firstPrice:
                firstPrice = prices[timeStr]
                firstStr = "%d(%s)" % (firstPrice, timeStr)
            else:
                lastPrice = prices[timeStr]
                lastStr = "%d(%s)" % (lastPrice, timeStr)

    if not lastPrice:
        print("writePriceRiseData error, lastPrice is None")
        return [name, 0, 0, 0]
    return [name, firstStr, lastStr, lastPrice * 100.0 / firstPrice]

# 写入涨幅数据
def writeRiseData(workbook, name, datas):
    sheet = workbook.add_worksheet(name)
    sheet.set_column(1, 2, 15)
    sheet.write_row(0, 0, [u"区域", u"开始价格", u"最后价格", u"涨幅"])
    datas.sort(key = lambda data: data[3], reverse = True)
    for i in range(0, len(datas)):
        datas[i][3] = "%.2f%%" % datas[i][3]
        sheet.write_row(i + 1, 0, datas[i])

def parseRiseData(name, fileName):
    result = getJsonFile(fileName)
    cityDatas = []
    sectionsDict = {}
    for (sectionName, sectionData) in result["sections"].items():
        cityDatas.append(getRiseData(sectionName, sectionData["prices"]))
        sectionDatas = []
        sectionsDict[sectionName] = sectionDatas
        for (streetName, streetData) in sectionData["streets"].items():
            sectionDatas.append(getRiseData(streetName, streetData))

    workbook = xlsxwriter.Workbook(name + u"涨幅.xlsx")
    textWrapFormat = workbook.add_format({"text_wrap": True})
    writeRiseData(workbook, name, cityDatas)
    for name, datas in sectionsDict.items():
        writeRiseData(workbook, name, datas)
    workbook.close()
    print("all done")

parseRiseData(u"天津", u"天津房价.json")
# parseRiseData(u"北京", u"北京房价.json")
