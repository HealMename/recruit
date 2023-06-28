import time


from dj2.common import get_user_id
from libs.utils.auth_token import get_random_string
from libs.utils.redis_com import rd
from main.models import yonghu, gongsi

from libs.utils import ajax, db, auth_token
from libs.utils.common import Struct, render_template
from main.users_model import users
from util.auth import Auth

role_dict = {"管理员": 1, "出题专家": 2, "面试官": 3, "用户": 4, "公司": 5}


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
        user_id, _ = get_user_id(phone_number, 2, id_)
        if user_id:
            return ajax.ajax_fail(message='手机号已注册教师身份')
        if not verify_(code, phone_number, 3):
            return ajax.ajax_fail(message='验证码错误')
        now = int(time.time())
        if not id_:
            password = get_random_string(length=6, allowed_chars='0123456789')
            password = auth_token.sha1_encode_password(password)  # 加密密码
            id_ = db.default.users.create(username=phone_number, password=password, role='教师', type=2, status=0)
            db.default.user_tea_det.create(user_id=id_, nickname=username, add_time=now, **args)
        else:
            args['add_time'] = now
            db.default.users.filter(id=id_).update(username=phone_number)
            db.default.user_tea_det.filter(user_id=id_).update(**args)
        return ajax.ajax_ok(message='注册成功')
    else:
        user_id = request.QUERY.get('user_id')
        if user_id:
            sql = f"""
                select  d.* , u.status from recruit.users u 
                join recruit.user_tea_det d on d.user_id =u.id and u.`type` =2
                where u.id= {user_id}
            """
            data.user = db.default.fetchone_dict(sql)
            return ajax.ajax_ok(data)
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
        login_type = int(args.pop("login_type", 2))  # 1 密码登陆 2验证码登陆
        args['type'] = role_dict[role]
        phone = args['username']
        code = args['password']
        # type_ = args['type']
        type_ = 4
        user_id, password = get_user_id(phone, type_)
        if not user_id:
            return ajax.ajax_fail(message='账号不存在')
        if login_type == 1:
            if code != password:
                if not auth_token.verify_password(code, password):
                    return ajax.ajax_fail(message='密码错误')
        else:
            if not verify_(code, phone, 2):
                return ajax.ajax_fail(message='验证码错误')
        args = {'id': user_id}
        args['id'] = user_id
        if type_ in [1, 2, 3, 4]:
            args['status'] = 1
            return Auth.authenticate(Auth, users, args)
        else:
            return Auth.authenticate(Auth, gongsi, args)


def register_role(request):
    """角色选择"""
    data = Struct()
    return render_template(request, 'user/register_role.html', data)


def register_yonghu(request):
    """角色选择普通用户注册"""
    data = Struct()
    if request.method == 'POST':
        username = request.QUERY.get('username')
        code = request.QUERY.get('code')
        phone = request.QUERY.get('phone_number')
        password = request.QUERY.get('password1')
        if not verify_(code, phone, 4):
            return ajax.ajax_fail(message='验证码错误')
        if db.default.yonghu.filter(yonghuzhanghao=phone):
            return ajax.ajax_ok(message='手机号已被注册')
        db.default.yonghu.create(yonghuzhanghao=phone, mima=password,
                                 shouji=phone, yonghuxingming=username)
        password = auth_token.sha1_encode_password(password)
        id_ = db.default.users.create(username=phone, password=password, role='用户', type=4, status=1)
        now = int(time.time())
        db.default.user_tea_det.create(user_id=id_, nickname=username, add_time=now,
                                       phone_number=phone, status=1, step_id=0)
        return ajax.ajax_ok(message='注册成功')
    else:
        return render_template(request, 'user/yonghu.html', data)

