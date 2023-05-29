# coding:utf-8
# author:ila
import base64, copy
from django.http import JsonResponse
from django.apps import apps

from libs.utils import Struct, db, auth_token
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
        token = token or request.QUERY.get("token") \
                or request.META.get('HTTP_TOKEN') \
                or request.COOKIES.get('token')
        if token and token != "null":
            user_info = auth_token.decode_token(token)
            if not user_info:
                msg['code'] = username_error_code
                msg['msg'] = '找不到该用户信息'
                result = msg
                return result
            tablename = user_info.get('tablename')
            datas = None
            allModels = apps.get_app_config('main').get_models()
            for model in allModels:
                if model.__tablename__ == tablename:
                    datas = model.getbyparams(model, model, {'id': user_info['user_id']})
                    break
            if not datas:
                msg['code'] = username_error_code
                msg['msg'] = '找不到该用户信息'
                result = msg
            else:
                request.user = Struct(datas[0])

                if request.user.yonghuzhanghao:
                    request.user.role = '用户'
                    request.user.username = request.user.yonghuzhanghao
                    datas[0]['username'] = request.user.yonghuzhanghao
                if request.user.role == '教师' or request.user.role == '面试官':
                    request.user.shouji = db.default.user_tea_det.get(user_id=request.user.id).phone_number
                request.session['tablename'] = tablename
                msg['msg'] = '身份验证通过。'
                msg['user'] = Struct(datas[0])
                result = msg

        else:
            msg['code'] = 401
            msg['msg'] = 'headers未包含认证信息。'
            result = msg
        return result
