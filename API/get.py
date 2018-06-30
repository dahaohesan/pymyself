#_*_coding:utf-8 _*_
__author__ = 'yuanyuan'
__date__ = '2018/6/30 下午1:08'

from pithy.api import request


class DemoAPP:

    def __init__(self):
        self.base_url = 'http://httpbin.org'

    @request(url='get')
    def get(self, value):
        '''
        get接口
        :param value:
        :return:
        '''
        params = {
            'key': value
        }

        return dict(params=params)