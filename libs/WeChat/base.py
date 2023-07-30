# coding: utf-8
import hashlib
import json
import logging
import random
import string

import requests
import time

from django.core.cache import cache

from libs.WeChat import config
from libs.utils import db
from dj2.settings import GHAT_ID
from libs.utils.redis_com import rd
log = logging.getLogger(__name__)


class WebChatBase(object):
    def __init__(self, app_id=1):
        self.app_id = config.WC_CONFIG[app_id]['app_id']
        self.app_secret = config.WC_CONFIG[app_id]['app_secret']
        self.webChat_domain = config.WC_CONFIG[app_id]['webchat_domain']
        self.cache_key = config.WC_CONFIG[app_id]['cache_key']
        self.redirect_uri = config.WC_CONFIG[app_id]['redirect_uri']
        self.WECHAT_TMPLATE_ID = config.WC_CONFIG[app_id]['template_id']
        self.timeout = 7200

    def get_access_token(self):
        # 获取token
        wx_app = db.default.wx_app.get(app_id=self.app_id)
        token = wx_app.access_token
        token_timeout = wx_app.token_timeout
        now = int(time.time())
        if now > token_timeout:
            """如果token已过期"""
            result = self.get_remote_token()
            token = result.get('access_token')
            token_timeout = now + 7200
            if token:
                db.default.wx_app.filter(app_id=self.app_id).update(access_token=token, token_timeout=token_timeout)
        return token

    def get_remote_token(self):
        # 请求微信access_token
        path = 'cgi-bin/token'
        args = (self.app_id, self.app_secret)
        query_string = 'grant_type=client_credential&appid=%s&secret=%s' % args
        result = self.request_api(path, query_string)
        return result

    def get_ip_list(self, access_token):
        # 获取ip集合
        if not access_token:
            return {}
        path = 'cgi-bin/getcallbackip'
        args = 'access_token=%s' % access_token
        return self.request_api(path, args)

    def request_api(self, path, query_string='', data='', body={}, headers={}, method='get'):
        # 请求微信服务基础接口
        url = 'https://%s/%s?%s' % (self.webChat_domain, path, query_string)
        print(url)
        args = [url]
        if data and method == 'post':
            args.append(data)

        # 日志输出url及参数信息
        logging.info('START REQUEST[%s]: %s' % (method.upper(), url))
        if data:
            logging.info('***params***:%s', data)
        # 获取方法
        meth = getattr(requests, method)
        if body:
            body = json.dumps(body, ensure_ascii=False).encode('utf-8')
            r = meth(*args, data=body, headers=headers)
        else:
            r = meth(*args, headers=headers)
        r.encoding = 'utf-8'
        d = r.json()
        # 如果查询结果出现问题，打印
        if d.get('errcode', 0):
            log.error(f"error: {d} post_url: {url}")
            if d.get('errcode', 0) == 40001:
                db.default.wx_app.filter(app_id=self.app_id).update(access_token='token', token_timeout=0)
        return d



class BaseClient(object):

    def __init__(self, token=None):
        self.access_token = token if token else WebChatBase(GHAT_ID).get_access_token()

    def get(self, path):
        query_string = 'access_token=%s' % self.access_token
        d = WebChatBase(GHAT_ID).request_api(path, query_string)
        return d

    def post(self, path, data):
        query_string = 'access_token=%s' % self.access_token
        d = WebChatBase(GHAT_ID).request_api(path, query_string, data=data, method="post")
        return d



class JsSign(WebChatBase):
    def __init__(self, url, wx_type=2):
        self.wx_type = wx_type
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'timestamp': self.__create_timestamp(),
            'url': url
        }
        WebChatBase.__init__(self, wx_type)

    @staticmethod
    def __create_nonce_str():
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    @staticmethod
    def __create_timestamp():
        return int(time.time())

    def get_ticket(self):
        ticket_name = "wx-ticket"
        ticket = rd.user_code.get(ticket_name)  # 缓存验证码
        if not ticket:
            access_token = self.get_access_token()
            path = "cgi-bin/ticket/getticket"
            args = "access_token=%s&type=jsapi" % access_token
            ticket = self.request_api(path, args).get("ticket")
            rd.user_code.set(ticket_name, ticket, timeout=60 * 60)  # 设置缓存key 过期时间
        return ticket

    def sign(self):
        out = self.ret
        self.ret['jsapi_ticket'] = self.get_ticket()
        keys = list(self.ret.keys())
        keys.sort()
        sign = "&".join("%s=%s" % (k.lower(), self.ret[k]) for k in keys)
        sha1 = hashlib.sha1()
        sha1.update(sign.encode())
        out['signature'] = sha1.hexdigest()
        return out
