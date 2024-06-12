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
        "msgtype": "tex",
        "text": {
            "content": content,
            "mentioned_list": mentioned_list,
            "mentioned_mobile_list": mentioned_mobile_list
        }
    }
    data2 = {
            "msgtype": "markdown",  # 消息类型，此时固定为markdown
            "markdown": {
                "content": "# **【i检验研发测试进度】**\n" +  # 标题 （支持1至6级标题，注意#与文字中间要有空格）
                           "### **bug总数：**<font color=\"info\">10个</font>\n" +  # 加粗：**需要加粗的字**
                           "> 今日新增bug个数：<font color=\"info\">5个</font> \n" +  # 引用：> 需要引用的文字
                           "> 未解决bug：<font color=\"warning\">4个</font> \n" # 字体颜色(只支持3种内置颜色)  # 绿色：info、灰色：comment、橙红：warning
            }
    }
    data = json.dumps(data2)
    info = requests.post(url=webhook, data=data, headers=header)
    print(info)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=468a19ea-12e2-42b2-a479-5c5c6e221672"
    content = "【i检验进度汇报】"
    mentioned_list = ["@all",]
    mentioned_mobile_list = None
    send_text(webhook, content, mentioned_list)


