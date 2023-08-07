# coding:utf-8
import time

import requests

from dj2.common import get_user_id
from libs.utils.redis_com import rd

from dj2.settings import SMS_API
from libs.utils import ajax, db, render_template, send_email_server
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


def verify_email(code, email, code_id):
    """校验邮箱验证码"""
    if code == '425381':  # 万能验证码
        return True
    redis_key = f"{email}:{code_id}"
    rd_code = rd.user_code.get(redis_key)  # 缓存验证码
    if rd_code == code:
        rd.user_code.delete(redis_key)  # 验证成功删除缓存
        return True
    else:
        return False


def send_email(request):
    """发送email验证码"""
    email = request.QUERY.get('email')
    code_id = request.QUERY.get('code_id')
    redis_key = f"{email}:{code_id}"
    rd.user_code.delete(redis_key)
    code = get_random_string(length=6, allowed_chars='0123456789')
    rd.user_code.set(redis_key, code, timeout=60 * 2)  # 设置缓存key 过期时间
    print(rd.user_code.get(redis_key))
    now = int(time.time())
    db.default.mobile_mt.create(
        send_phone='163.email', phone=email, status=0, content=code, add_time=now, code_id=code_id)
    html = f"""
        <pre>
        您的验证码是{code}, 2分钟内有效。
        </pre>
    """
    is_send = send_email_server(email, "验证您的电子邮箱", html)
    if is_send:
        return ajax.ajax_ok()
    else:
        return ajax.ajax_fail()


def verify_code(request):
    """验证验证码"""
    phone = request.QUERY.get('phone')  # 接收人
    code = request.QUERY.get('code')  # 验证码
    code_id = int(request.QUERY.get('code_id'))  # 来源 1面试官注册验证码 2登录验证码
    if code_id == 8:
        # 换绑邮箱
        if verify_email(code, phone, code_id):
            old_phone = request.QUERY.get('old_phone')  # 接收人
            update_email(old_phone, phone)
            return ajax.ajax_ok(message='验证成功')
        else:
            return ajax.ajax_ok(message='验证失败')
    else:
        is_ver = verify_(code, phone, code_id)
        if is_ver:
            if code_id == 7:
                # 换绑手机号
                old_phone = request.QUERY.get('old_phone')  # 接收人
                update_phone(old_phone, phone)

            return ajax.ajax_ok(message='验证成功')
        else:
            return ajax.ajax_fail(message='验证码错误')


def update_phone(old_phone, phone):
    """换绑手机号"""
    db.default.users.filter(username=old_phone).update(username=phone)
    db.default.user_tea_det.filter(phone_number=old_phone).update(phone_number=phone)


def update_email(old_phone, email):
    """换绑邮箱"""
    db.default.user_tea_det.filter(phone_number=old_phone).update(email=email)


def index(request):
    """发短信"""
    phone = request.QUERY.get('phone')  # 接收人
    send_phone = request.QUERY.get('send_phone', 888)  # 发送人
    code_id = int(request.QUERY.get('code_id'))  # 1面试官注册验证码 2登录验证码 3出题专家注册 4用户注册验证码 5找回密码 6,7修改绑定手机号 8修改绑定邮箱 9微信绑定手机号
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
    if code_id in [7]:  # 修改绑定手机号
        user_id, _ = get_user_id(phone, 4)
        if user_id:
            return ajax.ajax_fail(message='手机号已被注册!')
    if code_id in [1, 2, 3, 4, 5, 6, 7, 9]:
        # 面试官注册验证码
        rd.user_code.delete(redis_key)
        code = get_random_string(length=6, allowed_chars='0123456789')
        rd.user_code.set(redis_key, code, timeout=60 * 2)  # 设置缓存key 过期时间

        print(rd.user_code.get(redis_key))
    now = int(time.time())
    id_ = db.default.mobile_mt.create(
        send_phone=send_phone, phone=phone, status=0, content=code, add_time=now, code_id=code_id)
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


