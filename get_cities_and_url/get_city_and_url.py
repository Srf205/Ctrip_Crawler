# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import csv
import re
# 获取网页代码
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

def praseHtml(html):
    
    soup = BeautifulSoup(html,'lxml')
    res = []
    # 找热点城市
    citys = soup.findAll('li',class_='w_220')
    for i in citys:
        tmp = i.find('a')
        # print(tmp)
        city_name = tmp.find('dt').text
        city_url = tmp['href']
        city_name = re.search('\D+',city_name).group(0)
        res.append([city_name,city_url])
    
    # 找非热点城市
    citys = soup.findAll('ul',class_='c_city_nlist cf')
    tmp = citys[0].findAll('a')
    baseUrl = 'https://you.ctrip.com/sight/'   # 后续可以凭借此直接拼凑URL
    for i in tmp:
        city_name = i.string
        city_url = i['href']
        res.append([city_name,city_url])    
    return res

    # 输出到csv文件
def outPut(res):
    path = 'Citys_And_Url.csv'
    with open(path, 'w', newline='',encoding='utf-8') as f:
        file = csv.writer(f)
        file.writerow(['城市名','城市URL'])
        for record in res:
            record[1] = record[1][7:]
            file.writerow(record)
            
def main():
    # 主要页面
    url_base = "https://you.ctrip.com/sitelist/china110000.html"
    page_code = getHtmlText(url_base)
    res = praseHtml(page_code)
    outPut(res)
    print("Done!")
    
if __name__ == '__main__':
    main()