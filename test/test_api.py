#_*_coding:utf-8 _*_
__author__ = 'yuanyuan'
__date__ = '2018/6/23 下午4:12'

from pithy import request
import pytest

from API import get



@pytest.mark.bvt
class TestApi:

    @classmethod
    def test_setUp(cls):
        cls.app = get.DemoAPP()

    def test_get(self):

        r = get.DemoAPP().get('123').json

        assert r.args.key == '123'



