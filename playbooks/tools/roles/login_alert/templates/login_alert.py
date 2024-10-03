#!/usr/bin/python2.7
#_*_coding:utf-8 _*_
#auther:yubinhong
import subprocess
import requests
import sys
import time
import hashlib

reload(sys)
sys.setdefaultencoding('utf-8')

IP = "{{ inventory_hostname }}"


def get_online_info():

    current_time = int(time.time())
    last_min_time = current_time-60
    date_time = time.strftime("%H:%M", time.localtime(last_min_time))
    date_day = time.localtime(last_min_time)[2]
    p = subprocess.Popen("grep '%s %s' /var/log/secure|grep 'Accepted publickey'|egrep -v '10.21.0.128|117.29.165.58|47.75.118.35'|awk '{print $3,$9,$11}' " % (date_day,date_time), shell=True, stdout=subprocess.PIPE)
    result = p.stdout.readlines()
    if len(result) == 0:
        sys.exit()
    text = u'当前主机：' + IP + '\n'
    for line in result:
        text += line
    return text


def main():
    url = "http://wxapi.waterblock.ga/api/v1/post"
    data = {}
    data['user'] = '@all'
    data['agent_id'] = '1000006'
    data['content'] = get_online_info()
    current_time = int(time.time())
    data['time'] = '%s' % current_time
    secure_word = 'DCgbfW8cCaxdDup2' + '%s' % current_time
    s = hashlib.md5()
    s.update(secure_word.encode(encoding='utf-8'))
    data['signature']=s.hexdigest()
    req=requests.post(url, data=data)
    print(req.content)


if __name__ == '__main__':
    main()
