# coding:utf-8
# author:ila
import base64, copy
from django.http import JsonResponse
from django.apps import apps

from libs.utils import Struct, db, auth_token
from main.users_model import users
from util.codes import *
from util import message as mes


class Auth(object):
    def authenticate(self, model, req_dict):
        """
        用户登录，登录成功返回token；登录失败返回失败原因
        :param username:账号
        :param password:密码
        :return: json
        """
        msg = {'code': normal_code, 'msg': mes.normal_code, 'data': {}}
        tablename = model.__tablename__
        token = auth_token.create_token(tablename, req_dict.get("id"))
        msg['data']["id"] = req_dict.get("id")
        msg["id"] = req_dict.get("id")
        msg['token'] = token
        return JsonResponse(msg)

    def identify(self, request, token=''):
        """
        用户鉴权
        :param request:本次请求对象
        :return: list
        """

        msg = {'code': normal_code, 'msg': mes.normal_code, 'data': {}}
        # django的header被处理过了
        token = token or request.QUERY.get("token") or request.META.get('HTTP_TOKEN')
        if token and token != "null":
            user_info = auth_token.decode_token(token)
            if not user_info:
                msg['msg'] = '找不到该用户信息'
                result = msg
                return result
            datas = users.getbyparams(users, users, {'id': user_info['user_id']})
            if not datas:
                msg['msg'] = '找不到该用户信息'
                result = msg
            else:
                request.user = Struct(datas[0])

                if request.user.role == '用户':
                    request.user.shouji = request.user.username
                    datas[0]['nickname'] = request.user.username
                    datas[0]['open_role'] = []
                    if db.default.users.get(username=request.user.username, type=3, status=1):
                        datas[0]['open_role'].append('3')
                    if db.default.users.get(username=request.user.username, type=2, status=1):
                        datas[0]['open_role'].append('2')
                    datas[0]['open_role'] = ','.join(datas[0]['open_role'])
                else:
                    datas[0]['nickname'] = request.user.gongsimingcheng
                request.session['tablename'] = 'users'
                msg['msg'] = '身份验证通过。'
                msg['user'] = Struct(datas[0])
                result = msg

        else:
            msg['code'] = 401
            msg['msg'] = 'headers未包含认证信息。'
            result = msg
        return result
