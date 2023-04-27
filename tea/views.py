import time

from django.http import JsonResponse
from django.shortcuts import render
from util.codes import *

from libs.utils import ajax, db, auth_token
from libs.utils.common import Struct, render_template, num_to_ch
from main.users_model import users
from util.auth import Auth


def add_tea(request):
    """
    教师注册
    """
    data = Struct()
    if request.method == 'POST':
        args = {k: v for k, v in request.QUERY.items()}

        id_ = args.pop('id', 0)
        username = args.pop('username', '')
        if db.default.users.filter(username=username, type=3, id__ne=id_):
            return ajax.ajax_fail(message='用户名已存在')
        now = int(time.time())
        if not id_:
            password = args.pop('password1', '')
            args.pop('password2')
            password = auth_token.sha1_encode_password(password)  # 加密密码
            id_ = db.default.users.create(username=username, password=password, role='教师', type=3)
            db.default.user_tea_det.create(user_id=id_, add_time=now, **args)
        else:
            args['add_time'] = now
            db.default.users.filter(id=id_).update(username=username)
            db.default.user_tea_det.filter(user_id=id_).update(**args)
        return ajax.ajax_ok(message='注册成功')

    return render_template(request, 'tea/index.html', data)


def user_info(request):
    """用户信息"""
    id_ = request.QUERY.get('id')
    user = db.default.users.get(id=id_)
    info = db.default.user_tea_det.get(user_id=id_)
    data = {
        'username': user.username,
    }
    data.update(info)
    data['id'] = id_
    return ajax.ajax_ok(data)


def login(request):
    """
    教师注册
    """
    if request.method == 'POST':
        args = {k: v for k, v in request.QUERY.items()}
        args['type'] = 3
        password = args.pop('password')
        datas = users.getbyparams(users, users, args)
        if not datas:
            return ajax.ajax_fail(message='账号不存在请联系管理员！')
        if not auth_token.verify_password(password, datas[0]['password']):
            return ajax.ajax_fail(message='密码不正确请重试！')
        args['id'] = datas[0].get('id')
        return Auth.authenticate(Auth, users, args)
