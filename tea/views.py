import time

from django.shortcuts import render

from libs.utils import ajax, db, auth_token
from libs.utils.common import Struct, render_template, num_to_ch


def add_tea(request):
    """
    教师注册
    """
    data = Struct()
    if request.method == 'POST':
        args = {k: v for k, v in request.QUERY.items()}

        id_ = args.pop('id', 0)
        username = args.pop('username')
        password = args.pop('password1')
        args.pop('password2')
        if db.default.users.filter(username=username, type=3).exclude(id=id_):
            return ajax.ajax_fail(message='用户名已存在')
        now = int(time.time())
        if not id_:
            password = auth_token.sha1_encode_password(password)  # 加密密码
            id_ = db.default.users.create(username=username, password=password, role='教师', type=3)
            db.default.user_tea_det.create(user_id=id_, add_time=now, **args)
        return ajax.ajax_ok(message='注册成功')
    return render_template(request, 'tea/index.html', data)

