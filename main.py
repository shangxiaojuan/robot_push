# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json

import requests as requests


def send_text(webhook, content, mentioned_list=None, mentioned_mobile_list=None):
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    data = {
        "msgtype": "text",
        "text": {
            "content": content,
            "mentioned_list": mentioned_list,
            "mentioned_mobile_list": mentioned_mobile_list
        }
    }
    data = json.dumps(data)
    info = requests.post(url=webhook, data=data, headers=header)
    print(info)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=468a19ea-12e2-42b2-a479-5c5c6e221672"
    content = "i检验进度汇报"
    mentioned_list = ["@all",]
    mentioned_mobile_list = None
    send_text(webhook, content, mentioned_list)


