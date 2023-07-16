# coding:utf-8
import json

import requests

from dj2.common import get_user_id
from libs.utils.redis_com import rd

from dj2.settings import SMS_API
from libs.utils import ajax, db, render_template
from libs.utils.auth_token import get_random_string

ROLE_ID = {
    "管理员": 1,
    "出题专家": 2,
    "面试官": 3,
    "用户": 4,
    "企业": 5,
}


def call_index(request):
    """视频面试"""
    return render_template(request, 'call/call.html', {})


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


def verify_code(request):
    """验证验证码"""
    phone = request.QUERY.get('phone')  # 接收人
    code = request.QUERY.get('code')  # 验证码
    code_id = int(request.QUERY.get('code_id'))  # 来源 1面试官注册验证码 2登录验证码
    is_ver = verify_(code, phone, code_id)
    if is_ver:
        return ajax.ajax_ok(message='验证成功')
    else:
        return ajax.ajax_fail(message='验证码错误')


def index(request):
    """发短信"""
    phone = request.QUERY.get('phone')  # 接收人
    send_phone = request.QUERY.get('send_phone', 888)  # 发送人
    code_id = int(request.QUERY.get('code_id'))  # 1面试官注册验证码 2登录验证码 3出题专家注册 4用户注册验证码 5找回密码
    content = request.QUERY.get('content')  # 发送内容
    code = 0
    redis_key = f"{phone}:{code_id}"
    if code_id in [2, 5]:
        # 登录验证码
        user_id, _ = get_user_id(phone, 4)
        if not user_id:
            return ajax.ajax_fail(message='账号不存在')
    if code_id in [4]:
        user_id, _ = get_user_id(phone, 4)
        if user_id:
            return ajax.ajax_fail(message='账号已存在')
    if code_id in [1, 3]:
        user_id, _ = get_user_id(phone, 4)
        if user_id:
            return ajax.ajax_fail(message='手机号已被注册请登录后再申请开通权限!')
    if code_id in [1, 2, 3, 4, 5]:
        # 面试官注册验证码
        rd.user_code.delete(redis_key)
        code = get_random_string(length=6, allowed_chars='0123456789')
        rd.user_code.set(redis_key, code, timeout=60 * 2)  # 设置缓存key 过期时间

        print(rd.user_code.get(redis_key))

    id_ = db.default.mobile_mt.create(send_phone=send_phone, phone=phone, content=code)
    body = {
        "action": "SendSms",
        "signName": "云数智学堂",
        "phoneNumber": phone,
        "templateCode": "SMS44785239911",
        "templateParam": "{\"code\":\"%s\"}" % code,
        "extendCode": str(id_)
    }
    res = requests.post(SMS_API, json=body)
    print(res)
    return ajax.ajax_ok()


