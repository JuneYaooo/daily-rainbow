#!D:/Code/python
# -*- coding: utf-8 -*-
# @Time : 2020/8/22 12:32
# @Author : Am0xil
# @Description : 网易云音乐模拟器

import base64
import binascii
import json
import random
import string
from urllib import parse

import requests
from Crypto.Cipher import AES

class CloudMusic(object):
    def __init__(self):
        pass

    # 从a-z,A-Z,0-9中随机获取16位字符
    def get_random(self):
        random_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        return random_str

    # AES加密要求加密的文本长度必须是16的倍数，密钥的长度固定只能为16,24或32位，因此我们采取统一转换为16位的方法
    def len_change(self, text):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        text = text.encode("utf-8")
        return text

    # AES加密方法
    def aes(self, text, key):
        # 首先对加密的内容进行位数补全，然后使用 CBC 模式进行加密
        iv = b'0102030405060708'
        text = self.len_change(text)
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(text)
        encrypt = base64.b64encode(encrypted).decode()
        return encrypt

    # js中的 b 函数，调用两次 AES 加密
    # text 为需要加密的文本， str 为生成的16位随机数
    def func_b(self, text, str):
        first_data = self.aes(text, '0CoJUm6Qyw8W8jud')
        second_data = self.aes(first_data, str)
        return second_data

    # 这就是那个巨坑的 c 函数
    def func_c(self, text):
        e = '010001'
        f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        text = text[::-1]
        result = pow(int(binascii.hexlify(text.encode()), 16), int(e, 16), int(f, 16))
        return format(result, 'x').zfill(131)

    # 获取最终的参数 params 和 encSecKey 的方法
    def get_final_param(self, text, str):
        params = self.func_b(text, str)
        encSecKey = self.func_c(str)
        return {'params': params, 'encSecKey': encSecKey}

    # 通过参数获取搜索歌曲的列表
    def get_music_list(self, params, encSecKey):
        url = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="

        payload = 'params=' + parse.quote(params) + '&encSecKey=' + parse.quote(encSecKey)
        headers = {
            'authority': 'music.163.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'origin': 'https://music.163.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://music.163.com/search/',
            'accept-language': 'zh-CN,zh;q=0.9',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()['result']['songs']


    # 获取歌曲的播放链接
    def get_reply(self, params, encSecKey):
        url = "https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token="
        payload = 'params=' + parse.quote(params) + '&encSecKey=' + parse.quote(encSecKey)
        headers = {
            'authority': 'music.163.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'origin': 'https://music.163.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://music.163.com/',
            'accept-language': 'zh-CN,zh;q=0.9'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text

    def SarchSong(self, song):
        d = {"csrf_token": "", "hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "s": song,
             "type": "1",
             "offset": "0",
             "total": "true", "limit": "30"}
        d = json.dumps(d)
        random_param = self.get_random()
        param = self.get_final_param(d, random_param)
        try:
            song_list = self.get_music_list(param['params'], param['encSecKey'])
            first_id = song_list[0]['id']
            song_link = f"https://music.163.com/#/song?id={first_id}"
            song_name = song_list[0]['name']
            artist_name = song_list[0]['ar'][0]['name']
            return [song_name, song_link, artist_name]
        except Exception as e:
            print('error!! ', e)
            return None

if __name__ == '__main__':
    music = CloudMusic()
    music_list = music.SarchSong('红马')
    if music_list is not None and len(music_list) == 3:
        print('送上一首 '+str(music_list[2])+'的 【'+str(music_list[0])+'】，来听听吧~\n'+str(music_list[1]))



