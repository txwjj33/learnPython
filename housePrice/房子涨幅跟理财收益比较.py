# _*_ coding: UTF-8 _*_
# 计算房子和理财的收益
import math

# 理财年化收益9%
r = 1.09
# 20年
time = 20
# 每月收益
rMonth = (r - 1) / 12 + 1

print("%d年以后数据：" % time)

# 200万房子按照每年r涨幅，time年以后的总价
s0 = 200 * math.pow(r, time)
print("房子总价: %f" % s0)

# 买房首付三成加上各种税算70w,20年
s1 = 70 * math.pow(r, time)
print("首付收益: %f" % s1)

s2 = 0   # 月供收益
s3 = 0   # 租金收益, 假设每个月租金是2000
monthCount = time * 12
# 将每个月的月供拿来理财，20年等额本息，利率5.1%，每个月月供是9352
for i in range(0, monthCount):
    # 理财方式：整年按照每年r收益，不足一年时按照每月rMonth收益
    year = (monthCount - i) / 12
    growth = math.pow(r, year) * math.pow(rMonth, monthCount - i - 12 * year)
    s2 += 0.9352 * growth
    s3 += 0.2 * growth

print("月供收益: %f" % s2)
print("租金收益: %f" % s3)
print("房子总价 + 房租收益：%f" % (s0 + s3))
print("首付收益 + 月供收益: %f" % (s1 + s2))
