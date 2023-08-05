import json
import time

import random
from collections import defaultdict

from django.http import HttpResponseRedirect

from dj2.settings import K8S_URL
from libs.utils import ajax, db, auth_token
from libs.utils.common import Struct, trancate_date, get_today_zero_timestamp
from tea.common import all_subjects

level_name = {'1': "初级", "2": "中级", "3": "高级"}
size_name = {'1': '单机', "2": "集群", "3": "多集群"}

ROLE = {"用户": 1, "教师": 2, "面试官": 3, "企业": 4}


def user_test_list(request):
    """获取做题记录"""
    id_ = request.QUERY.get('id')
    phone = request.QUERY.get('phone', 0)
    start_time = request.QUERY.get('start_time', 0)
    end_time = request.QUERY.get('end_time', 0)
    page_id = request.QUERY.get('page_id', 1)
    page_size = request.QUERY.get('page_size', 5)
    user_id = request.user.id
    open_role = request.user.open_role
    where_sql = ""
    if id_ and id_.isdigit():
        if id_.isdigit():
            where_sql += f" and det.id = {id_}"
    if '1' not in open_role:
        where_sql += f" and det.add_user = {user_id}"
    if phone:
        user_id = db.default.users.get(username=phone, type=4) or {'id': -1}
        where_sql += f" and det.add_user = {user_id['id']}"
    if start_time:
        where_sql += f" and det.add_time >= {get_today_zero_timestamp(start_time)}"
    if end_time:
        where_sql += f" and det.add_time <= {get_today_zero_timestamp(end_time) + (60 * 60 * 24)}"
    sql = f"""
            select det.id, det.add_user, det.add_time, det.`role`, det.city 
            from recruit.user_test_det det 
            join recruit.user_test_det_content d on d.det_id = det.id
            where det.status != -1
            {where_sql}
            order by -det.id
            limit {(page_id - 1) * page_size}, {page_size} ;
        """
    page_data = db.default.fetchall_dict(sql)
    user_ids = [x.add_user for x in page_data]
    userdata = db.default.user_tea_det.filter(user_id__in=user_ids)
    username_dict = {x.user_id: x.name for x in userdata}
    userphone_dict = {x.user_id: x.phone_number for x in userdata}
    for obj in page_data:
        obj['add_time'] = trancate_date(obj.add_time)
        if obj.role == 1:
            obj['name'] = username_dict.get(obj.add_user, f'游客{obj.add_user}')
            obj['phone'] = userphone_dict.get(obj.add_user, '')
        else:
            obj['name'] = f'游客{obj.add_user}'
            obj['phone'] = '/'
    data = Struct()
    data.page_data = page_data
    data.sum_len = data.sum_len = get_page_len(where_sql)
    return ajax.ajax_ok(data)


def get_page_len(where_sql):
    """获取总页数"""
    sql = f"""
    select count(det.id) num 
    from recruit.user_test_det det 
    join recruit.user_test_det_content d on d.det_id = det.id
    where det.status != -1
    {where_sql}
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
        select q.do_time as q_do_time, q.id, q.title, q.version, q.`level`, q.desc,
        q.`size`,det.content,det.add_time, q.sid, det.update_time  from recruit.user_test_det t
        join recruit.user_test_det_content det on det.det_id =t.id and t.id={id_}
        join recruit.question q on q.id =det.question_id 
    """
    data = db.default.fetchall_dict(sql)
    # 获取题目扩展信息
    qids = [x.id for x in data]
    step_list = db.default.question_step_detail.filter(question_id__in=qids, status=1)
    step_dict = defaultdict(list)
    for x in step_list:
        step_dict[x.question_id].append(x.content)
    step_answer = db.default.question_step_answer.filter(question_id__in=qids, status=1)
    answer_dict = defaultdict(list)
    for x in step_answer:
        answer_dict[x.question_id].append(x.content)
    os_detail = db.default.question_os_detail.filter(question_id__in=qids, status=1)
    os_dict = defaultdict(list)
    for x in os_detail:
        os_dict[x.question_id].append(x.content)

    sid_name = all_subjects()
    for q in data:
        if q.update_time:
            do_time = q.update_time - q.add_time
            q['do_time'] = f'{do_time}秒' if do_time < 60 else f"{round(do_time / 60)}分"
        else:
            q['do_time'] = f"1分钟"
        q['q_do_time'] = f'{q.q_do_time}分'
        q['add_time'] = trancate_date(q['add_time'])
        q['sid'] = sid_name[q['sid']]
        q['level'] = level_name[str(q['level'])]
        q['size'] = size_name[str(q['size'])]
        q['step_list'] = step_dict[q.id]
        q['answer_list'] = answer_dict[q.id]
        q['os_list'] = os_dict[q.id]
        q.content = json.loads(q.content)
        for x in q.content:
            if x['type'] == 1:
                x['msg'] += '\r\n'
    return ajax.ajax_ok(data[:])




