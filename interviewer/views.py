import datetime
import json
import time

from aip import AipOcr

from dj2.send_msg import verify_
from dj2.settings import UPLOAD_URL, web_file_url, BD_APP_ID, BD_API_KEY, BD_SECRET_KEY
from libs.utils import ajax, db, auth_token
from libs.utils.auth_token import get_random_string
from libs.utils.common import Struct, render_template, get_upload_key

role_name = {2: "出题专家", 3: "面试专家"}

def save_info(request):
    """保存信息"""
    step_id = int(request.QUERY.get('step_id', 0))

    role_id = request.QUERY.get('role_id')
    role_type = 0
    if role_id == '2,3':
        role_id = 2
        role_type = 3

    now = int(time.time())
    data = Struct()
    user_id = request.user.id or 0
    if request.method == 'POST':
        # 保存个人信息
        if step_id == 1:
            password = request.QUERY.get('password1')
            phone = request.QUERY.get('phone')
            code = request.QUERY.get('code')  # 验证码
            is_ver = verify_(code, phone, 1)
            if not is_ver and not user_id:
                return ajax.ajax_fail(message='验证码错误')
            front = request.QUERY.get('front')
            back = request.QUERY.get('back')
            info_front = Struct(json.loads(request.QUERY.get('info_front')))
            info_back = Struct(json.loads(request.QUERY.get('info_back')))
            ocr_info_front = Struct(json.loads(request.QUERY.get('ocr_info_front')))
            ocr_info_back = Struct(json.loads(request.QUERY.get('ocr_info_back')))
            if db.default.users.filter(username=phone, type=4, id__ne=user_id, status=1):
                return ajax.ajax_fail(message='手机号已被注册请登录后再申请开通权限!')
            password = auth_token.sha1_encode_password(password)  # 加密密码
            if not user_id:
                db.default.users.create(username=phone, type=role_id, status=0, role=role_name[int(role_id)], password=password)
                user_id = db.default.users.create(username=phone, type=4, status=1, role='用户', password=password)
            if not db.default.users.filter(username=phone, type=role_id):
                db.default.users.create(username=phone, type=role_id, status=0, role=role_name[int(role_id)], password='')
            if role_type:
                # 双角色同时注册
                if not user_id:
                    db.default.users.create(username=phone, type=role_type, status=0, role=role_name[role_type],
                                            password=password)
                    user_id = db.default.users.create(username=phone, type=4, status=1, role='用户', password=password)
                if not db.default.users.filter(username=phone, type=role_type):
                    db.default.users.create(username=phone, type=role_type, status=0, role=role_name[role_type],
                                            password='')
            data.token = auth_token.create_token('users', user_id)
            data.user_id = user_id
            media_args = dict(
                add_time=now, front=front, back=back, ocr_info_front=json.dumps(ocr_info_front),
                ocr_info_back=json.dumps(ocr_info_back), status=1)

            if not db.default.user_media_det.filter(user_id=user_id):
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
                            nickname=phone, number_id=info_front.number_id, is_update=is_update,
                            start_time=info_back.start_time, end_time=info_back.end_time)
            if not db.default.user_tea_det.filter(user_id=user_id):
                db.default.user_tea_det.create(user_id=user_id, **det_args)
            else:
                db.default.user_tea_det.filter(user_id=user_id).update(**det_args)
        elif step_id == 2:
            # 步骤2
            data = json.loads(request.QUERY.get('data'))
            if not user_id:
                return ajax.ajax_fail(message='请登陆后重试!')
            db.default.user_school_list.filter(user_id=user_id).update(status=-1)
            objs = []
            for obj in data:
                obj.pop('time')
                obj['user_id'] = user_id
                obj['add_time'] = now
                objs.append(obj)
            db.default.user_school_list.bulk_create(objs)
            db.default.user_tea_det.filter(user_id=user_id).update(step_id=step_id)
        elif step_id == 3:
            # 步骤 3
            data = json.loads(request.QUERY.get('data'))
            if not user_id:
                return ajax.ajax_fail(message='请登陆后重试!')
            db.default.user_work_list.filter(user_id=user_id).update(status=-1)
            objs = []
            for obj in data:
                obj.pop('time')
                obj.pop('keyword_new', '')
                obj['user_id'] = user_id
                obj['add_time'] = now

                objs.append(obj)
            db.default.user_work_list.bulk_create(objs)
            db.default.user_tea_det.filter(user_id=user_id).update(step_id=step_id)
        elif step_id == 4:
            # 步骤 4
            prove = json.loads(request.QUERY.get('prove'))
            if not user_id:
                return ajax.ajax_fail(message='请登陆后重试!')

            db.default.user_prove_list.filter(user_id=user_id).update(status=-1)
            db.default.user_prove_list.create(user_id=user_id, add_time=now, **prove)
            db.default.user_tea_det.filter(user_id=user_id).update(step_id=step_id)
        elif step_id == 5:
            # 步骤 5
            data = json.loads(request.QUERY.get('data'))
            if not user_id:
                return ajax.ajax_fail(message='请登陆后重试!')
            db.default.user_knowledge_list.filter(user_id=user_id, status=1).update(status=-1)
            objs = []
            sub = {x.name: x.id for x in db.default.subjects.filter(status=1).select('id', 'name')}
            for obj in data:
                obj['sid'] = sub.get(obj['name'], 0)
                obj['user_id'] = user_id
                obj['add_time'] = now
                objs.append(obj)
            db.default.user_knowledge_list.bulk_create(objs)
            db.default.user_tea_det.filter(user_id=user_id).update(step_id=step_id)
        elif step_id == 6:
            # 步骤 5 确定审核
            db.default.user_tea_det.filter(user_id=user_id).update(step_id=step_id)

        username = db.default.users.get(id=user_id).username
        db.default.users.filter(username=username, type__in=[2, 3]).update(status=0, addtime=datetime.datetime.now())
        return ajax.ajax_ok(data)
    else:
        """获取提交步骤内容"""
        user_id = request.GET.get('cms_user_id', 0) or request.user.id
        is_cms = 0
        if request.GET.get('cms_user_id', 0):
            is_cms = 1  # 后台过来的

        if user_id:
            # 步骤 1
            username = db.default.users.get(id=user_id).username
            user_id = db.default.users.get(username=username, type=4).id
            if db.default.users.get(username=username, type=role_id):
                data.status = db.default.users.get(username=username, type=role_id).status
            else:
                data.status = 0

            user_det = db.default.user_tea_det.get(user_id=user_id)
            user_media = db.default.user_media_det.get(user_id=user_id)
            data.form = Struct()
            data.form.phone = user_det.phone_number
            data.step_id = 0
            if user_media:
                data.form.imageUrl1 = user_media.front
                data.form.imageUrl2 = user_media.back
                data.form.ocr_front = json.loads(user_media.ocr_info_front or '{}')
                data.form.ocr_back = json.loads(user_media.ocr_info_back or '{}')
                data.step_id = 1
                if not db.default.users.get(username=username, type=role_id) and not is_cms:
                    db.default.users.create(username=username, type=role_id, status=0, role=role_name[int(role_id)], password='')
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
                        "stu_card": obj.stu_card,
                })
                data.step_id = 2
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
                data.step_id = 3
            # 步骤 4
            data.prove = db.default.user_prove_list.filter(user_id=user_id, status=1).select(
                'other', 'security', 'work').first()
            if data.prove:
                data.step_id = 4
            # 步骤 5
            data.knowledge_list = []
            for obj in db.default.user_knowledge_list.filter(user_id=user_id, status=1):
                data.knowledge_list.append({
                    "name": obj.name,
                    "sid": str(obj.sid),
                    "level": str(obj.level),
                    "type": str(obj.type),
                    "use_month": obj.use_month
                })
                data.step_id = 5

            if data.step_id == 6 and data.status == 0:
                data.step_id = 6
        return ajax.ajax_ok(data)


def add_tea(request):
    """
    面试官注册页面
    """
    data = Struct()
    role_id = request.GET.get('role_id')
    data.role_id = role_id
    data.upload_url = f"{UPLOAD_URL}?upcheck={get_upload_key()}&up_type=number_id_img"
    data.web_file_url = web_file_url
    data.subjects = db.default.subjects.filter(status=1).select('id', 'name')[:]
    return render_template(request, 'interviewer/index.html', data)


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
    try:
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
    except Exception as e:
        print('识别失败请重试')
        return ajax.ajax_fail(message='识别失败请重新上传')
