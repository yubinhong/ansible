#!/usr/bin/env python
#coding:utf-8
#__author__="ybh"
import os
import time
import json
import requests
IP="{{ inventory_hostname }}"
BASE_DIR="/etc/letsencrypt/live"
API="https://oapi.dingtalk.com/robot/send?access_token=07133fed0a8d1c70c34c279653967514ced6f3b3de194b5824250218f9034cef"
def main():
    domain_list=os.listdir(BASE_DIR)
    text=""
    for domain in domain_list:
        file_path="%s/%s" % (BASE_DIR,domain)
        ctime=os.stat(file_path)[9]
        current_time=time.time()
        expire_time=60 * 60 * 24 * 90 + int(ctime)
        free_time = expire_time - int(current_time)

        if free_time < 60*60*24*30 and free_time >= 60*60*24*29:
            text += "## 服务器\n\n>%s \n\n" % IP
            text += "## 信息\n\n>%s SSL证书有效期不足30天，请即时更新！\n\n " % domain
            text += "## 到期时间\n\n%s \n\n" % time.strftime("%Y-%m-%d",time.localtime(expire_time))
        elif free_time < 60*60*24*15 and 60*60*24*14:
            text += "## 服务器\n\n>%s \n\n" % IP
            text += "## 信息\n\n>%s SSL证书有效期不足15天，请及时更新！\n\n " % domain
            text += "## 到期时间\n\n%s \n\n" % time.strftime("%Y-%m-%d", time.localtime(expire_time))
        elif free_time < 60*60*24*7 and 60*60*24*6:
            text += "## 服务器\n\n>%s \n\n" % IP
            text += "## 警告\n\n>%s SSL证书有效期不足7天，请及时更新！\n\n " % domain
            text += "## 到期时间\n\n%s \n\n" % time.strftime("%Y-%m-%d", time.localtime(expire_time))
        elif free_time > 60*60*24*89 and free_time < 60*60*24*90:
            text += "## 服务器\n\n>%s \n\n" % IP
            text += "## 提示\n\n>%s SSL证书已更新！如有加CDN，请即时更新CDN证书\n\n " % domain
            text += "## 到期时间\n\n%s \n\n" % time.strftime("%Y-%m-%d", time.localtime(expire_time))
    if text!="":
        result=send_to_dingding(text)
        return result




def send_to_dingding(text):
    headers = {'content-type': 'application/json'}
    parames = {
        "msgtype": "markdown",
        "markdown": {
            "title": "SSL证书",
            "text": text
        },
    }
    parames = json.dumps(parames)
    r = requests.post(API, data=parames, headers=headers)
    return r.text


if __name__=='__main__':
    result=main()
    if result:
        print(result)

