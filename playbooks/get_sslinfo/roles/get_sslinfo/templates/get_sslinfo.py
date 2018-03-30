#!/usr/bin/env python
#coding:utf-8
#__author__="ybh"
import os
import time
import json
import requests
import hashlib
import commands
IP="{{ inventory_hostname }}"
BASE_DIR="/etc/letsencrypt/live"
API="https://oapi.dingtalk.com/robot/send?access_token=07133fed0a8d1c70c34c279653967514ced6f3b3de194b5824250218f9034cef"
CMDB_API="http://miguanvpn2.f3322.net:23336/api/cdn/update_https/"
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
            text += "## 提示\n\n>%s SSL证书已更新！\n\n " % domain
            message=update_https(domain)
            try:
                text += "## 注意\n\n>%s \n\n" % message
            except Exception as e:
                text += "## 注意\n\n>%s \n\n" % message.encode('utf-8')
            text += "## 到期时间\n\n>%s \n\n" % time.strftime("%Y-%m-%d", time.localtime(expire_time))
    if text!="":
        result=send_to_dingding(text)
        return result



def update_https(domain):
    cmd="/usr/bin/certbot certificates 2> /dev/null|grep 'Certificate Name: %s' -A 1|grep Domains|cut -d ' ' -f 6-" % (domain,domain)
    result=commands.getoutput(cmd)
    subdomain_list=result.split()
    text=""
    for subdomain in subdomain_list:
        current_time=int(time.time())
        m=hashlib.md5()
        m.update((str(current_time)+'miguan').encode('utf-8'))
        token=m.hexdigest()
        payload={}
        payload['timestamp']=int(time.time())
        payload['token']=token
        payload['domain_name']=subdomain
        payload['ip']=IP
        f=open('%s/%s/fullchain.pem' % (BASE_DIR,domain),'r')
        certificate=f.read()
        f.close()
        f=open('%s/%s/privkey.pem' % (BASE_DIR,domain),'r')
        privatekey=f.read()
        f.close()
        payload['certificate']=certificate
        payload['privatekey']=privatekey
        req=requests.post(CMDB_API,data=payload)
        req=req.json()
        if len(req.keys())==1:
            text +="%s 更新cdn证书成功！" % subdomain
        else:
            text +=req['message']
    return text


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
