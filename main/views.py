import json
import time
from collections import defaultdict

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
        join recruit.sys_m_role_module ro on ro.module_id =m.id and m.status=1
        join recruit.users u on u.`type` =ro.role_id 
        and u.username ='{request.user.username}' order by m.mod_order ;
    """
    data = db.default.fetchall_dict(sql)
    parent_obj = [x for x in data if x['parent_id'] == 0]
    for obj in parent_obj:
        obj['child'] = [x for x in data if x['parent_id'] == obj['id']]
    return ajax.ajax_ok(parent_obj)


def sys_m_module(request):
    """模块管理"""
    module_list = db.default.sys_m_module.filter(status=1).order_by('mod_order')
    module_dict = defaultdict(list)

    parent_data = defaultdict(list)
    for obj in module_list:
        if obj.parent_id:
            obj['is_del'] = 1
            module_dict[obj.parent_id].append(obj)
        else:
            parent_data[obj.id] = [obj]
    data = []
    for parent_id, obj in parent_data.items():
        obj[0]['is_del'] = 0
        if not module_dict[parent_id]:
            obj[0]['is_del'] = 1
        obj = obj + module_dict[parent_id]
        data.extend(obj)
    return ajax.ajax_ok(data)


def sys_m_module_del(request):
    """删除菜单"""
    data = Struct()
    id_ = request.QUERY.get('id')
    status = request.QUERY.get('status')
    db.default.sys_m_module.filter(id=id_).update(status=status)
    return ajax.ajax_ok(data=data)


def sys_m_module_add(request):
    """添加菜单"""
    id_ = request.QUERY.get('id')
    parent_id = request.QUERY.get('parent_id')
    mod_name = request.QUERY.get('mod_name')
    mod_path = request.QUERY.get('mod_path')
    mod_order = request.QUERY.get('mod_order')
    icon = request.QUERY.get('icon')
    if parent_id:
        if not db.default.sys_m_module.filter(id=parent_id, parent_id=0):
            return ajax.ajax_fail(message='无效的父级id')
    if id_:
        db.default.sys_m_module.filter(id=id_).update(
            parent_id=parent_id, mod_name=mod_name, mod_path=mod_path, mod_order=mod_order, icon=icon, status=1)
    else:
        db.default.sys_m_module.create(parent_id=parent_id, mod_name=mod_name,
                                       mod_path=mod_path, mod_order=mod_order, icon=icon, status=1)
    return ajax.ajax_ok()


def sys_m_module_role(request):
    """角色权限"""
    id_ = request.QUERY.get('id')
    if request.method == 'GET':
        sql = f"""
                select distinct m.* from recruit.sys_m_module m
                join recruit.sys_m_role_module ro on ro.module_id =m.id and m.status=1 and ro.role_id={id_} and m.parent_id != 0
            """
        data = db.default.fetchall_dict(sql)
        return ajax.ajax_ok([x.id for x in data])
    else:
        role_moids = json.loads(request.QUERY.get('role_moids'))
        db.default.sys_m_role_module.filter(role_id=id_, status=1).update(status=-1)
        for module_id in role_moids:
            if db.default.sys_m_role_module.filter(role_id=id_, module_id=module_id):
                db.default.sys_m_role_module.filter(role_id=id_, module_id=module_id).update(status=1)
            else:
                db.default.sys_m_role_module.create(role_id=id_, module_id=module_id, status=1)
            mo = db.default.sys_m_module.get(id=module_id)
            if db.default.sys_m_role_module.filter(role_id=id_, module_id=mo.parent_id):
                db.default.sys_m_role_module.filter(role_id=id_, module_id=mo.parent_id).update(status=1)
            else:
                db.default.sys_m_role_module.create(role_id=id_, module_id=mo.parent_id, status=1)
    return ajax.ajax_ok()


def home_index(request):
    """获取首页数据"""
    sql = f"""
        select s.name, if(t1.num, t1.num, 0) as num from recruit.subjects s 
        left join (
            select q.sid, count(det.id) num from question q 
            join user_test_det_content det on det.question_id =q.id 
        group by q.sid 
        ) t1 on t1.sid=s.id
        where s.status =1
    """
    subject_list = db.default.fetchall_dict(sql)
    data = Struct()
    data.subject_list = subject_list
    return ajax.ajax_ok(data)


