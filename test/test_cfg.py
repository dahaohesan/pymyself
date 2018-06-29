#_*_coding:utf-8 _*_
__author__ = 'yuanyuan'
__date__ = '2018/6/26 下午4:47'
import pytest
from pithy import Config

@pytest.mark.bvt
class TestA:

    def test_json_cfg(self):
        cfg= Config('cfg.json')
        assert cfg['a'] == 1


    def test_yaml(self):
        cfg= Config('cfg.yaml')
        assert cfg['user'] == 'admi'
