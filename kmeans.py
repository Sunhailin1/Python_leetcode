# coding=utf-8
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime

# city = 'xian'
city = 'hangzhou'
startday = '20170101'
endday = '20211204'

# 常用Header
my_headers = [
    # 随机Header，防止403
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
]
# 免费IP池
proxy_list = [
    #随机IP，防止403
    "3.219.153.200:80",
    "3.216.45.64:80",
    "3.221.105.1:80",
    "3.216.58.165:80",
    "3.95.108.97:80",
    "54.173.31.46:80",
    "52.7.49.13:80",
    "34.192.172.235:80",
    "3.225.148.200:80",
    "54.174.230.114:80",
    "3.224.205.253:80",
    "3.218.203.153:80",
    "3.224.69.117:80",
    "54.90.113.178:5678",
    "3.211.65.185:80",
    "18.210.77.4:80",
    "35.153.140.35:5678",
    "18.207.70.248:80",
    "3.211.17.212:80",
    "52.87.85.141:80",
    "18.204.234.136:80",
    "54.173.70.38:80",
    "35.153.140.35:5678",
    "54.209.69.235:80",
    "54.90.113.178:5678",
    "34.231.175.107:80",
    "208.113.134.223:80",
    "3.214.232.83:80",
    "178.128.243.121:3128",
    "45.199.148.4:80",
    "45.199.148.2:80",
    "206.253.164.120:80",
    "199.19.224.3:80",
    "190.115.15.13:8080",
    "209.141.35.151:80",
    "206.253.164.146:80",
    "206.253.164.101:80",
    "209.141.55.228:80",
    "206.253.164.28:80",
    "159.223.31.84:3129",
    "189.164.254.200:10101",
    "209.141.56.127:80",
    "206.253.164.122:80",
    "3.65.204.5:5678",
    "3.120.159.141:12000",
    "194.5.193.183:80",
    "190.26.201.194:8080",
    "51.91.157.66:80",
    "181.78.11.103:999",
    "18.184.4.1:5678",
    "88.99.25.49:80",
    "188.165.59.127:3128",
    "41.65.251.75:1976",
    "154.236.189.26:1976",
    "206.253.164.108:80",
    "194.163.131.117:8080",
    "190.115.15.13:8080",
    "103.124.2.229:3128",
    "119.81.71.27:8123",
    "188.134.90.77:8080",
    "47.100.102.227:8888",
    "124.70.46.14:3128",
    "66.98.82.3:999",
    "121.43.190.89:3128",
    "181.204.163.34:999",
    "114.249.223.20:3128",
    "190.26.201.194:8080",
    "121.78.139.75:80",
    "139.99.237.62:80",
    "189.164.254.200:10101",
    "18.184.4.1:5678",
    "106.15.193.237:8088",
    "101.37.127.28:3000",
    "223.17.44.84:80",
    "3.120.159.141:12000",
    "120.77.247.79:80",
    "117.161.75.82:3128",
    "159.223.31.84:3129",
    "188.165.59.127:3128",
    "120.79.15.203:80",
    "103.149.162.194:80",
    "3.65.204.5:5678",
    "124.204.33.162:8000",
    "58.20.235.180:9091",
    "171.244.170.206:8080",
    "47.100.1.112:8089",
    "103.216.103.26:80",
    "118.212.48.245:8085",
    "121.78.139.77:80",
    "178.128.243.121:3128",
    "181.78.11.103:999",
    "123.131.94.74:7890",
    "180.183.118.154:3128",
    "66.98.82.3:999",
    "115.224.121.202:8085",
    "1.117.100.196:7788",
    "112.6.117.135:8085",
    "54.38.243.181:8080",
    "223.96.90.216:8085",
    "81.4.102.233:8081",
    "188.134.90.77:8080",
    "207.244.227.169:443",
    "36.27.48.212:7890",
    "180.87.102.69:80",
    "121.78.139.44:80",
    "180.87.102.68:80",
    "103.124.2.229:3128",
    "103.216.103.25:80",
    "181.198.86.74:999",
    "113.125.118.95:8888",
    "119.4.231.171:8085",
    "162.241.76.185:80",
    "119.81.71.27:8123",
    "101.37.127.28:3000",
    "47.100.102.227:8888"
]

#生成日期列表
date_l = [datetime.strftime(x, '%Y%m') for x in list(pd.date_range(start=startday, end=endday, freq='MS'))]

# 生成urls
# urls = ["http://lishi.tianqi.com/xian/201510.html"]
urls = []
for day in date_l:
    urls.append('http://lishi.tianqi.com/' + city + '/' + day + '.html')

#记录数据，方便存储
day = []
maxtemper = []
mintemper = []
weather = []
wind = []


#获取当月数据
def getWeather(url):

    #随机等待一段时间
    t = np.random.randint(0, 2)
    time.sleep(t)
    #随机选择header
    header = {"User-Agent": random.choice(my_headers)}
    #随机选择IP地址
    proxies = {'https': random.choice(proxy_list)}

    response = requests.get(url, headers=header, proxies=proxies, timeout=5)
    soup = BeautifulSoup(response.text, 'html.parser')
    #万一403，更换浏览器请求头和IP地址，再次尝试
    if response.status_code == 403:
        getWeather(url)
        return

    #找出存储天气数据的字段
    weather_month = soup.select('ul[class="thrui"]')[0].text[2:-8]
    #将字段分割
    weather_day = weather_month.split('\n\n\n\n')

    for i in range(len(weather_day)):
        tem_weather = weather_day[i].split('\n')
        day.append(tem_weather[0][:-1])
        maxtemper.append(tem_weather[1])
        mintemper.append(tem_weather[2])
        weather.append(tem_weather[3])
        wind.append(tem_weather[4])
    print('存入{}_{}天数据'.format(url[-11:-5], len(weather_day)))
    return


#按月获取天气数据
for url in urls:
    getWeather(url)

df = pd.DataFrame({'日期': day, '最高温度': maxtemper, '最低温度': mintemper, '天气': weather, '风向': wind})
df.to_csv('Weather of {} Date{}_{}.csv'.format(city, startday, endday), encoding='utf-8')
