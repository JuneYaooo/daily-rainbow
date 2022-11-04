# -*- coding: utf-8 -*-
import sys
import time
import ntchat
import datetime
import random
import re
import schedule
from modules.weather import MoJiWeather
from modules.robot import TulinRobot
from modules.sentence import Sentence
from modules.news import News
from modules.database import MySQL
from modules.music import CloudMusic
from modules.picture import DreamDiffusion, ERNIEViLG
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
weather = config_dict['weather']

# class
robot = TulinRobot(tulin_robot['apiKey'])
sentence = Sentence()

# ==================全局变量====================


def hide_menu():
    menu = """=====恭喜你触发了彩蛋=====
    1.可以和我说，早安，晚安~
    2.天气查询，如发送 天气查询 北京
    3.听听音乐，如发送 音乐 人间
    4.试试AI绘画？只是可能要有点耐心~如发送 绘画 一朵紫色的花
    5.看看新闻，如发送 新闻|热搜|微博|头条
    6.可以有一搭没一搭闲聊，如发送 包含闲聊|聊天|机器人等关键词；不想聊了就说再见~
    7.隐含词触发夸夸文学/毒鸡汤/土味情话/笑话等等...等你来撩~
    8.其他请期待..
    PS: 如有任何建议，请留言（关键词：建议|推荐|安利|留言+你的建议）
    """
    return menu


def getTime():
    today = datetime.datetime.now()+datetime.timedelta(hours=+8)
    date2 = time.strptime('1900-01-01', "%Y-%m-%d")
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    t = today.timetuple()
    days = (today-date2).days
    return f'今天是{t.tm_year}年{t.tm_mon}月{t.tm_mday}日 星期{t.tm_wday+1} 我们在一起：{days}天'


def getTimeX():
    t = int(time.strftime("%H", time.localtime()))
    if t > 24:
        t = t-24
    print('time',t)
    return t


def message_handler():
    if random.random()>0.9:
        message = sentence.getSoup()
    elif random.random()>0.6:
        message = sentence.getEarthyLove()
    elif random.random()>0.5 and joke_station['flag']==True:
        message = sentence.getJoke(joke_station['app_id'], joke_station['app_secret'])
    else:
        message = sentence.getPi()

    return message

def news_handler(msg):
    news = News()
    if len(re.findall(r'微博|weibo|热搜|新闻',msg))>0:
        send_text = '当前微博热搜\n' + news.crawl_weibo_hot_rank()
    elif len(re.findall(r'头条|toutiao',msg))>0:
        send_text = '当前今日热搜\n' + news.crawl_toutiao_hot_rank()
    return send_text


## 存储建议和反馈
def suggest_handler(msg, wxid):
    db = MySQL(db_connection['host'], db_connection['port'], db_connection['user'], str(db_connection['passwd']), db_connection['db'])
    keyword = re.findall(r'建议|推荐|安利',msg)[0]
    id = 'SG' + str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
    raw_text = msg
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = f"insert into suggestion(`id`,`wxid`,`type`,`raw_text`,`create_time`) values('{id}','{wxid}','{keyword}','{raw_text}','{create_time}');"
    res = db.exeSQL(sql)
    if res == None:
        file = os.path.join(curPath, "suggestion.txt")
        with open(file, 'a+') as f:
            f.write(' '.join([id, wxid, keyword, raw_text, create_time, '\n']) ) #
    return f'你的{keyword}已收到~'


def weather_handler(msg):
    msg_split = re.split('[,;，。；\s]', msg)
    if len(msg_split) > 1:
        city_name = msg_split[1] if '天气' in msg_split[0] else msg_split[0]
    else:
        city_name = weather['default_city']
    try:
        city_url = MoJiWeather.search_city(city_name)
        send_text = MoJiWeather.parse(city_url)
    except:
        send_text = '天气查询失败，请输入正确格式，如 天气查询 北京 或 北京 天气查询'
    return send_text

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

def picture_handler(msg):
    msg_split = re.split('[,;，。；\s]', msg)
    print('====picture_handler=====')
    print('msg_split', msg_split)
    ernie_style_list = ['古风', '油画', '水彩画', '卡通画', '二次元', '浮世绘', '蒸汽波艺术', 'low poly', '像素风格', '概念艺术', '未来主义', '赛博朋克',
                        '写实风格', '洛丽塔风格', '巴洛克风格', '超现实主义']
    if len(msg_split) > 1:
        pic_name = msg_split[1] if len(re.findall(r'画图|画画|图像|绘画', msg_split[0])) > 0 else msg_split[0]
        print('===使用ERNIE ViLG===')
        pic_model = ERNIEViLG(ak=ai_art['ernie_vilg']['ak'], sk=ai_art['ernie_vilg']['sk'])
        img_path = pic_model.get_pic(pic_name, ernie_style_list[random.randint(0, len(ernie_style_list))])
    else:
        img_path = None
    print('img_path: ', img_path)
    return img_path



def morning(nickname):
    return '\n'.join([f'早安，{nickname}❤~',sentence.getEarthyLove()])


def night(nickname):
    return '\n'.join([f'晚安[月亮]，{nickname}(´-ω-`)', sentence.getPi()])


# 微信回复
wechat = ntchat.WeChat()

# 打开pc微信, smart: 是否管理已经登录的微信
wechat.open(smart=True)



# 注册监听所有消息回调
@wechat.msg_register(ntchat.MT_ALL)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    # print("########################")
    # print(message)
    # 声明全局变量（使函数里可修改变量）
    global auto_reply_flag
    global robot_reply_flag

    data = message["data"]
    from_wxid = data["from_wxid"]
    to_wxid = data["to_wxid"]
    self_wxid = wechat_instance.get_login_info()["wxid"]
    nickname = white_dict[from_wxid]
    msg = data["msg"]

    # 全局自动回复模式是否开启
    if msg == '月光宝盒':
        auto_reply_flag = True
        wechat_instance.send_text(to_wxid=from_wxid, content='已开启June自动回复模式~')
        return
    elif msg == '芝麻关门':
        auto_reply_flag = False
        wechat_instance.send_text(to_wxid=from_wxid, content='已关闭June自动回复模式~')
        return

    # 判断消息不是自己发的，且在白名单里，并回复对方
    send_text = ''
    if auto_reply_flag == True and from_wxid in list(white_dict.keys()) and to_wxid == self_wxid and len(msg)>0:
        print("########################")
        print(message)
        # 闲聊机器人
        if len(re.findall(r'机器人|聊天|闲聊|旺旺',msg))>0 and robot_reply_flag == False:
            robot_reply_flag = True
            send_text = '哈喽哈喽~我在呢，来闲聊吧~'
        elif len(re.findall(r'退出|关闭|再见|拜拜|不聊了|see you|さようなら|じゃね',msg,re.IGNORECASE))>0 and robot_reply_flag == True:
            robot_reply_flag = False
            send_text = '那先聊到这~拜拜啦~下次再召唤我吧~'
        # 天气查询
        elif '天气' in msg:
            send_text = weather_handler(msg)
        # 音乐查询
        elif len(re.findall(r'音乐|歌',msg))>0:
            send_text = music_handler(msg)
        # 关键词触发新闻|热搜查询
        elif len(re.findall(r'微博|weibo|热搜|新闻|头条',msg))>0:
            send_text = news_handler(msg)
        # 关键词触发土味情话
        elif len(re.findall(r'宝贝|honey|亲爱的|爱你|情话',msg))>0:
            send_text = sentence.getEarthyLove()
        # 关键词触发彩虹屁
        elif len(re.findall(r'夸|好听的|赞美|褒扬|夸奖|彩虹屁|吹|幸运',msg))>0:
            send_text = sentence.getPi()
        # 关键词触发笑话
        elif len(re.findall(r'笑话|搞笑|段子', msg)) > 0 and joke_station['flag']==True:
            send_text = sentence.getJoke(joke_station['app_id'], joke_station['app_secret'])
        # 关键词触发毒鸡汤
        elif '鸡汤' in msg:
            send_text = sentence.getSoup()
        # 关键词触发本品说明书
        elif len(re.findall(r'这是什么|菜单|这是啥|本人吗|说明书|操作说明|使用说明|用法|怎么用|menu|姐姐', msg, re.IGNORECASE)) > 0:
            send_text = hide_menu()
        # 关键词触发随机回复
        elif len(re.findall(r'随便|说点|无聊|累|唉|哎|说话', msg)) > 0:
            send_text = message_handler()
        # 关键词触发晚安回复
        elif '晚安' in msg or (len(re.findall(r'睡|困|休息', msg)) > 0 and getTimeX() > 21):
            send_text = night(nickname)
        # 关键词触发早安回复
        elif len(re.findall(r'早啊|早安|早上好|早呀', msg)) > 0:
            send_text = morning(nickname)
        # 关键词触发建议|推荐|安利
        elif len(re.findall(r'建议|推荐|安利', msg)) > 0:
            send_text = suggest_handler(msg, from_wxid)
        # 关键词触发自拍提示
        elif len(re.findall(r'出门', msg)) > 0:
            print('自拍',white_dict[from_wxid])
            send_text = f'今日{white_dict[from_wxid]}自拍（0/1）'
        # 关键词触发AI绘画
        elif len(re.findall(r'画图|画画|图像|绘画', msg))>0:
            if len(re.split('[,;，。；\s]', msg))>1:
                wechat_instance.send_text(to_wxid=from_wxid, content='已收到，正在处理，请稍等~')
            img_path = picture_handler(msg)
            if img_path is not None:
                wechat_instance.send_image(to_wxid=from_wxid, file_path=img_path)
            else:
                send_text = 'AI绘画尝试失败，请输入正确格式~ 如 绘画 山上有一个和尚'
        elif robot_reply_flag == True:
            send_text = robot.dialog(msg)
        # 其余情况不说话
        else:
            send_text = ''
        # 是否需要发送消息
        if len(send_text)>0:
            wechat_instance.send_text(to_wxid=from_wxid, content=send_text)



# 以下是为了让程序不结束，如果有用于PyQt等有主循环消息的框架，可以去除下面代码
try:
    while True:
        schedule.run_pending()  # 定时任务
        time.sleep(2)
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()