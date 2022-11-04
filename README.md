# daily-rainbow
a lovely sweet wechat assistance

1.在config.yaml里做基本配置,

- 希望发送消息的白名单, 先运行before-start文件夹里的get-wxid.py，找到好友的wxid
- 文心文生图ak和sk换成自己的 详见 https://wenxin.baidu.com/ernie-vilg
- 笑话使用自己申请的id，详见 https://www.mxnzp.com/doc/detail?id=5

2.一些临时写死的东西..

开启自动回复的暗号是 月光宝盒

关闭自动回复模式的暗号是 芝麻关门

默认天气查询是当前时间，默认地点可自己修改
...

3.一些包的安装问题


安装 ntchat：`pip install ntchat` 或 `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple ntchat`（国内源）

安装 Crypto：`pip install pycryptodome`

安装 yaml：` pip install PyYAML`
