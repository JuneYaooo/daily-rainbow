import json
import time
import requests
import datetime
import os
import wenxin_api  # 可以通过"pip install wenxin-api"命令安装
from wenxin_api.tasks.text_to_image import TextToImage
import random

class DreamDiffusion(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def get_pic(self, prompt, style='2'):
        s = requests.session()
        login_url = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key' \
                    '=AIzaSyDCvp5MTJLUdtBYEKYWXJrlLzu1zuKM6Xw '
        url = 'https://paint.api.wombo.ai/api/tasks/'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        }
        payload = {
            "returnSecureToken": True,
            "email": self.email,
            "password": self.password
        }
        payload = json.dumps(payload)
        login_respone = s.request('POST', url=login_url, headers=headers, data=payload)
        idtoken = login_respone.json()['idToken']
        headers['authorization'] = 'bearer ' + idtoken
        respone = s.request('POST', url=url, headers=headers)
        new_headers = respone.json()
        print(new_headers)
        new_id = new_headers['id']
        param = {
            'input_spec': {
                "style": str(style),
                "prompt": prompt,
                "display_freq": '10'
            }
        }
        param = json.dumps(param)
        respone2 = s.put(url=url + new_id, headers=headers, data=param)
        result = respone2.json()
        count=0
        while True:
            time.sleep(4)
            respone2 = s.request('GET', url=url + new_id, headers=headers, data=new_headers)
            result = respone2.json()
            print(result)
            count+=1
            if result['result'] is not None or count>4:
                break
        try:
            pic_url = result['result']['final']
            pic = s.request('GET', url=pic_url, headers=headers).content
            this_time = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
            curPath = os.path.dirname(os.path.realpath(__file__))
            dirs = os.path.join(curPath, "images")
            if not os.path.exists(dirs):
                os.makedirs(dirs)
            img_path = os.path.join(dirs, f'{this_time}.jpg')
            with open(img_path, 'wb') as f:
                f.write(pic)
            print('下载完毕')
            return img_path
        except Exception as e:
            print('error!! ', e)
            return None

class ERNIEViLG(object):
    def __init__(self, ak, sk):
        self.ak = ak
        self.sk = sk

    def get_pic(self, prompt, style='油画'):
        wenxin_api.ak = self.ak
        wenxin_api.sk = self.sk
        input_dict = {
            "text": prompt,
            "style": style
        }
        rst = TextToImage.create(**input_dict)
        try:
            IMAGE_URL = rst['imgUrls'][random.randint(0,len(rst['imgUrls'])-1)]
            r = requests.get(IMAGE_URL)
            this_time = int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
            curPath = os.path.dirname(os.path.realpath(__file__))
            dirs = os.path.join(curPath, "images")
            if not os.path.exists(dirs):
                os.makedirs(dirs)
            img_path = os.path.join(dirs, f'{this_time}.jpg')
            with open(img_path, 'wb') as f:
                f.write(r.content)
            print('下载完毕')
            return img_path
        except Exception as e:
            print('error!! ', e)
            return None

if __name__ == '__main__':
    # pic_model = DreamDiffusion(email= "yao0302@163.com", password= "yao666666")
    # img_path = pic_model.get_pic("千钟美酒，一曲满庭芳", '10')
    pic_model = ERNIEViLG(ak="fLiuueWmKeqEfFn7rMQp9qsLrR1h1QwM", sk="sIIS1x1iXamnsuH331lk0oewWltSin14")
    img_path = pic_model.get_pic("千钟美酒，一曲满庭芳", '油画')
    print('img_path',img_path)
