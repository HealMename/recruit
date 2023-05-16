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



