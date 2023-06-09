import json
import time

import random

from django.http import HttpResponseRedirect

from dj2.settings import K8S_URL
from libs.utils import ajax, db, auth_token
from libs.utils.common import Struct, trancate_date
from tea.common import all_subjects

level_name = {'1': "初级", "2": "中级", "3": "高级"}
size_name = {'1': '单机', "2": "集群", "3": "多集群"}

ROLE = {"用户": 1, "教师": 2, "面试官": 3, "企业": 4}


def user_test_list(request):
    """获取做题记录"""
    id_ = request.QUERY.get('id')
    phone = request.QUERY.get('phone', 0)
    page_id = request.QUERY.get('page_id', 1)
    page_size = request.QUERY.get('page_size', 5)
    where_sql = ""
    if id_ and id_.isdigit():
        if id_.isdigit():
            where_sql += f" and det.id = {id_}"

    # 教师
    if phone:
        where_sql += f" and tea.phone_number = '{phone}'"
    sql = f"""
            select distinct det.id ,tea.name name, tea.phone_number phone, det.add_time 
            from recruit.user_test_det det
            join recruit.users au on au.id =det.add_user and det.status!=-1
            join user_tea_det tea on tea.user_id =det.add_user
            join user_test_det_content c on c.det_id=det.id
            {where_sql}
            order by -det.id
            limit {(page_id - 1) * page_size}, {page_size} ;
        """

    page_data = db.default.fetchall_dict(sql)
    for obj in page_data:
        obj['add_time'] = trancate_date(obj.add_time)
    data = Struct()
    data.page_data = page_data
    data.sum_len = data.sum_len = get_page_len(where_sql)
    return ajax.ajax_ok(data)


def get_page_len(where_sql):
    """获取总页数"""
    sql = f"""
    select count(distinct det.id) num
            from recruit.user_test_det det
            join recruit.users au on au.id =det.add_user and det.status!=-1
            join user_tea_det tea on tea.user_id =det.add_user
            join user_test_det_content c on c.det_id=det.id
            {where_sql}
            order by -det.id
    """
    num = db.default.fetchone_dict(sql)
    return num.num if num else 0


def user_test_del(request):
    """
    删除
    status:1正常 -1删除
    """
    id_ = request.QUERY.get('id')
    status = request.QUERY.get('status')
    db.default.user_test_det.filter(id=id_).update(status=status)
    return ajax.ajax_ok()


def get_user_test_det(request):
    """获取做题详情"""
    id_ = request.QUERY.get('id')
    sql = f"""
        select q.id, q.title, q.version, q.`level`, q.`size`,det.content,det.add_time, q.sid  from recruit.user_test_det t
        join recruit.user_test_det_content det on det.det_id =t.id and t.id={id_}
        join recruit.question q on q.id =det.question_id 
    """
    data = db.default.fetchall_dict(sql)
    sid_name = all_subjects()
    for q in data:
        q['add_time'] = trancate_date(q['add_time'])
        q['sid'] = sid_name[q['sid']]
        q['level'] = level_name[str(q['level'])]
        q['size'] = size_name[str(q['size'])]
        q.content = json.loads(q.content)
        for x in q.content:
            if x['type'] == 1:
                x['msg'] += '\r\n'
    return ajax.ajax_ok(data[:])




