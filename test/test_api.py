#_*_coding:utf-8 _*_
__author__ = 'yuanyuan'
__date__ = '2018/6/23 下午4:12'

from pithy import request
import pytest

class DemoAPP:

    def __init__(self):
        self.base_url = ''

    @request(url='')
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

    @request(url='', method='post')
    def _login(self, value):
        data={
            '': value
        }

        return dict(data = data)

@pytest.mark.bvt
class TestApi(pytest):

    def setUp(self):
        self.app = DemoAPP()

    def test_get(self):

        r = DemoAPP().get('').json
        assert r.agrs.key == 123
