import json
import time


from dj2.common import get_user_id
from dj2.settings import UPLOAD_URL, web_file_url
from libs.utils.auth_token import get_random_string
from libs.utils.redis_com import rd
from main.models import yonghu, gongsi

from libs.utils import ajax, db, auth_token
from libs.utils.common import Struct, render_template, get_upload_key
from main.users_model import users
from tea.common import all_subjects
from util.auth import Auth

role_dict = {"管理员": 1, "出题专家": 2, "面试官": 3, "用户": 4, "公司": 5}
level = {1: "大专", 2: "本科", 3: "硕士", 4: "博士"}


def add_tea(request):
    """
    教师注册
    """
    data = Struct()
    if request.method == 'POST':
        args = {k: v for k, v in request.QUERY.items()}
        id_ = request.QUERY.get('id')
        phone_number = request.QUERY.get('phone_number')
        code = request.QUERY.get('code')
        password = request.QUERY.get('password1')
        ocr_front_img = request.QUERY.get('ocr_front_img')
        ocr_back_img = request.QUERY.get('ocr_back_img')
        number_id = request.QUERY.get('number_id')
        address = request.QUERY.get('address')
        expire = request.QUERY.get('expire')
        school = request.QUERY.get('school')
        school_level = request.QUERY.get('school_level')
        speciality = request.QUERY.get('speciality')
        ocr_front = json.loads(request.QUERY.get('ocr_front'))
        ocr_back = json.loads(request.QUERY.get('ocr_back'))
        user_id, _ = get_user_id(phone_number, 2, id_)
        if user_id:
            return ajax.ajax_fail(message='手机号已注册教师身份')
        if not verify_(code, phone_number, 3):
            return ajax.ajax_fail(message='验证码错误')
        now = int(time.time())
        expire = [x.strip() for x in expire.split('-')]
        start_time = ''.join(expire[:3])
        end_time = ''.join(expire[3:])
        tea_det = dict(nickname=phone_number,
                       phone_number=phone_number,
                       number_id=number_id,
                       school=school,
                       school_level=school_level,
                       step_id=0,
                       status=1, speciality=speciality, start_time=start_time, end_time=end_time)
        if not id_:
            db.default.yonghu.create(yonghuzhanghao=phone_number, mima=password,
                                     shouji=phone_number, yonghuxingming=phone_number)
            password = auth_token.sha1_encode_password(password)  # 加密密码
            db.default.users.create(username=phone_number, password=password, role='教师', type=2, status=0)
            yonghu_id = db.default.users.create(username=phone_number, password=password, role='用户', type=4, status=1)
            db.default.user_tea_det.create(user_id=yonghu_id, add_time=now, **tea_det)
            # 身份信息
            media_args = dict(
                address=address, add_time=now, front=ocr_front_img, back=ocr_back_img, ocr_info_front=json.dumps(ocr_front),
                ocr_info_back=json.dumps(ocr_back), status=1)
            db.default.user_media_det.create(user_id=yonghu_id, **media_args)
            # 学历信息
            education = level[int(school_level)]
            school_obj = dict(user_id=yonghu_id, school=school, education=education, speciality=speciality)
            if not db.default.user_school_list.filter(**school_obj):
                db.default.user_school_list.create(**school_obj, add_time=now, status=1)

        return ajax.ajax_ok(message='注册成功')
    else:
        if request.user and request.user.id:
            sql = f"""
                select  u.id , u.status from recruit.users u where u.type=2 and u.username='{request.user.shouji}'
            """
            us = db.default.fetchone_dict(sql)
            data.status = us.status if us else -2
        data.upload_url = f"{UPLOAD_URL}?upcheck={get_upload_key()}&up_type=number_id_img"
        data.web_file_url = web_file_url
        return render_template(request, 'tea/index.html', data)


def user_info(request):
    """用户信息"""
    id_ = request.user.id
    user = db.default.users.get(id=id_)
    info = db.default.user_tea_det.get(user_id=id_)
    data = {
        'username': user.username,
        'upload_url': f"{UPLOAD_URL}?upcheck={get_upload_key()}&up_type=number_id_img",
        "subjects": db.default.subjects.filter(status=1).select('id', 'name')[:]
    }
    data = Struct(data)
    data.update(info)
    data['id'] = id_
    user_id = id_
    # 步骤 1
    username = db.default.users.get(id=user_id).username
    if db.default.users.get(id=user_id).type == 3:
        user_id = db.default.users.get(username=username, type=4).id
    user_det = db.default.user_tea_det.get(user_id=user_id)
    user_media = db.default.user_media_det.get(user_id=user_id)
    data.step_id = user_det.step_id
    data.form = Struct()
    data.form.phone = user_det.phone_number
    if user_media:
        data.form.imageUrl1 = user_media.front
        data.form.imageUrl2 = user_media.back
        data.form.ocr_front = json.loads(user_media.ocr_info_front)
        data.form.ocr_back = json.loads(user_media.ocr_info_back)
    data.form.name = user_det.name
    data.form.number_id = user_det.number_id
    data.form.start_time = user_det.start_time
    data.form.end_time = user_det.end_time

    # 步骤 2
    data.school_list = []
    for obj in db.default.user_school_list.filter(user_id=user_id, status=1):
        data.school_list.append({
            "education": obj.education,
            "school": obj.school,
            "speciality": obj.speciality,
            "time": [obj.start_time, obj.end_time],
            "diploma": obj.diploma,
            "degree": obj.degree,
        })
    # 步骤 3
    data.work_list = []
    for obj in db.default.user_work_list.filter(user_id=user_id, status=1):
        data.work_list.append({
            "name": obj.name,
            "industry": obj.industry,
            "post": obj.post,
            "time": [obj.start_time, obj.end_time],
            "start_time": obj.start_time,
            "end_time": obj.end_time,
            "keyword": obj.keyword,
        })

    data.knowledge_list = []
    for obj in db.default.user_knowledge_list.filter(user_id=user_id, status=1):
        data.knowledge_list.append({
            "name": obj.name,
            "sid": str(obj.sid),
            "level": str(obj.level),
            "type": str(obj.type),
            "use_month": obj.use_month
        })

    data.prove = db.default.user_prove_list.filter(user_id=user_id, status=1).select(
        'other', 'security', 'work').first()
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
        print(phone)
        user_id, password = get_user_id(phone, type_)
        if not user_id and login_type == 2:
            password = get_random_string(length=6, allowed_chars='0123456789')
            password = auth_token.sha1_encode_password(password)
            user_id = db.default.users.create(username=phone, password=password, role='用户', type=4, status=1)
            now = int(time.time())
            db.default.user_tea_det.create(
                user_id=user_id, nickname=phone, add_time=now, phone_number=phone, status=1, step_id=0)
        if not user_id:
            return ajax.ajax_fail(message='账号不存在')
        if login_type == 1:
            if code != password:
                if not auth_token.verify_password(code, password):
                    return ajax.ajax_fail(message='密码错误')
        else:
            if not verify_(code, phone, 2):
                return ajax.ajax_fail(message='验证码错误')
        args = {'id': user_id, 'phone': phone}
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
    type_ = int(request.QUERY.get('type', 1))
    code_id = int(type_) + 3
    if request.method == 'POST':
        code = request.QUERY.get('code')
        phone = request.QUERY.get('username')
        password = request.QUERY.get('password1')
        if not verify_(code, phone, code_id):
            return ajax.ajax_fail(message='验证码错误')
        password = auth_token.sha1_encode_password(password)
        if type_ == 1:
            if db.default.users.filter(username=phone, role='用户', type=4, status=1):
                return ajax.ajax_fail(message='手机号已被注册！')
            id_ = db.default.users.create(username=phone, password=password, role='用户', type=4, status=1)
            now = int(time.time())
            db.default.user_tea_det.create(user_id=id_, nickname=phone, add_time=now,
                                           phone_number=phone, status=1, step_id=0)
            data.token = auth_token.create_token('users', id_)
            data.user_id = id_
            data.phone = phone
            return ajax.ajax_ok(data=data, message='注册成功')
        else:
            db.default.users.filter(username=phone).update(password=password)
            return ajax.ajax_ok(message='修改成功')
    else:

        title = {1: '用户注册', 2: "找回密码", 3: "修改密码"}[int(type_)]
        data.title = title
        data.code_id = code_id
        return render_template(request, 'user/yonghu.html', data)




