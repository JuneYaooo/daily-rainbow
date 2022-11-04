import requests

class TulinRobot(object):
    def __init__(self, apiKey):
        self.apiKey = apiKey

    def dialog(self, question):
        url = "http://openapi.tuling123.com/openapi/api/v2"
        data = {
            "reqType": 0,
            "perception": {
                "inputText": {
                    "text": question
                }
            },
            "userInfo": {
                "apiKey": self.apiKey,
                "userId": "wangwang"
            }
        }
        res = requests.post(url=url, json=data)  # JSON格式的请求，将数据赋给json参数
        answer = res.json()["results"][0]["values"]["text"]
        return answer