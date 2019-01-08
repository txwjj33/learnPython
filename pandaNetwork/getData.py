# _*_ coding: UTF-8 _*_
import requests
import json

url = "http://10.1.1.62:8080/classroom_stat/schedule/panda_product/"

result = {}
ids = json.load(open('lessonID.json'))
for lessonID in ids:
    print("get data of lessonID: " + lessonID)
    response = requests.get(url + lessonID, headers = {"invite-code": "O5pROB"})
    dataStr = response.content.decode("utf-8")
    data = json.loads(dataStr)
    result[lessonID] = data

with open('datas.json', 'w') as f:
    f.write(json.dumps(result))
