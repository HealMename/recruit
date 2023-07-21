import time

from django.http import JsonResponse
from django.shortcuts import render
import util.message as mes
from main.models import yonghu, gongsi
from util.codes import *

from libs.utils import ajax, db, auth_token
from libs.utils.common import Struct, render_template, num_to_ch
from main.users_model import users
from util.auth import Auth

role_dict = {"管理员": 1, "出题专家": 2, "面试官": 3, "用户": 4, "公司": 5}


def checkout_user_type(request):
    """
    切换用户身份
    """
    type_ = int(request.QUERY.get('type'))  # 用户要切换的身份 1普通用户 2教师 3面试官 4企业用户
    user = request.user
    phone = user.shouji
    if type_ == 1:
        # 普通用户
        yonghu = db.default.yonghu.filter(shouji=phone).first()
        if yonghu:
            return yonghu_login({'shouji': phone})
        else:
            return ajax.ajax_fail(message='您还没有注册')
    elif type_ in (2, 3):
        # 教师
        sql = f"""
                select u.id, status from recruit.users u where u.`type` ={type_} and username ='{phone}'
        """
        print(sql)
        tea = db.default.fetchone_dict(sql)
        if tea and tea.status == 1:
            return tea_login({'id': tea.id})
        elif tea and tea.status == 0:
            return ajax.ajax_fail(message='该身份正在审核中!')
        elif tea and tea.status == -1:
            return ajax.ajax_fail(message='该身份审核被拒绝请重新提交审核！')
        else:
            return ajax.ajax_fail(message='您还没有注册该身份，请前往注册')
    elif type_ == 4:
        # 企业
        yonghu = db.default.gongsi.filter(shouji=phone).first()
        if yonghu:
            return gongsi_login({'shouji': phone})
        else:
            return ajax.ajax_fail(message='您还没有注册该身份，请前往注册')
    return ajax.ajax_ok()


def yonghu_login(req_dict):
    "用户登录"
    msg = {'code': normal_code, "msg": mes.normal_code}
    datas = yonghu.getbyparams(yonghu, yonghu, req_dict)
    if not datas:
        msg['code'] = password_error_code
        msg['msg'] = mes.password_error_code
        return JsonResponse(msg)
    req_dict['id'] = datas[0].get('id')
    return Auth.authenticate(Auth, yonghu, req_dict)


def tea_login(args):
    "教师登录"
    datas = users.getbyparams(users, users, args)
    if not datas:
        return ajax.ajax_fail(message='您还没有出题专家身份，请前往注册！')
    args['id'] = datas[0].get('id')
    return Auth.authenticate(Auth, users, args)


def gongsi_login(req_dict):
    """企业登录"""
    msg = {'code': normal_code, "msg": mes.normal_code}
    datas = gongsi.getbyparams(gongsi, gongsi, req_dict)
    if not datas:
        msg['code'] = password_error_code
        msg['msg'] = mes.password_error_code
        return JsonResponse(msg)

    req_dict['id'] = datas[0].get('id')
    return Auth.authenticate(Auth, gongsi, req_dict)


def menu_list(request):
    """获取权限列表"""
    sql = f"""
        select distinct m.* from recruit.sys_m_module m
        join recruit.sys_m_role_module ro on ro.module_id =m.id
        join recruit.users u on u.`type` =ro.role_id and u.username ='{request.user.shouji}' order by m.mod_order ;
    """
    data = db.default.fetchall_dict(sql)
    parent_obj = [x for x in data if x['parent_id'] == 0]
    for obj in parent_obj:
        obj['child'] = [x for x in data if x['parent_id'] == obj['id']]
    return ajax.ajax_ok(parent_obj)

