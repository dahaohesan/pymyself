# _*_coding:utf-8 _*_
from copy import deepcopy

from pithy.utils import format_json

__author__ = 'yuanyuan'
__date__ = '2018/6/19 下午2:33'

from jinja2 import Template
from requests.sessions import Session
from jinja2 import Template
import inspect
from collections import OrderedDict


# 类装饰器对类的方法进行装饰
class HttpRequet:
    def __init__(self, url='', method='get', **kwargs):
        self.url = url
        self.method = method
        self.decorator_args = kwargs
        self.func_return = None  # 相当于接口传的参数
        self.fun_doc = None
        self.func_im_self = None

    # 使用call方法类实例可调用，等同于HttpRequest(func)=HttpRequest.__call__(func)
    def __call__(self, func):
        self.func = func  # func就是get方法
        self.is_class = False
        # 判断是不是实例方法，排除静态方法和类方法     （类装饰器可以装饰类也可以装饰函数
        try:
            # 获取函数的参数
            if inspect.getargspec(func).args[0] == 'self':
                self.is_class = True  # True代表装饰的是函数
        except IndexError:
            pass

        # 装饰器
        # args就是自己写的类
        # get有两个参数self:DemoApp 实例和value
        def fun_wrapper(*args, **kwargs):
            self.func_return = self.func(*args, **kwargs) or {}
            self.func_im_self = args[0] if self.is_class else object

            # try:
            #     self.func.__doc__ = self.func.__doc__.decode('utf-8')
            # except:
            #     pass

            # self.func.__name__就是接口的名字
            self.func_doc = (self.func.__doc__ or self.func.__name__).strip()
            self.create_url()
            self.create_session()
            self.session.headers.update(getattr(self.func_im_self, 'headers', {}))
            self.decorator_args.update(self.func_return)
            # 开始请求接口
            return Request(self.method, self.url, self.session, self.fun_doc, self.decorator_args)

        return fun_wrapper

    def create_url(self):

        # self.func_im_self是实例
        base_url = getattr(self.func_im_self, 'base_url', '')
        # 去掉url这个键 什么意思？？？？这一步是干什么的？？？？
        # self.url = self.func_return.pop('url', None) or self.url
        self.url = base_url + self.url

    def create_session(self):

        # 装饰对象是方法
        if self.is_class:
            self.session = getattr(self.func_im_self, 'session', None)
            if not isinstance(self.session, Session):
                session = Session()
                setattr(self.func_im_self, 'session', session)

                # 接口集合的实例的session实例，然后同一个会话实例请求所有的接口

                # DemoAPP实例含有Session(), 此时装饰器和DemoApp含有共同的Session()实例
                self.session = session

        # 不知道什么时候会是下面两种情况？？？？？？
        elif isinstance(self.func_return.get('session'), Session):
            self.session = self.func_return.get('session')


        else:
            self.session = Session()


request = HttpRequet

LOG_TEMPLATE = u'''
***********************************
{% for index, item in items%}
{{ index+1 }}. {{ item['desc'] }}
{{ item['value'] }}
{{ endfor }}
'''


def context(func):
    def wrapper(self):
        # 调用这个接口的结果存在self.response
        self._request()
        try:
            res = func(self)
        finally:
            self._log()
        return res

    return wrapper


class Request:
    '''
    请求对象模型
    '''

    def __init__(self, method, url, session, doc, args):
        self.method = method
        self.url = url
        self.session = session
        self.doc = doc  # 接口描述
        self.args = args  # 接口传的数据

        self.response = None
        self.log_content = [
            dict(desc=u'接口描述', value=doc),
            dict(desc=u'请求url', value=url),
            dict(desc=u'请求方法', value=method),
        ]

        # 参数序列化
        for i in ['params', 'data']:
            if args.get[i]:
                args[i] = self.fixation_order(args[i])

    @staticmethod
    def fixation_order(d):
        o = OrderedDict()
        # i是键
        for i in d:
            #
            o[i] = d[i]
        return o

    def prepare_log(self):
        # 有下面一步这一步需要吗？？？ ----headers没定义，需要
        headers = deepcopy(self.args.get('headers', {}))
        headers.update(self.session.headers)

        if headers:
            self.log_content.append(dict(
                desc=u'请求headers', value=format_json(self.args.get('params'))
            ))

        if self.args.get('params'):
            self.log_content.append(dict(
                desc=u'请求url参数', value=format_json(self.args.get('params'))
            ))

        if self.args.get('data'):
            self.log_content.append(dict(
                desc=u'body参数', value=format_json(self.args.get('data'))
            ))

        if self.args.get('json'):
            self.log_content.append(dict(
                desc=u'body参数', value=format_json(self.args.get('json'))
            ))

    @context
    # 转化json格式的数据  并格式化输出
    def to_json(self):
        try:
            response_json = self.response.json()
            self.log_content.append(dict(
                desc=u'响应结果',
                value=format_json(response_json)
            ))
        except ValueError:
            self.log_content.append(dict(
                desc=u'响应结果',
                value=self.response.content.decode('utf-8')
            ))
            raise ValueError(u'No JSON object in response')

        return JSONProcessor(response_json)

    @context
    def to_content(self):
        # .content   转成二进制数据
        response_content = self.response.content()

    # 使用property装饰器该方法可以当做属性来使用
    @property
    def json(self):
        return self.to_json()

    @property
    def content(self):
        return self.to_content()

    # 返回接口的结果
    def _request(self):
        if not self.response:
            self.prepare_log()
            # 《《所以接口就是用requests.Session().request()方法请求的》》
            self.response = self.session.request(self.method, self.url, *self.args)

    # 日志模板使用jinja2模板渲染
    def _log(self):
        print(Template(LOG_TEMPLATE).render(items=enumerate(self.log_content)))

    # 这个什么时候用？？？
    def __getattr__(self, item):
        self._request()
        self._log()
        return getattr(self.response, item)
