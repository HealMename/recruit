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
        phone = req_dict.pop('phone', '')
        token = auth_token.create_token(tablename, req_dict.get("id"))
        msg['data']["id"] = req_dict.get("id")
        msg["id"] = req_dict.get("id")
        msg['token'] = token
        msg['open_role'] = ','.join([str(x.type) for x in db.default.users.filter(
                            username=phone, status=1)])
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
                msg['msg'] = '登陆信息已失效'
                msg['code'] = 401
                result = msg
                return result
            datas = users.getbyparams(users, users, {'id': user_info['user_id']})
            if not datas:
                msg['msg'] = '登陆信息已失效'
                msg['code'] = 401
                result = msg
            else:
                request.user = Struct(datas[0])
                datas[0]['nickname'] = request.user.username
                datas[0]['open_role'] = ','.join(
                    [str(x.type) for x in db.default.users.filter(
                        username=request.user.username, status=1)])
                request.user = Struct(datas[0])
                request.user.shouji = request.user.username
                request.user.detail = db.default.user_tea_det.get(user_id=request.user.id, status=1)
                request.session['tablename'] = 'users'
                msg['msg'] = '身份验证通过。'
                msg['user'] = Struct(datas[0])
                result = msg

        else:
            msg['code'] = 401
            msg['msg'] = 'not user'
            result = msg
        return result
