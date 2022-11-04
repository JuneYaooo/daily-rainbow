import requests
from lxml.html import etree
import json


class MoJiWeather():
    def city_name(self):  # 定义一个输入城市名称的函数
        cityname = str(input("输入城市名称："))
        return cityname
    def search_city(city_name):# 搜索这个城市
        index_url = "http://tianqi.moji.com/api/citysearch/%s"%city_name   #  构造查询相应城市天气的url
        response = requests.get(index_url)
        response.encoding = "utf-8"
        try:# 异常捕获
            city_id = json.loads(response.text).get('city_list')[0].get('cityId')# 通过上面的url获取城市的id
            city_url = "http://tianqi.moji.com/api/redirect/%s"%str(city_id)  # 通过城市id获取城市天气
            return city_url
        except:
            print('城市名输入错误')
            exit()
    def parse(city_url):# 解析函数
        response = requests.get(city_url)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        current_city = html.xpath("//div[@class='search_default']/em/text()")[0]#    下面都是利用xpath解析的
        current_kongqi = html.xpath("//div[@class='left']/div[@class='wea_alert clearfix']/ul/li/a/em/text()")[0]
        current_wendu = html.xpath("//div[@class='left']/div[@class='wea_weather clearfix']/em/text()")[0]
        current_weather = html.xpath("//div[@class='wea_weather clearfix']/b/text()")[0]
        current_shidu = html.xpath("//div[@class='left']/div[@class='wea_about clearfix']/span/text()")[0]
        current_fengji = html.xpath("//div[@class='left']/div[@class='wea_about clearfix']/em/text()")[0]
        res = '城市：'+current_city +'\n' + '空气质量：'+current_kongqi +'\n'+'当前温度：'+current_wendu+'℃'+'\n'+'天气状况：' + current_weather+'\n'+'当前湿度：'+current_shidu+'\n'+'当前风速：'+current_fengji
        return res