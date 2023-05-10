import json
import time

import random

from django.http import HttpResponseRedirect

from dj2.settings import K8S_URL
from libs.utils import ajax, db, auth_token
from libs.utils.common import Struct, trancate_date

level_name = {'1': "初级", "2": "中级", "3": "高级"}
sid_name = {'1': "K8s", "2": "Mysql", "3": "Vue"}
size_name = {'1': '单机', "2": "集群", "3": "多集群"}

ROLE = {"用户": 1, "教师": 2, "面试官": 3, "企业": 4}


def user_test_list(request):
    """获取做题记录"""
    id_ = request.QUERY.get('id')
    phone = request.QUERY.get('phone', 0)
    role = request.QUERY.get('role', 2)
    page_id = request.QUERY.get('page_id', 1)
    page_size = request.QUERY.get('page_size', 5)
    where_sql = ""
    if id_ and id_.isdigit():
        if id_.isdigit():
            where_sql += f" and det.id = {id_}"

    if role == 2:
        # 教师
        if phone:
            where_sql += f" and tea.phone_number = '{phone}'"
        sql = f"""
                select det.id ,au.username name, tea.phone_number phone, det.add_time  from django7681v.user_test_det det
                join django7681v.users au on au.id =det.add_user  and det.`role` =2
                join user_tea_det tea on tea.user_id =det.add_user 
                {where_sql}
                order by -det.id
                limit {(page_id - 1) * page_size}, {page_size} ;
            """
    else:
        if phone:
            where_sql += f" and au.shouji = '{phone}'"
        # 用户
        sql = f"""
            select det.id ,au.shouji phone, au.yonghuxingming name, det.add_time  
            from django7681v.user_test_det det
            join django7681v.yonghu au on au.id =det.add_user  and det.`role` =1 {where_sql}
        """
    page_data = db.default.fetchall_dict(sql)
    for obj in page_data:
        obj['add_time'] = trancate_date(obj.add_time)
    data = Struct()
    data.page_data = page_data
    data.sum_len = data.sum_len = get_page_len('paper', where_sql)
    return ajax.ajax_ok(data)


def get_page_len(table, where_sql):
    """获取总页数"""
    sql = f"""
    select count(1) as num from {table} 
        where status in (0, 1) 
        {where_sql} 
    """
    num = db.default.fetchone_dict(sql)
    return num.num if num else 0