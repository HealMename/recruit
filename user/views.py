from libs.utils import ajax, db, auth_token, render_template
from main.models import yonghu
from util.auth import Auth


def login(request):
    """
    登录
    """
    if request.method == 'POST':
        args = {k: v for k, v in request.QUERY.items()}
        datas = yonghu.getbyparams(yonghu, yonghu, args)
        if not datas:
            return ajax.ajax_fail(message='账号或密码错误')
        args['id'] = datas[0].get('id')
        return Auth.authenticate(Auth, yonghu, args)
    else:
        return render_template(request, 'user/index.html')


def info(request):
    """获取用户信息"""
    return ajax.ajax_ok(Auth.identify(request, request))


def encode_password(request):
    """
    @api {get} /encode_password/ [公共接口]加密密码
    @apiGroup common
    @apiParamExample {json} 请求示例
    {
        "password": "123456"  密码
    }

    @apiSuccessExample {json} 成功返回
    {
        "response": "ok",
        "data": "sha1$4EPUN9mYQcWJ$fd217c695073f27e9a1ea21f7c8ba6d9576d1181",
        "error": "",
        "next": "",
        "message": ""
    }
    """
    password = request.QUERY.get('password')
    password = auth_token.sha1_encode_password(password)
    return ajax.ajax_ok(password)


def request_verify_password(request):
    """
    @api {get} /verify_password/ [公共接口]验证密码是否正确
    @apiGroup common
    @apiParamExample {json} 请求示例
    {
        "password": "123456",  # 登陆密码
        "encoded": "sha1$awnulEq41wMD$e9ac1787d66808c1c431268f7ed779ba1d8d05a4"    # 加密密码
    }
    @apiSuccessExample {json} 成功返回
    {
        "response": "ok",
        "data": 1,  1正确 0错误
        "error": "",
        "next": "",
        "message": ""
    }
    """
    password = request.QUERY.get('password')
    encoded = request.QUERY.get('encoded')
    verify = int(auth_token.verify_password(password, encoded))
    return ajax.ajax_ok(verify)

