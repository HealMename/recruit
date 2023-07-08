import json
import logging
import os
import time

import requests
from rest_framework.views import APIView
import hashlib
from django.http import HttpResponse

from ChatApi.wx.utils import parse_xml, detail_img_one_school
from dj2.settings import GHAT_ID
from libs.WeChat import config
from libs.WeChat.user import WebChatUser
from libs.utils import ajax, db, auth_token, Struct, get_key


def r_index(request):
    """
    微信请求入口
    :param request:
    :return:
    """
    # path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    # wx = WebChatUser(GHAT_ID)
    # wx.upload_media(path + "/site_media/img/auth.png", 1)
    if request.method == "GET":
        args = request.QUERY.casts(signature=str, timestamp=str, nonce=str, echostr=str, openid=str)
        signature = args.signature
        timestamp = args.timestamp
        nonce = args.nonce
        echo_str = args.echostr

        lst = [config.token, timestamp, nonce]
        lst.sort()
        str_list = ''.join(lst)
        sha1 = hashlib.sha1()
        sha1.update(str_list.encode('utf-8'))
        hashcode = sha1.hexdigest()
        if hashcode == signature:
            return HttpResponse(echo_str)
        return HttpResponse("")

    if request.method == "POST":
        msg_xml = request.body
        xml = parse_xml(msg_xml)
        return HttpResponse(xml)


def r_oauth(request):
    args = request.QUERY.casts(type=str, url=str)
    typ = args.type
    url = args.url or 'https://wechat.m.tbkt.cn/#/'
    state = typ if typ else 1
    if str(state).isdigit():
        scope = 'snsapi_userinfo'
    else:
        scope = 'snsapi_base'
    return WebChatUser(GHAT_ID).get_oauth_url(url, scope=scope, state=state)


def create_login_img(request):
    """生成登陆二维码"""
    res = WebChatUser(GHAT_ID).login_img()
    print(res)
    return ajax.ajax_ok()


def r_user_info(request):
    """
    根据code获取 用户信息
    :param request:
    :return:
    """
    args = request.QUERY.casts(code=str)
    user_id = request.user_id
    now = int(time.time())
    if not request.user_id:
        code = args.code
        if not code:
            return ajax.jsonp_fail(request, message='not found code!')
        wx = WebChatUser(GHAT_ID)
        user = wx.user(code)
        open_id = user.get('openid', '')
        if not open_id:
            return ajax.ajax_fail(message='not found open_id')
        res = wx.get_unionid(open_id)
        unionid = res.get('unionid', '-1')
        user = db.wechat_lzfd.auth_user.filter(open_id=open_id, type=2)
        if not user:
            user_id = db.wechat_lzfd.auth_user.create(
                name='微信用户', open_id=open_id, type=2, unionid=unionid, add_time=now)
        else:
            user_id = user.first().id
    db.wechat_lzfd.auth_user.filter(id=user_id).update(last_login=now)
    token = auth_token.create_token(user_id)
    data = Struct()
    data.key = give(user_id)
    data.token = token
    return ajax.ajax_ok(data)


def give(user_id):
    """赠送3天十次"""
    now = int(time.time())
    user_open = db.wechat_lzfd.chatapi_open_detail.filter(user_id=user_id)
    if user_open:
        user_open = user_open.first()
        # if now > user_open.cancel_date:
        #     """已过期"""
        #     cancel_date = now + 86400 * 3
        # else:
        #     cancel_date = user_open.cancel_date + 86400 * 3
        #
        # if user_open.speak_num == 0:
        #     speak_num = 10
        # else:
        #     speak_num = user_open.speak_num + 10
        # db.wechat_lzfd.chatapi_open_detail.filter(user_id=user_id).update(cancel_date=cancel_date, speak_num=speak_num)
        key = user_open.key
    else:
        key = get_key()
        db.wechat_lzfd.chatapi_open_detail.create(
            user_id=user_id, cancel_date=now + 86400 * 3, speak_num=10, add_date=now, key=key)
    return key



