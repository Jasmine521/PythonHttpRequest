import json
import sched

import pymysql
from datetime import datetime

import requests

from wxcloudrun.models import Token
ul1 =  'https://qcsh.h5yunban.com/youth-learning/cgi-bin/login/we-chat/callback?callback=https%3A%2F%2Fqcsh.h5yunban.com%2Fyouth-learning%2Fmine.php&scope=snsapi_userinfo&appid=wxa693f4127cc93fad&nickname=%25E4%25BA%2591%25E5%25B8%25B8%25E8%2588%2592%25E6%25B0%25B4%25E9%2595%25BF%25E4%25B8%259C&headimg=https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FUIIYUMuyKFoKXicO6b6KQw34JfmpFkfwo3MHd5SkqA78iaZeZsERibWIDEicWV1HFT6gZMY6gcDa8AfHmaPzlBAToQ%2F132&time=1668496003&source=common&sign=C218A223236B18AC4039701DADD93Cs12&t=1768496003 '

payjoin = {'accessToken': '6885F968-7377-427D-8689-B9BADE217450'}
payload1 = {'openid':'okMqsjkGt9CenI2WgTnDEPFcpEDc'}

joincourse='https://qcsh.h5yunban.com/youth-learning/cgi-bin/user-api/course/join'
courseurl = 'https://qcsh.h5yunban.com/youth-learning/cgi-bin/common-api/course/current'
dict = {'course': 'C1046', 'nid': 'N0002000600081015', 'cardNo': '颜久博'}
def job_function():
    # 根据openid获取token再去获取课程id
    r = requests.get(ul1, params=payload1)
    payjoin['accessToken'] = r.text.split('\'')[3]

    r = requests.get(courseurl, params=payjoin)
    rs = r.text.split("\"")
    courseId = rs[rs.index('id') + 2]
    dict['course'] = courseId

    tokens = Token.objects.all()
    for t in tokens:
        payload1['openid'] = t.qcshopenid
        r = requests.get(ul1, params=payload1)
        payjoin['accessToken'] = r.text.split('\'')[3]
        dict['nid'] = t.pid
        dict['cardNo'] = t.name
        joindata = json.dumps(dict)
        r = requests.get(joincourse,params=payjoin,data=joindata)
        print(r.text)
    print("完成一轮学习捏")
# 每两小时执行一次
sched.add_job(job_function, 'interval', mins=1)
pymysql.install_as_MySQLdb()
