# coding:utf-8
import json

import requests
from libs.utils.redis_com import rd

from dj2.settings import SMS_API
from libs.utils import ajax, db
from libs.utils.auth_token import get_random_string


def verify_code(request):
    """验证验证码"""
    phone = request.QUERY.get('phone')  # 接收人
    code = request.QUERY.get('code')  # 验证码
    code_id = int(request.QUERY.get('code_id'))  # 来源 1验证码
    redis_key = f"{phone}:{code_id}"
    rd_code = rd.user_code.get(redis_key)  # 缓存验证码
    if rd_code == code:
        rd.user_code.delete(redis_key)  # 验证成功删除缓存
        return ajax.ajax_ok(message='验证成功')
    else:
        return ajax.ajax_fail(message='验证码错误')


def index(request):
    """发短信"""
    phone = request.QUERY.get('phone')  # 接收人
    send_phone = request.QUERY.get('send_phone', 888)  # 发送人
    code_id = int(request.QUERY.get('code_id'))  # 来源 1验证码
    content = request.QUERY.get('content')  # 发送内容
    code = 0
    redis_key = f"{phone}:{code_id}"
    if code_id == 1:
        # 面试官注册验证码
        rd.user_code.delete(redis_key)
        code = get_random_string(length=6, allowed_chars='0123456789')
        rd.user_code.set(redis_key, code, timeout=60 * 2)  # 设置缓存key 过期时间

        print(rd.user_code.get(redis_key))

    id_ = db.default.mobile_mt.create(send_phone=send_phone, phone=phone, content=code)
    body = {
        "action": "SendSms",
        "signName": "天翼云测试",
        "phoneNumber": phone,
        "templateCode": "SMS64124870510",
        "templateParam": "{\"code\":\"%s\"}" % code,
        "extendCode": str(id_)
    }
    requests.post(SMS_API, json=body)
    return ajax.ajax_ok()
