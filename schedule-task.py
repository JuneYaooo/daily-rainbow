# -*- coding: utf-8 -*-
import sys
import time
import ntchat
import random
import re
import schedule
from modules.weather import MoJiWeather
from modules.sentence import Sentence
from modules.news import News
from modules.database import MySQL
from modules.music import CloudMusic
import yaml
import os

# ==================全局变量====================
# get config variables
# 获取当前脚本所在文件夹路径
curPath = os.path.dirname(os.path.realpath(__file__))
# 获取yaml文件路径
yamlPath = os.path.join(curPath, "config.yaml")
# open方法打开直接读出来
with open(yamlPath, 'r', encoding='utf-8') as f:
    config = f.read()
config_dict = yaml.load(config, Loader=yaml.FullLoader)  # 用load方法转字典
white_dict = config_dict['white_dict']
auto_reply_flag = config_dict['auto_reply_flag']  # 自动回复开关
robot_reply_flag = config_dict['robot_reply_flag']  # 机器人回复开关
db_connection = config_dict['db_connection']
default_music_list = config_dict['default_music_list']
tulin_robot = config_dict['tulin_robot']
ai_art = config_dict['ai_art']
joke_station = config_dict['joke_station']

# class
sentence = Sentence()

def morning(nickname):
    return '\n'.join([f'早安，{nickname}❤~',sentence.getEarthyLove()])

def music_handler(msg):
    msg_split = re.split('[,;，。；\s]', msg)
    print('====music_handler=====')
    print('msg_split', msg_split)
    if len(msg_split) > 1:
        song_name = msg_split[1] if len(re.findall(r'音乐|歌', msg_split[0]))>0 else msg_split[0]
    else:
        song_name = default_music_list[random.randint(0, len(default_music_list)-1)]
    music = CloudMusic()
    print('查询音乐名：  ', song_name)
    music_list = music.SarchSong(song_name)
    if music_list is not None and len(music_list) == 3:
        send_text = '送上一首 ' + str(music_list[2]) + '的 【' + str(music_list[0]) + '】，来听听吧~\n' + str(music_list[1])
    else:
        send_text = '未获取到相关音乐，换一首试试哦~'
    return send_text


# 微信回复
wechat = ntchat.WeChat()

# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)

# 定时发送
# 发送早安消息任务
def send_morning_job():
    if not wechat.login_status:
        return
    wechat.send_text(to_wxid="wxid_3bl22ci7j97v22", content=morning(white_dict["wxid_xxxxx"]))

# 每天8:01 am执行
schedule.every().day.at("08:01").do(send_morning_job)

# 定时发送
# 发送中午歌曲任务
def send_afternoon_music(to_wxid):
    if not wechat.login_status:
        return
    wechat.send_text(to_wxid=to_wxid, content=f'☆{white_dict[to_wxid]}放松一下吧🐳 ☆ \n'+music_handler('午间音乐'))

# 随机发送音乐
music_time = f"{random.randint(12,18)}:{random.randint(10,59)}:{random.randint(10,59)}"
print('music_time',music_time)
schedule.every().day.at(music_time).do(send_afternoon_music,'wxid_xxxxx')

# 随机发送音乐
music_time = f"{random.randint(13,18)}:{random.randint(10,59)}:{random.randint(10,59)}"
print('music_time',music_time)
schedule.every().day.at(music_time).do(send_afternoon_music,'wxid_xxxxx')

# 随机发送音乐
music_time = f"{random.randint(14,17)}:{random.randint(10,59)}:{random.randint(10,59)}"
print('music_time',music_time)
schedule.every().day.at(music_time).do(send_afternoon_music,'wxid_xxxxx')

# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
try:
    while True:
        schedule.run_pending() # 定时任务
        time.sleep(10)
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
