# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import csv
import re,os,json

from requests.models import parse_url
# 获取网页代码
provience_index=[
'北京','广东','山东','江苏','河南','上海','河北','浙江','香港','陕西','湖南','重庆','福建','天津','云南','四川','广西','安徽','海南','江西','湖北','山西','辽宁','台湾','黑龙江','内蒙古','澳门','贵州','甘肃','青海','新疆','西藏','吉林','宁夏'
]

csv_name_provience = 'provience_url.csv'

def getHtmlText(url):
    try:
        # 伪装头
        headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
        r = requests.get(url,headers = headers)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        print('false')
        return 'false'

def parseHtml(provience):
    base_url = 'https://you.ctrip.com/searchsite/?query='
    url = base_url + provience
    site_code = getHtmlText(url)
    soup = BeautifulSoup(site_code,'lxml')
    res = []
    # 找各省市的具体信息
    city_url = soup.find('ul',class_='mudidi-ul cf').find('a',class_='pic')['href'][7:]
    return city_url

    # 输出到csv文件
def outPut(res):
    path = 'Citys_And_Url.csv'
    with open(path, 'w', newline='',encoding='utf-8') as f:
        file = csv.writer(f)
        file.writerow(['城','名','城','URL'])
        for record in res:
            record[1] = record[1][7:]
            file.writerow(record)
            
def fetchProvienceUrl():
    res = []
    cnt = 0
    for city in provience_index[0:2]:
        cnt += 1
        print('Processing ' + city + ", {:.2f}%".format(cnt/len(provience_index) * 100)  )
        city_url = parseHtml(city)
        res.append([city,city_url])
        
    with open(csv_name_provience,'w',encoding='utf-8',newline='') as f:
        file = csv.writer(f)
        for i in res:
            file.writerow(i)
    print('Success! Provience Url fetching done! Data saved as \'' + csv_name_provience + '\'.')
    return res

def fetchCitys(pro_name, url):
    base_url = 'https://you.ctrip.com/place/'
    site_url = base_url + url
    site_code = getHtmlText(site_url)
    soup = BeautifulSoup(site_code,'lxml')
    cities = soup.find('div',class_='hot_destlist cf')
    if cities == None:
        return [[pro_name,url]]
    cities = cities.find_all('li',class_='w_220')
    res =[]
    for i in range(0,5):
        city_name = cities[i].find('dt').text
        city_name = re.search('\D+',city_name).group(0)
        city_url = cities[i].find('a')['href'][7:]
        res.append([city_name,city_url])
    return res
        
data = {}
def main():
    # 主要页面
    pro_url = []
    if os.path.exists(csv_name_provience):
        with open(csv_name_provience,'r',encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                pro_url.append(row)
    else:
        pro_url = fetchProvienceUrl()
    print('=== Data of provience is loaded! ===')
    # print(pro_url)
    
    
    citys = {}
    for record in pro_url:
        print('processing ' + record[0] )
        res = fetchCitys(record[0], record[1])
        citys[record[0]] = res
        
    with open("Cities.json",'w',encoding='utf-8') as f:
        json.dump(citys,f,ensure_ascii = False)
        
if __name__ == '__main__':
    main()