
import time

import hashlib
from django.http import HttpResponse

from ChatApi.wx.utils import parse_xml
from dj2.settings import GHAT_ID
from libs.WeChat import config
from libs.WeChat.base import JsSign
from libs.WeChat.user import WebChatUser
from libs.utils import ajax, Struct, render_template, db, auth_token
from libs.utils.redis_com import rd


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
    if request.method == "GET":
        wechat_login = db.default.wechat_login.filter(status=2)
        now = int(time.time())
        if not wechat_login:
            id_ = db.default.wechat_login.create(status=0, add_date=now)
            scene_str = f"1:{id_}"
            res = WebChatUser(2).create_qr(scene_str)
            img_url = res.get('img_url')
            db.default.wechat_login.filter(id=id_).update(img_url=img_url)
            return ajax.ajax_ok(res.get('img_url'))
        else:
            id_ = wechat_login.first().id
            db.default.wechat_login.filter(id=id_).update(status=0)
            return ajax.ajax_ok(wechat_login.first().img_url)
    else:
        id_ = request.QUERY.get('id')
        type_ = request.QUERY.get('type')
        if type_ == 1:
            # 轮询是否扫码
            token = ''
            if db.default.wechat_login.filter(id=id_, status=1):
                db.default.wechat_login.filter(id=id_).update(status=2)
                phone = db.default.wechat_login.get(id=id_).phone
                if phone:
                    user_id = db.default.users.get(username=phone, status=1, type=4).id
                    token = auth_token.create_token('users', user_id)
                return ajax.ajax_ok({'token': token})
            else:
                return ajax.ajax_fail()
        else:
            # 绑定手机号
            phone = request.QUERY.get('phone')
            code = request.QUERY.get('code')
            now = int(time.time())
            if not verify_(code, phone, 9):
                return ajax.ajax_fail(message='验证码错误')
            open_id = db.default.wechat_login.get(id=id_).open_id
            if db.default.wechat_user.filter(app_id=2, open_id=open_id):
                db.default.wechat_user.filter(app_id=2, open_id=open_id).update(
                    phone=phone, status=1, add_date=now)
            else:
                db.default.wechat_user.create(
                    app_id=2, open_id=open_id, phone=phone, status=1, add_date=now)
            user = db.default.users.filter(username=phone, status__in=[0, 1], type=4)
            if user:
                user = user.first()
                if user.status == 0:
                    return ajax.ajax_fail(message='手机号已被禁用！')
                user_id = user.id
            else:
                user_id = db.default.users.create(username=phone, type=4, status=1, role='用户', password='')
            token = auth_token.create_token('users', user_id)
            return ajax.ajax_ok({'token': token})


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


def r_user_info(request):
    """
    根据code获取 用户信息
    :param request:
    :return:
    """
    args = request.QUERY.casts(code=str)
    data = Struct()
    code = args.code
    if not code:
        return ajax.jsonp_fail(request, message='not found code!')
    wx = WebChatUser(2)
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
        args = request.QUERY.casts(open_id=str, phone=str)
        open_id = args.open_id
        phone = args.phone

        return ajax.ajax_ok()
    return render_template(request, 'h5/index.html')


def r_js_ticket(request):
    """
    获取jssdk签名
    :param request:
    :return:
    """
    args = request.QUERY.casts(url=str)
    base = JsSign(args.url)
    result = base.sign()
    result["appId"] = config.WC_CONFIG[2]['app_id']
    print(result)
    return ajax.jsonp_ok(request, result)

