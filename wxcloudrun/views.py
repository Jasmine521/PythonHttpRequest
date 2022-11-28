import json
import logging
import requests

from django.http import JsonResponse
from django.shortcuts import render
from wxcloudrun.models import Counters, Token

logger = logging.getLogger('log')


def index(request, _):
    """
    获取主页

     `` request `` 请求对象
    """

    return render(request, 'index.html')


def counter(request, _):
    """
    获取当前计数

     `` request `` 请求对象
    """

    rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'GET' or request.method == 'get':
        rsp = get_count()
    elif request.method == 'POST' or request.method == 'post':
        rsp = update_count(request)
    else:
        rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
                            json_dumps_params={'ensure_ascii': False})
    logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
    return rsp


def get_count():
    """
    获取当前计数
    """

    try:
        data = Counters.objects.get(id=1)
    except Counters.DoesNotExist:
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'code': 0, 'data': data.count},
                        json_dumps_params={'ensure_ascii': False})


def update_count(request):
    """
    更新计数，自增或者清零

    `` request `` 请求对象
    """

    logger.info('update_count req: {}'.format(request.body))

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if 'action' not in body:
        return JsonResponse({'code': -1, 'errorMsg': '缺少action参数'},
                            json_dumps_params={'ensure_ascii': False})

    if body['action'] == 'inc':
        try:
            data = Counters.objects.get(id=1)
        except Counters.DoesNotExist:
            data = Counters()
        data.id = 1
        data.count += 1
        data.save()
        return JsonResponse({'code': 0, "data": data.count},
                    json_dumps_params={'ensure_ascii': False})
    elif body['action'] == 'clear':
        try:
            data = Counters.objects.get(id=1)
            data.delete()
        except Counters.DoesNotExist:
            logger.info('record not exist')
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'code': -1, 'errorMsg': 'action参数错误'},
                    json_dumps_params={'ensure_ascii': False})


# 地区列表
courselisturl = 'https://qcsh.h5yunban.com/youth-learning/cgi-bin/common-api/organization/children'
# 地区参数
courselistpay = {'pid':'N'}
def getregionlist(request):
    """
    怎么说呢 就是获取列表再返回
    """
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    logger.info("body： "+body)
    if 'pid' not in body:
        return JsonResponse({'code': -1, 'errorMsg': '缺少pid参数'},
                            json_dumps_params={'ensure_ascii': False})
    courselistpay['pid'] = body['pid']

    r = requests.get(courselisturl,params=courselistpay)
    if r.status_code == '200':
        return JsonResponse({'code': 0, "data": json.loads(r.text)['result']},
                        json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'code': -1, 'errorMsg': '无法获取列表信息'},
                            json_dumps_params={'ensure_ascii': False})

courseurl = 'https://qcsh.h5yunban.com/youth-learning/cgi-bin/common-api/course/current'

payload1 = {'openid':'okMqsjkGt9CenI2WgTnDEPFcpEDc'}

tokenurl =  'https://qcsh.h5yunban.com/youth-learning/cgi-bin/login/we-chat/callback?callback=https%3A%2F%2Fqcsh.h5yunban.com%2Fyouth-learning%2Fmine.php&scope=snsapi_userinfo&appid=wxa693f4127cc93fad&nickname=%25E4%25BA%2591%25E5%25B8%25B8%25E8%2588%2592%25E6%25B0%25B4%25E9%2595%25BF%25E4%25B8%259C&headimg=https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FUIIYUMuyKFoKXicO6b6KQw34JfmpFkfwo3MHd5SkqA78iaZeZsERibWIDEicWV1HFT6gZMY6gcDa8AfHmaPzlBAToQ%2F132&time=1668496003&source=common&sign=C218A223236B18AC4039701DADD93Cs12&t=1768496003 '

def createToken(request):
    """
    创建人物啦
    """
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    try:
        data = Token.objects.get(openid=body['openid'])
    except Token.DoesNotExist:
        data = Token()
    data.openid = body['openid']
    data.qcshopenid = body['qcshopenid']
    payload1['openid'] = data.qcshopenid
    data.qcshtoken = requests.get(tokenurl,params=payload1['openid'])
    data.pid = body['pid']
    data.name = body['name']
    data.save()

openidurl = 'https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code'
appid = 'wxf68d915fdfbf2513'
def getOpenId(request):
    logger.info('getOpenId req: {}'.format(request.body))
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    logger.info('body: {}'.body)
    openidurl.replace('APPID',appid).replace('JSCODE',body['code'])
    r = requests.get(url=openidurl)
    if r.status_code == '200':
        return JsonResponse({'code': 0, "data": json.loads(r.text)['result']},
                            json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'code': -1, 'errorMsg': '无法获取列表信息'},
                            json_dumps_params={'ensure_ascii': False})