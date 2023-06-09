import time

from django.http import JsonResponse
from django.shortcuts import render

from dj2.common import get_user_id
from libs.utils.auth_token import get_random_string
from libs.utils.redis_com import rd
from main.models import yonghu, gongsi
from util.codes import *

from libs.utils import ajax, db, auth_token
from libs.utils.common import Struct, render_template, num_to_ch
from main.users_model import users
from util.auth import Auth

role_dict = {"管理员": 1, "出题专家": 2, "面试官": 3, "用户": 4, "公司": 5}


def verify_(code, phone, code_id):
    """校验验证码"""
    if code == '425381':  # 万能验证码
        return True
    redis_key = f"{phone}:{code_id}"
    rd_code = rd.user_code.get(redis_key)  # 缓存验证码
    if rd_code == code:
        rd.user_code.delete(redis_key)  # 验证成功删除缓存
        return True
    else:
        return False


def add_tea(request):
    """
    教师注册
    """
    data = Struct()
    if request.method == 'POST':
        args = {k: v for k, v in request.QUERY.items()}
        username = args.pop('username')
        id_ = args.pop('id', 0)
        code = args.pop('code', 0)
        args.pop('token', '')
        phone_number = args['phone_number']
        if get_user_id(phone_number, 2, id_):
            return ajax.ajax_fail(message='手机号已注册教师身份')
        if not verify_(code, phone_number, 3):
            return ajax.ajax_fail(message='验证码错误')
        now = int(time.time())
        if not id_:
            password = get_random_string(length=6, allowed_chars='0123456789')
            password = auth_token.sha1_encode_password(password)  # 加密密码
            id_ = db.default.users.create(username=phone_number, password=password, role='教师', type=2)
            db.default.user_tea_det.create(user_id=id_, nickname=username, add_time=now, **args)
        else:
            args['add_time'] = now
            db.default.users.filter(id=id_).update(username=phone_number)
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


def verify_(code, phone, code_id):
    """校验验证码"""
    if code == '425381':  # 万能验证码
        return True
    redis_key = f"{phone}:{code_id}"
    rd_code = rd.user_code.get(redis_key)  # 缓存验证码
    if rd_code == code:
        rd.user_code.delete(redis_key)  # 验证成功删除缓存
        return True
    else:
        return False


def login(request):
    """
    教师/面试官登录
    """
    if request.method == 'POST':
        args = {k: v for k, v in request.QUERY.items()}
        role = args.pop("role")
        args['type'] = role_dict[role]
        phone = args['username']
        code = args['password']
        type_ = args['type']
        user_id = get_user_id(phone, type_)
        if not user_id:
            return ajax.ajax_fail(message='账号不存在')
        if not verify_(code, phone, 2):
            return ajax.ajax_fail(message='验证码错误')
        args = {'id': user_id}
        args['id'] = user_id
        if type_ in [1, 2, 3]:
            return Auth.authenticate(Auth, users, args)
        elif type_ == 4:
            return Auth.authenticate(Auth, yonghu, args)
        else:
            return Auth.authenticate(Auth, gongsi, args)

