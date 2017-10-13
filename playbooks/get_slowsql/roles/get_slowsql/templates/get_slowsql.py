#!/usr/bin/env python
#coding:utf-8
#__author__="ybh"
import linecache
import requests
import json
import sys
IP="{{ ansible_all_ipv4_addresses.0 }}"
FILE_PATH="/data0/mysql/3306/logs/mysql-slow.log"
COUNT_FILE="/tmp/count.txt"
API="https://oapi.dingtalk.com/robot/send?access_token=2ae59053f2340e19eb9adc1e00e8b25c9bdc25c8e3870abe9f7580b942f2139a"


def write_count(count):
    f=open(COUNT_FILE,'w')
    f.write(str(count))
    f.close()


def get_count():
    try:
        count=int(linecache.getline(COUNT_FILE,1))
    except Exception as e:
        count=0
    return count


def send_to_dingding(sql_text):
    headers={'content-type':'application/json'}
    parames={
        "msgtype":"markdown",
        "markdown":{
            "title":"SQL 慢查询",
            "text": sql_text
        },
    }
    parames=json.dumps(parames)
    r=requests.post(API,data=parames,headers=headers)
    return r.text

def main():
    count=0
    try:
        for count,line in enumerate(open(FILE_PATH,"rU")):
            pass
    except Exception as e:
        sys.exit(1)
    count +=1
    old_count=get_count()
    if old_count == 0:
        write_count(count)
        sys.exit(0)
    result=count-old_count
    if result !=0:
        write_count(count)
        sql_text="## 服务器:%s\n\n" % (IP)
        flag=0
        for i in range(1,result+1):
            line=linecache.getline(FILE_PATH,old_count+i)
            if "Schema" in line:
                db=line.split()[2]
                sql_text += "## 数据库\n\n> %s\n\n" % db
            elif "Query_time" in line:
                time=line.split()[2]
                sql_text += "## 耗时\n\n> %s秒\n\n" % time
            elif "SELECT" in line or "UPDATE" in line or "INSERT" in line or "DELETE" in line:
                flag=1
                sql_text += "## SQL\n\n> %s" % line.strip("\n")
            elif flag==1:
                sql_text += "%s" % line.strip("\n")
        sql_text += "\n\n<a href='http://sql.miguan.com/'>详情</a>"

        print(send_to_dingding(sql_text))


if __name__=="__main__":
    main()

