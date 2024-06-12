# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
from datetime import date
import requests as requests


def send_text(webhook, content, mentioned_list=None,bug_info=None):
    bug_total_count = bug_info["bug_total_count"]
    bug_new_create = bug_info["bug_new_create"]
    bug_unsolved_count = bug_info["bug_unsolved_count"]
    bug_members_list = bug_info["bug_members_list"]
    bug_member_nums = bug_info["bug_member_nums"]

    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }

    data = {
        "msgtype": "tex", #消息类型，为text
        "text": {
            "content": content,
            "mentioned_list": mentioned_list, #@相关人员列表
            "mentioned_mobile_list": mentioned_mobile_list
        }
    }
    bug_mem = ""
    count = 0
    for i in bug_members_list:
        remark = i["remark"]
        total_num = bug_member_nums[count]
        count +=1
        bug_mem += f"> {remark}：<font color=\"warning\">{total_num}个</font> \n"
    print(bug_mem)
    data2 = {
            "msgtype": "markdown",  # 消息类型，此时固定为markdown
            "markdown": {
                "content": "# **【i检验研发测试进度】**\n" +  # 标题 （支持1至6级标题，注意#与文字中间要有空格）
                           f">### **一、bug总数：**<font color=\"info\">{bug_total_count}个</font>\n" +  # 加粗：**需要加粗的字**
                           f"> 今日新增bug个数：<font color=\"info\">{bug_new_create}个</font> \n" +  # 引用：> 需要引用的文字
                           f"> 未解决bug：<font color=\"warning\">{bug_unsolved_count}个</font> \n" +# 字体颜色(只支持3种内置颜色)  # 绿色：info、灰色：comment、橙红：warning
                           f"### **二、缺陷按成员排名**\n" + bug_mem +  # 加粗：**需要加粗的字**
                            "> [详情请到gitee上查看：https://e.gitee.com/xinghe-lis/projects/660543/bugs/table](https://e.gitee.com/xinghe-lis/projects/660543/bugs/table)"

            },
           "mentioned_list": mentioned_list
    }
    data = json.dumps(data2)
    info = requests.post(url=webhook, data=data, headers=header)
    print(info)

def getIssueOverview():
    url = "https://api.gitee.com/enterprises/7329688/measure_boards/issue_overview?program_id=660543&tab_ident=delivery_quality&metric_ident=bug_overview&start_date=2024-05-13&end_date=2024-06-12&category=bug&is_show_high_priority=true"

    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; user_locale=zh-CN; BEC=1f1759df3ccd099821dcf0da6feb0357; Hm_lvt_24f17767262929947cc3631f99bfd274=1717464303,1718067328,1718179596,1718181144; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2210271719%22%2C%22first_id%22%3A%221900b93b65d568-0aa358487b0c6e8-26001c51-1296000-1900b93b65e7d3%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218f846d6e3e81-0fe854d779b6d08-26001d51-1296000-18f846d6e3f657%22%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThmODQ2ZGQ2NWUxMzItMDMxOTk1MWFlNjM5NzM2LTI2MDAxZDUxLTEyOTYwMDAtMThmODQ2ZGQ2NWYzMzciLCIkaWRlbnRpdHlfbG9naW5faWQiOiIxMDI3MTcxOSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%2210271719%22%7D%7D; csrf_token=oWR3pwXi6KTz3Uq44v32CotGk48uEzYzUs2Yp5jFZb5KRBlxkv4hbod977neTs%2FJpzoPRuYBFrAplQPq0YG37g%3D%3D; Hm_lpvt_24f17767262929947cc3631f99bfd274=1718181756; gitee-session-n=bEFPaXdvZE9GR2dCeEpwMUFNdHR5aTJJVnNYRTRJQWNKa0RQSzRvUENXak9OTTR6TU1tTXdvaDkyb09ud3cxeWVvWVdGaVJWR24zTEFKNFNFdURLd0ZEVldManhPdWJZd2VoZUdTdTFnSm9wejFncU04WCsvSGFVMGFMZWpZRjUzVkhzUElKRnBRSzg2TndDNmMzYUs0SXdDdVJIWFc3a0xOc0U2dkkxZVR2Y0REaHNJRG1iRGtvcXJSSTl6ZDBGZ2UzOWtwS1Y5RlpqcTFLRWJZVTdHcG8zd2UrMGh4ZUVXMFZxeXdtZjdEekN4OFpsK053Sm0wMS9WTFVld1RhN2t4TkZUNFRaUUlWWFhaMi9qbEJFYnkrVzJEZVdzcHN5ZTBHSHMyTUJaVG5aQWg4V1pEVWc0dUU4YXBhSUtZK0ZGOTJVdUFobGVKSHBpaWlnaTdWNjlYdUpqeUE4b04zMTlPVEFNRHYzaTJUN3NNQXNFcWFMWkoyNnlJTGw2czFrczVyOGVoYVpXU0ZLM2J6NlpIazBDK2Uyc3IzazBYVnZGUUZDdy9xNFJreWVMYzhwYWFqWkpIWUhWNzY3T1VXZ0ZPTWgwd0tuaXZtaWFCYlRjWURxRXJ1dmFIMXp5Y1dzR2RWcEc4T3pYaVE0cEpJVnFWWDFZQ29TR0ZXKzU2ZTlGSWEzdFF3QmsrQmYyeVlMSlNLYkFDa216QkhFS0RlMUpQL2pPRVllOXpDdGtxNVJxVFZnbmN2N2hGbzlWQVM2UWh3bmNyeVV3czFNN1ltUW93NksvQzZmRHpRZ1dBZkY4Q2tUNWdjWk1QdFhRZ1I2bmRsOC9QODdOaVhGRHBNWC0temN1UXJEZGx5RUtvNGRuaHFhR1ZuQT09--3f54df2cf305cbed485b0cf558bb7b0f30e41472; gitee-session-n=NmRzUjJHcHQvb1JPa3U0ajI1TWIwbXBMK2ZRRHppNEZpN09tSGxiQ3ZyYnNYallxV2pTTzVJTGl3bEFGSk5YYXZUZ3B3WlNQeGdsWlIvYzd0THJZVWRlTHBoeUl6eWcxSUFmaHBCaUVUcEFpZGd3S29wVXBiQmZMQmlBTGZrUHZ3bGl6Nzc2WlFibXVETWo5NERSWkdBRHdNdnE2akp3UjdKL0x0SEl4L2hwcFdtWnFja2h6T2EyN3o3WG9NRVVreFppQmE4bTRhL0VKRnBIQU1UZFhucE1ndDQ2UHgzZlJ2VTFYMDRkNC9SbjBlYUFRTjJvaDh2Kzh5QkZINkhyeHdITENmM1cvMXo1T3RiTjRpWnVxWnRVODlGdlp1SWpuYjhEUm5LTG54MTNDMlByNlp0aTYzcXplTGhWN3VzOU9Dcy91cC9mUFFRcDJPVit6aTBOTU52d3dGR2VqQjFpSDEzQm4wenlXZ01xOEQvL1U4MERsRk8rRDRaQ0VRSGIxSjU0UkF4Tk04cWExaWZ2ZnQ3ZFdxVXAzemtLRFhoTjJUaDRKRDJWY3BxbDRPSWFhRDZVN01XbzRiZndOOHVBN0RZRGtOVEJUY0s4dFVBcUFsZ0h0T1c2Ky8xTjVITWhPREJkMzE1UTBZRGl1RDFQeVQ4WkJwYWpvdGNMVGE4eVZrVzhBdy9UTWRhUVpKb1IvS1ZEdGxTUVJ3aWxheWhGcWVrbzRqTmhUZUNzZ1JwQWVSSDlzeU8yU0Y0bllnT2F0SXlqaWNtUU5idCt0dDZhemdHQTM2UVBaNEtENWJNUHJMeEIxRi9laFhhTEpEOUtKaU4ycjNDSVdaYnRKcHZKSy0tZTZmOHVDRHpkSnlwcmh1c2RUR2V6UT09--692136ca7b735a90e7b5e64b9d46315dcb7ac637',
        'Origin': 'https://e.gitee.com',
        'Referer': 'https://e.gitee.com/'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    return response.text

def get_issue_trend():

    url = "https://api.gitee.com/enterprises/7329688/measure_boards/issue_trend?program_id=660543&tab_ident=delivery_quality&metric_ident=bug_trend&start_date=2024-05-13&end_date=2024-06-12&category=bug"

    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; user_locale=zh-CN; BEC=1f1759df3ccd099821dcf0da6feb0357; Hm_lvt_24f17767262929947cc3631f99bfd274=1717464303,1718067328,1718179596,1718181144; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2210271719%22%2C%22first_id%22%3A%221900b93b65d568-0aa358487b0c6e8-26001c51-1296000-1900b93b65e7d3%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218f846d6e3e81-0fe854d779b6d08-26001d51-1296000-18f846d6e3f657%22%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThmODQ2ZGQ2NWUxMzItMDMxOTk1MWFlNjM5NzM2LTI2MDAxZDUxLTEyOTYwMDAtMThmODQ2ZGQ2NWYzMzciLCIkaWRlbnRpdHlfbG9naW5faWQiOiIxMDI3MTcxOSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%2210271719%22%7D%7D; csrf_token=oWR3pwXi6KTz3Uq44v32CotGk48uEzYzUs2Yp5jFZb5KRBlxkv4hbod977neTs%2FJpzoPRuYBFrAplQPq0YG37g%3D%3D; Hm_lpvt_24f17767262929947cc3631f99bfd274=1718181756; gitee-session-n=bEFPaXdvZE9GR2dCeEpwMUFNdHR5aTJJVnNYRTRJQWNKa0RQSzRvUENXak9OTTR6TU1tTXdvaDkyb09ud3cxeWVvWVdGaVJWR24zTEFKNFNFdURLd0ZEVldManhPdWJZd2VoZUdTdTFnSm9wejFncU04WCsvSGFVMGFMZWpZRjUzVkhzUElKRnBRSzg2TndDNmMzYUs0SXdDdVJIWFc3a0xOc0U2dkkxZVR2Y0REaHNJRG1iRGtvcXJSSTl6ZDBGZ2UzOWtwS1Y5RlpqcTFLRWJZVTdHcG8zd2UrMGh4ZUVXMFZxeXdtZjdEekN4OFpsK053Sm0wMS9WTFVld1RhN2t4TkZUNFRaUUlWWFhaMi9qbEJFYnkrVzJEZVdzcHN5ZTBHSHMyTUJaVG5aQWg4V1pEVWc0dUU4YXBhSUtZK0ZGOTJVdUFobGVKSHBpaWlnaTdWNjlYdUpqeUE4b04zMTlPVEFNRHYzaTJUN3NNQXNFcWFMWkoyNnlJTGw2czFrczVyOGVoYVpXU0ZLM2J6NlpIazBDK2Uyc3IzazBYVnZGUUZDdy9xNFJreWVMYzhwYWFqWkpIWUhWNzY3T1VXZ0ZPTWgwd0tuaXZtaWFCYlRjWURxRXJ1dmFIMXp5Y1dzR2RWcEc4T3pYaVE0cEpJVnFWWDFZQ29TR0ZXKzU2ZTlGSWEzdFF3QmsrQmYyeVlMSlNLYkFDa216QkhFS0RlMUpQL2pPRVllOXpDdGtxNVJxVFZnbmN2N2hGbzlWQVM2UWh3bmNyeVV3czFNN1ltUW93NksvQzZmRHpRZ1dBZkY4Q2tUNWdjWk1QdFhRZ1I2bmRsOC9QODdOaVhGRHBNWC0temN1UXJEZGx5RUtvNGRuaHFhR1ZuQT09--3f54df2cf305cbed485b0cf558bb7b0f30e41472; gitee-session-n=b00wRzZiZlVPaWxSbmFib0ppSGxhdGNsZ295YUFsZjNoVFduUzl5eEIwbVF6Rk5xcnpuZHQzNi8vQjdBRjA1U0liWXA0OEFvWWdXKzVpZzBFS0pRdEsrUGJKTjJCRUUvdUkvZ0l2b0xhdXRhWDRmSExGYkFsZnJVTCsrNmErMWRTbURYVnQ0eERFSFd3VHdnTUJDa0F4eXUyZ2hwdDBBY0VnRkluQ0Q3NHlmOExlRTBUWDU4V2ova2RVb0ZkdDZ0bWpPMUhEa2lxOUhKMnp5ejRmSmpVSEJwRmc1eGo2Ny92Q0xtMWNORDg4TkdOdnB4cjhOMHp0NU5wR3ovWm4wWGhCR0IzSkN5Zms0OUpoSWtqM1RrZXkzWkViKzE5Mk9KNnRwYlNkdEh2UWozZFFveUs0Z3hvSDlIeTF3R2RJNE5TR0J0dGRzckxYdklTVStuRVRzMlJKWFVlYU1JS3JXOEhTbEd3bTJ3WGZ3VWhQUzFaNm4ydWllSEYwT3g1TzlTUnJJMlNvc1VmeUJadFR4bHlKTEd1UTgzUU9WRmo4RmIrdlg4NHNlWDhORUxueno5SGdVT0NMV05XM2lHbUs4U1dmUGFoeVFBRGg0VkVsc2FaZks5RDdFc3NMVVprdEd2cURXaDNQR21yZFkyOHhHdGdTdkltYk9KNDlyK0krSWN4VUkzZGdZbmhmSXBLckZwVGdZOGxKRGdoM2plTmZ3MThYcW82UlE5ZHhPdlJPMW10aEZzWlVxakgwaExFbXJ3Rm9semlldEQySUdQZmU4OTZTNHVnenVRc1JlaGc0aGlCTjByazBhRGF0OWtNTjl5SFRHN0htWGtIQjFjK1JMcC0tOS9TL3R5bHhoTDJ5aUxSc200Zmw3Zz09--d191c4c560b4fe742d5bfd0d7f3497c4b373477f',
        'Origin': 'https://e.gitee.com',
        'Referer': 'https://e.gitee.com/'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text

def get_issue_rank():

    url = "https://api.gitee.com/enterprises/7329688/measure_boards/issue_rank?program_id=660543&tab_ident=delivery_quality&metric_ident=bug_rank&start_date=2024-05-13&end_date=2024-06-12&category=bug&sort=total"

    payload = {}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; user_locale=zh-CN; BEC=1f1759df3ccd099821dcf0da6feb0357; Hm_lvt_24f17767262929947cc3631f99bfd274=1717464303,1718067328,1718179596,1718181144; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2210271719%22%2C%22first_id%22%3A%221900b93b65d568-0aa358487b0c6e8-26001c51-1296000-1900b93b65e7d3%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218f846d6e3e81-0fe854d779b6d08-26001d51-1296000-18f846d6e3f657%22%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThmODQ2ZGQ2NWUxMzItMDMxOTk1MWFlNjM5NzM2LTI2MDAxZDUxLTEyOTYwMDAtMThmODQ2ZGQ2NWYzMzciLCIkaWRlbnRpdHlfbG9naW5faWQiOiIxMDI3MTcxOSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%2210271719%22%7D%7D; csrf_token=oWR3pwXi6KTz3Uq44v32CotGk48uEzYzUs2Yp5jFZb5KRBlxkv4hbod977neTs%2FJpzoPRuYBFrAplQPq0YG37g%3D%3D; Hm_lpvt_24f17767262929947cc3631f99bfd274=1718181756; gitee-session-n=bEFPaXdvZE9GR2dCeEpwMUFNdHR5aTJJVnNYRTRJQWNKa0RQSzRvUENXak9OTTR6TU1tTXdvaDkyb09ud3cxeWVvWVdGaVJWR24zTEFKNFNFdURLd0ZEVldManhPdWJZd2VoZUdTdTFnSm9wejFncU04WCsvSGFVMGFMZWpZRjUzVkhzUElKRnBRSzg2TndDNmMzYUs0SXdDdVJIWFc3a0xOc0U2dkkxZVR2Y0REaHNJRG1iRGtvcXJSSTl6ZDBGZ2UzOWtwS1Y5RlpqcTFLRWJZVTdHcG8zd2UrMGh4ZUVXMFZxeXdtZjdEekN4OFpsK053Sm0wMS9WTFVld1RhN2t4TkZUNFRaUUlWWFhaMi9qbEJFYnkrVzJEZVdzcHN5ZTBHSHMyTUJaVG5aQWg4V1pEVWc0dUU4YXBhSUtZK0ZGOTJVdUFobGVKSHBpaWlnaTdWNjlYdUpqeUE4b04zMTlPVEFNRHYzaTJUN3NNQXNFcWFMWkoyNnlJTGw2czFrczVyOGVoYVpXU0ZLM2J6NlpIazBDK2Uyc3IzazBYVnZGUUZDdy9xNFJreWVMYzhwYWFqWkpIWUhWNzY3T1VXZ0ZPTWgwd0tuaXZtaWFCYlRjWURxRXJ1dmFIMXp5Y1dzR2RWcEc4T3pYaVE0cEpJVnFWWDFZQ29TR0ZXKzU2ZTlGSWEzdFF3QmsrQmYyeVlMSlNLYkFDa216QkhFS0RlMUpQL2pPRVllOXpDdGtxNVJxVFZnbmN2N2hGbzlWQVM2UWh3bmNyeVV3czFNN1ltUW93NksvQzZmRHpRZ1dBZkY4Q2tUNWdjWk1QdFhRZ1I2bmRsOC9QODdOaVhGRHBNWC0temN1UXJEZGx5RUtvNGRuaHFhR1ZuQT09--3f54df2cf305cbed485b0cf558bb7b0f30e41472; gitee-session-n=bTRUNlg1Qjl3aHJaWWw0eHBuVmVJMGo5UlBXa2pYZStRbTFocTRvdUF3Mjk0UEFjTzl6b3pFN3VsbFBpMVZ0dkNKYklmTnNVZjAxeGZjUlZQYzZaOUsvQ3VqbXVtbFB2VGY1dGZTcmQrY1VlMG16R1VLa3NiRnNFVGdTeVJ3T0drTFhmcTN6SW5Xd2x4T0Vkc2RhWmJtU0RoZ0w3WEhmbi96WnIrd2haY0RGcGg1RVRLbXlURXlhUzFOMG90Q0ptOGtiTSs5cXpwQjhMREZyeGxabkVwbjN6Zkh6S0hxek90NXNuVnI0U2hoNXdTTzJKOU1ONVBCcEhadWtwQXNVTW5vQmFZcExwTlhWa1RJaEhEUnpXQ2tjd1g0L3NPYWRkUVlqdzFTK1BuTDJKeStiUDYzZzNDZjRJVDZXOWF0cUdOOElzdnFZeU51UGNvakVuRkFpT1dpRkdzU2k2NFRFNU0xMjNrT1JZTjI2QUk1ekpmbWJQMUJlcHNaTHE4K1NFMG5lRzg2QlBrZGwyVmpab0V5RkY0dU1qNVZJR01nR1crdjVQRFF0STdSTmZxMTBvb0c5REhNQ1ZJNDZnSzMrMFgxSHllMW1RdlNLbUNGTityZlg3bTlDb1lLYU16UURaU0FReklmRzRJbjl2VnR3NURDNjBhTGljMldIOXFMU0ZwNDB0S0lmbDE5VDgxNlM0NlZ1TE9xQ2EyYWg1REVUdVorb2JDd3E4czNpZGdyL2lrUm9FSVNHMUdUQmFjNXY4cDM0ZHJyR3g0aEVqbmxrOXpyT2hGNGM3MUhNYTlkM0xWS2JrVnhNYVc3ZHNFbXA2bmNDN1FMMzJSeUcvYzVjZS0tWmhwUklWVFRRQkZwWmw0QVQ0Uy8yUT09--e67db560fd968823997e304e4437dc79a5e231ca',
        'Origin': 'https://e.gitee.com',
        'Referer': 'https://e.gitee.com/'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    return response.text

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    current_time = str(date.today())
    res = json.loads(getIssueOverview())
    bug_total_count = res['total_count']
    bug_finish_count = res['finished_count']
    bug_unsolved_count = int(bug_total_count)-int(bug_finish_count)
    bug_list = json.loads(get_issue_trend())
    for i in bug_list:
        if i["date"] == current_time:
            bug_new_create = i["created_count"]

    bug_member_info = json.loads(get_issue_rank())
    bug_members_list = bug_member_info["members"]
    # for i in bug_member_info["members"]:
    #     bug_members_list.append(i)
    bug_member_nums = bug_member_info["total_count"]
    # for i in bug_member_info["total_count"]:
    #     bug_member_nums.append(i)
    bug_info = {
        "bug_total_count": bug_total_count,
        "bug_new_create": bug_new_create,
        "bug_unsolved_count": bug_unsolved_count,
        "bug_members_list": bug_members_list,
        "bug_member_nums": bug_member_nums

    }
    webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=468a19ea-12e2-42b2-a479-5c5c6e221672"
    content = "【i检验进度汇报】"
    mentioned_list = ["@all",]
    mentioned_mobile_list = None
    send_text(webhook, content, mentioned_list,bug_info)



