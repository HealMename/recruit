import json
import time

from aip import AipOcr
from dj2.settings import UPLOAD_URL, web_file_url, BD_APP_ID, BD_API_KEY, BD_SECRET_KEY

from libs.utils import ajax, db, auth_token
from libs.utils.common import Struct, render_template, get_upload_key
from main.users_model import users
from util.auth import Auth


def save_info(request):
    """保存信息"""
    step_id = int(request.QUERY.get('step_id'))
    now = int(time.time())
    data = Struct()
    if step_id == 1:
        # 保存个人信息
        id_ = request.user.id or 0
        name = request.QUERY.get('name')
        phone = request.QUERY.get('phone')
        code = request.QUERY.get('code')  # 验证码
        front = request.QUERY.get('front')
        back = request.QUERY.get('back')
        info_front = Struct(json.loads(request.QUERY.get('info_front')))
        info_back = Struct(json.loads(request.QUERY.get('info_back')))
        ocr_info_front = Struct(json.loads(request.QUERY.get('ocr_info_front')))
        ocr_info_back = Struct(json.loads(request.QUERY.get('ocr_info_back')))
        if db.default.users.filter(username=phone, type=3, status=1, id__ne=id_):
            return ajax.ajax_fail(message='手机号已被注册')
        user_id = db.default.users.create(username=phone, type=3, status=1, role='面试官') if not id_ else id_
        data.token = auth_token.create_token('users', user_id)
        media_args = dict(
            add_time=now, front=front, back=back, ocr_info_front=json.dumps(ocr_info_front),
            ocr_info_back=json.dumps(ocr_info_back), status=1)

        if not id_:
            db.default.user_media_det.create(user_id=user_id, **media_args)

        else:
            db.default.user_media_det.filter(user_id=user_id).update(**media_args)
        ocr_info_front = {x: y for x, y in ocr_info_front.items() if x in info_front}
        ocr_info_back = {x: y for x, y in ocr_info_back.items() if x in info_back}
        is_update = 0
        if info_front != ocr_info_front or info_back != ocr_info_back:
            # 判断用户是否修改过识别的内容
            is_update = 1
        det_args = dict(phone_number=phone, name=info_front.name, step_id=1, status=1, add_time=now,
                        nickname=name, number_id=info_front.number_id, is_update=is_update)
        if not id_:
            db.default.user_tea_det.create(user_id=user_id, **det_args)
        else:
            db.default.user_tea_det.filter(user_id=user_id).update(**det_args)
    return ajax.ajax_ok(data)


def add_tea(request):
    """
    面试官注册页面
    """
    data = Struct()
    data.upload_url = f"{UPLOAD_URL}?upcheck={get_upload_key()}&up_type=number_id_img"
    data.web_file_url = web_file_url
    data.step_id = 0
    if request.user.id:
        data.step_id = db.default.user_tea_det.get(user_id=request.user.id).step_id - 1
    return render_template(request, 'interviewer/index.html', data)


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


def login(request):
    """
    教师登录
    """
    if request.method == 'POST':
        args = {k: v for k, v in request.QUERY.items()}
        args['type'] = 3
        password = args.pop('password')
        datas = users.getbyparams(users, users, args)
        if not datas:
            return ajax.ajax_fail(message='账号不存在请联系管理员！')
        if not auth_token.verify_password(password, datas[0]['password']):
            return ajax.ajax_fail(message='密码不正确请重试！')
        args['id'] = datas[0].get('id')
        return Auth.authenticate(Auth, users, args)


def ocr_sfz(request):
    """识别身份证"""
    idCardSide = request.QUERY.get('idCardSide', 'front')
    url = request.QUERY.get('url')
    client = AipOcr(BD_APP_ID, BD_API_KEY, BD_SECRET_KEY)
    """ 读取图片 """
    # idCardSide = 'front'  # 身份证正面
    # idCardSide = 'back'   #身份证反面
    data = Struct()
    # 如果有可选参数
    options = {}
    options["detect_risk"] = "true"
    res_url = client.idcardUrl(url, idCardSide, options)
    if idCardSide == 'front':
        data.name = res_url['words_result']['姓名']['words']
        data.nation = res_url['words_result']['民族']['words']
        data.address = res_url['words_result']['住址']['words']
        data.number_id = res_url['words_result']['公民身份号码']['words']
        data.birthday = res_url['words_result']['出生']['words']
        data.sex = res_url['words_result']['性别']['words']
    else:
        data.end_time = res_url['words_result']['失效日期']['words']
        data.start_time = res_url['words_result']['签发日期']['words']
        data.organ = res_url['words_result']['签发机关']['words']
    return ajax.ajax_ok(data)
