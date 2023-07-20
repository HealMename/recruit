
import time

import hashlib
from django.http import HttpResponse

from ChatApi.wx.utils import parse_xml
from dj2.settings import GHAT_ID
from libs.WeChat import config
from libs.WeChat.user import WebChatUser
from libs.utils import ajax, Struct, render_template


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
    data = Struct()
    if not request.user_id:
        code = args.code
        if not code:
            return ajax.jsonp_fail(request, message='not found code!')
        wx = WebChatUser(GHAT_ID)
        user = wx.user(code)
        open_id = user.get('openid', '')
        data.open_id = open_id
        if not open_id:
            return ajax.ajax_fail(message='not found open_id')
    return ajax.ajax_ok(data)


def login(request):
    """登陆"""
    data = Struct()
    if request.method == "GET":
        code = request.GET.get('code')
        data.code = code
    else:
        return ajax.ajax_ok()
    return render_template(request, 'h5/index.html')
