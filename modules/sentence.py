import requests
import random

class Sentence(object):
    def __init__(self):
        pass

    def getSoup(self):
        # 毒鸡汤
        headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
                    "Referer": "",
                  "Origin": "https://www.iowen.cn"}
        r = requests.get(url='https://www.iowen.cn/jitang/api/', headers=headers, verify=False)
        if '数据获取成功' in r.text:
            return r.json()['data']['content']['content']
        return '高考在昨天，考研在明天，今天没有什么事儿。'

    def getPi(self):
        # 彩虹屁
        headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69",
                "Referer": "https://mp.weixin.qq.com"}
        res = requests.get(url='https://api.shadiao.pro/chp', headers=headers)
        r = res.json()['data']['text']
        return r if len(r) > 3 else '你上辈子一定是碳酸饮料吧，为什么我一看到你就开心的冒泡'

    def getEarthyLove(self):
        # 土味情话
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            }
        resp = requests.get(url='https://api.lovelive.tools/api/SweetNothings', headers=headers)
        if resp.status_code == 200:
            r = resp.text
        else:
            r = ''
        return r if len(r) > 3 else '你来自万千星河，是我的最大心动'

    def getJoke(self, app_id, app_secret):
        # 笑话
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            }
        resp = requests.get(
            url=f'https://www.mxnzp.com/api/jokes/list/random?page=1&app_id={app_id}&app_secret={app_secret}',
            headers=headers)
        if resp.status_code == 200:
            res = resp.json()
            r = res['data'][random.randint(0, 9)]['content']
        return r if len(r) > 3 else """同学一见面就跟我诉苦，说他前段时间总盗汗，一睡着就出汗，医院检查花了好几百，后来又找了个老中医开了十来副中药，喝了也不管用，而且一天比一天厉害。我问：“后来呢?咋治好的?”一问到这，我明显看到同学的嘴角一抽搐，愤愤道：“我换了个薄被子。”"""