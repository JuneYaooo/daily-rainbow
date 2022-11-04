#!/usr/bin/env Python
# coding=utf-8
import datetime
import requests
import time
import urllib3
from bs4 import BeautifulSoup
import os
import pytz
# 解除警告
urllib3.disable_warnings()

class News(object):
    def __init__(self):
        self.crawl_timestamp = int()
        self.today = datetime.date.today().strftime('%Y%m%d')
        self.spider_time = pytz.datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
        today = datetime.date.today()
        self.yesterday = str(today - datetime.timedelta(days=1))
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'

    def crawl_weibo_hot_rank(self):
        headUrl = "https://s.weibo.com/"
        headers = {
            'cookie': 'SINAGLOBAL=3911117184872.8696.1639527374827; SUB=_2AkMUCDdxf8NxqwJRmfoVz23ma451yw7EieKiVMaqJRMxHRl-yT9kqkgJtRB6P4gZnmdhCudLQHJHFQ36OiE8XXGYwh7W; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5uMMYLG3wuk8vQo76ViUOR; _s_tentry=passport.weibo.com; Apache=3614331364885.708.1666496583291; ULV=1666496583298:4:1:1:3614331364885.708.1666496583291:1641631578261; XSRF-TOKEN=BgF2yxQhYxOc3LtZ9wUb3A0t; WBPSESS=1QIptkPh0r7VTljIOfRP6xb4SavQ6pKx06o1fRiI4YlXUcQiUVkQxzi_g_RE0ihJx433iz5PTC9E_eS9xaVjJ742mxbOhp-geDqrlG5lc59O5YOejVZtSip65jNQh70m',
            'user-agent': self.user_agent
        }
        hotUrl = "https://s.weibo.com/top/summary?cate=realtimehot"
        prox = ''
        res = requests.get(hotUrl, proxies={'http': prox, 'https': prox}, headers=headers, verify=False) # 抓取内容
        res.raise_for_status()     # 检测抓取内容是否正常
        # encoding代表Head中的编码方式 apparent_encoding代表Body中编码方式
        # 当出现乱码时，apparent_encoding编码方式更准确
        res.encoding = res.apparent_encoding
        res = BeautifulSoup(res.text, "lxml")
        r = 0
        # 遍历热搜的标签
        # #pl_top_realtimehot 根据id, > table > tbody > tr 逐层查找
        news_list = []
        for item in res.select("#pl_top_realtimehot > table > tbody > tr"):
            # 按类名.td-01提取热搜排名
            _rank = item.select_one('.td-01').text
            if not _rank:
                continue
            # 按类名.td-02提取热搜
            topic = item.select_one(".td-02 > a").text
            topic_url = 'https://s.weibo.com/' + item.select_one(".td-02 > a")['href']

            # 提取热搜热度
            heat = item.select_one(".td-02 > span").text

            # 提取热搜标签
            icon = item.select_one(".td-03").text
            r += 1
            news_list.append(str(r)+'. '+topic +'\n'+topic_url)

        return '\n'.join(news_list[:10])

    def crawl_toutiao_hot_rank(self):
        headers = {
            'user-agent': self.user_agent,
            'referer': 'https://www.toutiao.com/',
        }
        hotUrl = "https://i.snssdk.com/hot-event/hot-board/?origin=hot_board"
        prox = ''
        response = requests.get(hotUrl, proxies={'http': prox, 'https': prox}, headers=headers, verify=False)  # 抓取内容
        if response.status_code == 200:
            res = response.json()
            res = res.get('data')
        news_list = []
        r = 0
        for item in res:
            r += 1
            topic = item['Title']
            topic_url = item['Url']
            news_list.append(str(r) + '. ' + topic + '\n' + topic_url)
        return '\n'.join(news_list[:10])



if __name__ == '__main__':
    news = News()
    weibo_news = news.crawl_weibo_hot_rank()
    toutiao_news = news.crawl_toutiao_hot_rank()

