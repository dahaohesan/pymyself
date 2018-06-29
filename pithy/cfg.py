#_*_coding:utf-8 _*_
__author__ = 'yuanyuan'
__date__ = '2018/6/26 下午4:23'

import os
import sys
import json
import yaml
from configobj import ConfigObj


class Config:
    '''
    读取配置文件
    1.优先读取当前目录，第二顺序读取根目录
    2.同一名称配置文件只加载一次，再次实例化不再加载 是因为重载了__new__方法！！！！！
    '''

    config_object_instance = {}

    def  __new__(cls, file_name='cfg.yaml'):
        if file_name not in cls.config_object_instance:
            config_file_path = file_name
            #如果不在当前目录
            if not os.path.exists(file_name):
                config_file_path0 = os.path.join(sys.path[0], file_name)
                config_file_path1 = os.path.join(sys.path[1], file_name)
                if os.path.exists(config_file_path0):
                    config_file_path = config_file_path0
                elif os.path.exists(config_file_path1):
                    config_file_path = config_file_path1
                else:
                    raise OSError('can not find config file')
            #存在当前目录
            if file_name.endswith('yaml'):
                cls.config_object_instance[file_name] = yaml.load(open(config_file_path))
            elif file_name.endswith(('.cfg', '.ini', '.conf')):
                cls.config_object_instance[file_name] = ConfigObj(config_file_path)
            elif file_name.endswith('.json'):
                cls.config_object_instance[file_name] = json.load(open(config_file_path))
            else:
                raise ValueError('Unsuported configuration file type')
        return cls.config_object_instance[file_name]

    #重定向到字典，可以这样使用Config()[key]
    def __getitem__(self, item):
        return self[item]





