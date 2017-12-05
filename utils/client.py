import base64
import hashlib
import time
import logging

import requests

from config.config import config


def get_data(url, payload, method='GET'):
    payload['request_ts'] = int(time.time())

    headers = {
        'User-Agent': config.lian_jia['ua'],
        'Authorization': get_token(payload)
    }
    func = requests.get if method == 'GET' else requests.post
    r = {"total_count":0,"has_more_data":False}
    try:
        r = func(url, payload, headers=headers)    
    except Exception as e:
        logging.info('请求出错：'+str(e))
        return r
    

    return parse_data(r)


def parse_data(response):
    as_json = response.json()

    if as_json['errno']:
        # 发生了错误
        raise Exception('请求出错了: ' + as_json['error'])

    else:
        return as_json['data']


def get_token(params):
    data = list(params.items())
    data.sort()

    token = config.lian_jia['app_secret']

    for entry in data:
        token += '{}={}'.format(*entry)

    token = hashlib.sha1(token.encode()).hexdigest()
    token = '{}:{}'.format(config.lian_jia['app_id'], token)
    token = base64.b64encode(token.encode()).decode()

    return token
