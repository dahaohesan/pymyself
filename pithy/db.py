#_*_coding:utf-8 _*_
__author__ = 'yuanyuan'
__date__ = '2018/6/26 下午8:44'

import sys
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class DB:
    def __init__(self, database_info, name):
        self.database_info = database_info
        self.name = name
        self.base = None
        self.session = None

    def load(self):
        self._init_db()
        sys.modules[self.database_name] = self

    def _init_db(self):
        #不关心数据库表的内部结构，自动映射
        self.base = automap_base()
        #数据库初始化连接
        engine = create_engine(self.database_info)
        engine.pool.status()
        self.base.prepare(engine, reflact=True)
        self.session=Session(engine)