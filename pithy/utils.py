#_*_coding:utf-8 _*_
__author__ = 'yuanyuan'
__date__ = '2018/6/24 下午3:12'

import json
import time
import sys
from functools import wraps


def fn_timer(function):
    """
    元素查找计时器
    :param function:
    :return:
    """

    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        total = str(t1-t0)
        return total, result

    return function_timer


def format_json(content):
    '''
    格式化json
    :param content:
    :return:
    '''

    #先解码
    if isinstance(content, str):
        content = json.loads(content)

    result = json.dumps(content, sort_keys=True, indent=4, separators=(',', ': ')). \
        encode('latin-1').decode('unicode_escape')

    return result

def pretty_print(content):

    print(format_json(content))

