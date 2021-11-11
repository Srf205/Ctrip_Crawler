# 此文件夹主要用于获取携程网站的城市到详情页url的映射
+ 主要是进行预处理，便于后续操作和爬虫编程
## 文件详情
### 用于直接拉取142个热门城市的爬虫
+ 代码：[get_city_and_url.py](get_city_and_url.py)
  + 数据主要来源于此网址：[https://you.ctrip.com/sitelist/china110000.html](https://you.ctrip.com/sitelist/china110000.html)
  + 数据会输出到：[Citys_And_Url.csv](Citys_And_Url.csv)
### 对34个省市，非直辖市选择前五城市，直辖市只留自己的爬虫
+ 代码：[get_city_and_url_Every5.py](get_city_and_url_Every5.py)
  + 数据主要来源于URL的query的直接检索：[https://you.ctrip.com/searchsite/?query=](https://you.ctrip.com/searchsite/?query=)
  + 模拟逐一访问搜索的流程，会比较慢
  + 数据会输出到：[Cities.json](Cities.json)