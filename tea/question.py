import json
import time
import random
from collections import defaultdict

from dj2.settings import K8S_URL
from libs.utils import ajax, db, auth_token
from libs.utils.auth_token import get_random_string
from libs.utils.common import Struct, trancate_date, render_template
from tea.common import all_subjects, get_question, get_q_count

level_name = {'1': "初级", "2": "中级", "3": "高级"}
size_name = {'1': '单机', "2": "集群", "3": "多集群"}

ROLE = {"用户": 1, "教师": 2, "面试官": 3, "企业": 4}


def get_paper_question(request):
    """获取试卷关联题目"""
    type_ = int(request.QUERY.get('type'))  # 1 1考试试卷 2随机试卷
    paper_id = request.QUERY.get('paper_id')  # 试卷id
    if type_ == 1:
        sql = f"""
            select q.* from recruit.paper_question p
            join recruit.question q on q.id=p.question_id
            where p.paper_id ={paper_id} and p.status =1
        """
        data = db.default.fetchall_dict(sql)[:]
    else:
        ids = [x['id'] for x in json.loads(db.default.user_test_det.get(id=paper_id).content)]
        data = db.default.question.filter(id__in=ids)[:]
    sid_name = all_subjects()
    for q in data:
        q['add_time'] = trancate_date(q['add_time'])
        q['sid'] = str(q['sid'])
        q['sid_name'] = sid_name[q['sid']]
        q['level'] = str(q['level'])
        q['level_name'] = level_name[str(q['level'])]
        q['size'] = str(q['size'])
        q['size_name'] = size_name[str(q['size'])]
    return ajax.ajax_ok(data)


def question_list(request):
    """
    题目列表
    """
    id_ = request.QUERY.get('id')
    is_cms = request.QUERY.get('is_cms')
    sid = int(request.QUERY.get('sid', 0) or 0)
    is_web = int(request.QUERY.get('is_web', 0) or 0)
    status = request.QUERY.get('status')
    level = int(request.QUERY.get('level', 0) or 0)
    size = int(request.QUERY.get('size', 0) or 0)
    page_id = int(request.QUERY.get('page_id', 1))
    page_size = int(request.QUERY.get('page_size', 5))
    where_sql = ""
    if id_:
        if id_.isdigit():
            where_sql += f" and id = {id_}"
        else:
            where_sql += f" and (title like '%{id_}%' or content like '%{id_}%')"
    if sid:
        where_sql += f" and sid= {sid}"
    if level:
        where_sql += f" and level= {level}"
    if size:
        where_sql += f" and size= {size}"
    if status:
        where_sql += f" and status = {status}"
    order_sql = "order by -id"
    if is_web:
        order_sql = f"order by -is_free,-id"
    if is_cms and '1' not in request.user.open_role:
        where_sql += f' and add_user={request.user.id}'
    sql = f"""
        select * from question 
        where status in (0, 1)
        {where_sql}
        {order_sql}
        limit {(page_id - 1) * page_size}, {page_size} ;
    """
    page_data = db.default.fetchall_dict(sql)
    sid_name = all_subjects()
    qids = [x.id for x in page_data]
    os_dict = get_os_detail(qids)
    q_count = get_q_count(qids) if qids else 0
    user_ids = [x.add_user for x in page_data] + [x.verify_user for x in page_data]
    userdata = db.default.user_tea_det.filter(user_id__in=user_ids)
    username_dict = {x.user_id: x.name for x in userdata}
    for q in page_data:
        q['status_name'] = {1: '已审核', 0: '未审核'}[q['status']]
        q['add_user'] = username_dict.get(q['add_user'], '/')
        q['status'] = str(q['status'])
        q['is_free'] = str(q['is_free'])
        q['add_time'] = trancate_date(q['add_time'])
        q['verify_time'] = trancate_date(q['verify_time']) if q['status'] == '1' else '/'
        q['verify_user'] = username_dict.get(q['verify_user'], '/') if q['status'] == '1' else '/'
        q['sid_name'] = sid_name[q['sid']]
        q['level'] = str(q['level'])
        q['level_name'] = level_name[str(q['level'])]
        q['size'] = str(q['size'])
        q['size_name'] = size_name[str(q['size'])]
        q['os_detail'] = '、'.join(os_dict.get(q.id, []))
        q['q_count'] = q_count.get(q.id, 0)
        if q['q_count'] >= 10000:
            q['q_count'] = f"{round(q['q_count'] / 10000, 2)}w"
    data = Struct()
    data.page_data = page_data
    data.sum_len = get_page_len('question', where_sql)
    return ajax.ajax_ok(data)



def get_os_detail(qids):
    """获取环境信息"""
    data = defaultdict(list)
    for x in db.default.question_os_detail.filter(
            question_id__in=qids, status=1).select('content', 'question_id').order_by('sequence'):
        data[x.question_id].append(x.content)

    return data


def get_page_len(table, where_sql):
    """获取总页数"""
    sql = f"""
    select count(1) as num from {table} 
        where status in (0, 1) 
        {where_sql} 
    """
    num = db.default.fetchone_dict(sql)
    return num.num if num else 0


def question_del(request):
    """
    删除题目
    status:1正常0未审核-1删除
    """
    id_ = request.QUERY.get('id')
    status = request.QUERY.get('status')
    args = dict(status=status)
    if status == 1:
        now = int(time.time())
        user_id = request.user.id
        args.update(dict(verify_time=now, verify_user=user_id))
    db.default.question.filter(id=id_).update(**args)
    return ajax.ajax_ok()


def question_add(request):
    """
    添加编辑
    """
    args = Struct({k: v for k, v in request.QUERY.items()})
    user_id = request.user.id
    if request.method == 'POST':
        id_ = int(args.pop('id', 0))
        now = int(time.time())
        os_detail = json.loads(args.pop('os_detail_data', '[]'))  # 解题步骤列表
        step_data = json.loads(args.pop('step_data', '[]'))  # 解题步骤列表
        answer_step = json.loads(args.pop('answer_step', '[]'))  # 答题步骤列表
        args.pop('os_detail', '')
        args.pop('status', '')
        args.pop('step_list', '')
        args.pop('answer_list', '')
        args.pop('add_time', '')
        args.pop('status_name', '')
        args.pop('level_name', '')
        args.pop('size_name', '')
        args.pop('sid_name', '')
        args.add_user = user_id
        if id_:
            db.default.question.filter(id=id_).update(status=-1)
        id_ = db.default.question.create(add_time=now, status=0, **args)
        # db.default.question_step_detail.filter(question_id=id_, status=1).update(status=-1)
        # db.default.question_step_answer.filter(question_id=id_, status=1).update(status=-1)
        # db.default.question_os_detail.filter(question_id=id_, status=1).update(status=-1)
        for eq, obj in enumerate(step_data, 1):
            obj['sequence'] = eq
            obj['question_id'] = id_
            obj['status'] = 1
            obj['add_user'] = user_id
            obj['add_time'] = now
        for eq, obj in enumerate(answer_step, 1):
            obj['sequence'] = eq
            obj['question_id'] = id_
            obj['status'] = 1
            obj['add_user'] = user_id
            obj['add_time'] = now
        for eq, obj in enumerate(os_detail, 1):
            obj['sequence'] = eq
            obj['question_id'] = id_
            obj['status'] = 1
            obj['add_user'] = user_id
            obj['add_time'] = now
        db.default.question_step_detail.bulk_create(step_data)
        db.default.question_step_answer.bulk_create(answer_step)
        db.default.question_os_detail.bulk_create(os_detail)
        return ajax.ajax_ok()
    else:
        data = get_question(args.id)
        return ajax.ajax_ok(data)


def paper(request):
    """
    试卷列表
    """
    id_ = request.QUERY.get('id')
    type_ = request.QUERY.get('type', 0)
    page_id = request.QUERY.get('page_id', 1)
    page_size = request.QUERY.get('page_size', 5)
    where_sql = ""
    user_id = request.user.id
    if id_:
        if id_.isdigit():
            where_sql += f" and id = {id_}"
        else:
            where_sql += f" and name like '%{id_}%'"
    if type_:
        where_sql += f" and type = {type_}"
    sql = f"""
        select id, name, type, add_time, level, do_time, sid from paper 
        where status in (0, 1)
        {where_sql} 
        order by -id
        limit {(page_id - 1) * page_size}, {page_size} ;
    """
    page_data = db.default.fetchall_dict(sql)
    sid_name = all_subjects()
    for q in page_data:
        q['type_name'] = {1: '练习平台', 2: '考试平台'}[q['type']]
        q['type'] = str(q['type'])
        q['level_name'] = level_name[str(q['level'])]
        q['level'] = str(q['level'])
        q['sid_name'] = sid_name[q['sid']]
        q['add_time'] = trancate_date(q['add_time'])
    data = Struct()
    data.page_data = page_data
    data.sum_len = data.sum_len = get_page_len('paper', where_sql)
    return ajax.ajax_ok(data)


def paper_det(request):
    """
    试卷详情
    """
    paper_id = int(request.QUERY.get('paper_id', 0))
    sql = f"""
        select q.* from paper_question p
        join question q on q.id=p.question_id 
        where p.paper_id = {paper_id} and p.status in (0, 1)
    """
    page_data = db.default.fetchall_dict(sql)
    for q in page_data:
        q['status'] = {1: '已审核', 0: '未审核'}[q['status']]
        q['add_time'] = trancate_date(q['add_time'])
        q['sid'] = str(q['sid'])
        q['level'] = str(q['level'])
        q['size'] = str(q['size'])
    data = Struct()
    data.page_data = page_data
    d_paper = db.default.paper.get(id=paper_id)
    data.name = d_paper.name if paper_id else ''
    data.type = str(d_paper.type) if paper_id else '1'
    return ajax.ajax_ok(data)


def paper_del(request):
    """
    删除试卷
    status:1正常0未审核-1删除
    """
    id_ = request.QUERY.get('id')
    status = request.QUERY.get('status')
    db.default.paper.filter(id=id_).update(status=status)
    return ajax.ajax_ok()


def save_paper(request):
    """
    保存试卷
    """
    args = Struct({k: v for k, v in request.QUERY.items()})
    id_ = int(args.pop('id', 0))
    args.pop('add_time', '')
    args.pop('type_name', '')
    args.pop('sid_name', '')
    args.pop('level_name', '')
    now = int(time.time())
    user_id = request.user.id
    if not id_:
        db.default.paper.create(status=1, add_time=now, add_user=user_id, **args)
    else:
        db.default.paper.filter(id=id_).update(update_time=now, update_user=user_id, **args)
    return ajax.ajax_ok()


def save_paper_question(request):
    """
    关联试卷题目
    """
    paper_id = int(request.QUERY.get('paper_id', 0) or 0)
    question_id = int(request.QUERY.get('qid', 0) or 0)
    now = int(time.time())
    user_id = request.user.id
    if not db.default.question.filter(id=question_id, status__in=[0, 1]):
        return ajax.ajax_fail(message='试题ID不存在')
    if db.default.paper_question.filter(paper_id=paper_id, status=1).count() == 10:
        return ajax.ajax_fail(message='最多关联10道题目')
    if not db.default.paper_question.filter(paper_id=paper_id, question_id=question_id, status=1):
        db.default.paper_question.create(
            paper_id=paper_id, question_id=question_id, status=1, add_time=now, add_user=user_id)
    return ajax.ajax_ok(paper_id)


def redirect(role_id, user_id, message_id):
    """重定向到做题页"""
    url = K8S_URL + f"?token={auth_token.create_token(role_id, user_id)}&id={message_id}"
    return url


def do_question(request):
    """生成做题url"""
    now = int(time.time())
    type_ = int(request.QUERY.get('type'))  # 1 单题练习
    qid = request.QUERY.get('qid')  # 题目id
    city = request.QUERY.get('city', '')  # 城市
    role_id = 1
    user_id = request.user.id or 0
    q = db.default.question.get(id=qid)
    if not user_id and q.is_free != 1:
        return ajax.ajax_fail(message='请先登录账号!')
    if not user_id:
        role_id = 2
        user_id = int(get_random_string(length=6, allowed_chars='0123456789'))
    if type_ == 1:
        # 单题练习
        content = json.dumps([{"id": qid, "is_right": 0}])
        message_id = db.default.user_test_det.create(
            type=1, content=content, status=0, add_user=user_id, add_time=now,
            do_time=0, role=role_id, city=city)
        url = redirect(role_id, user_id, message_id)
        return ajax.ajax_ok(url)


def create_user_question(request):
    """
    用户按照主题练习
    """
    user_id = request.user.id or 10
    now = int(time.time())
    # 生成 q_num 个试题
    sid = request.QUERY.get('sid')  # 科目
    level = request.QUERY.get('level')  # 级别
    if not sid:
        return ajax.ajax_fail(message='请选择科目')
    if not level:
        return ajax.ajax_fail(message='请选择级别')
    q_num = request.QUERY.get('q_num')  # 做题数量
    questions = db.default.question.filter(sid=sid, level=level)
    if len(questions) < 5:
        return ajax.ajax_fail(message='题目不足， 请联系管理员')
    qids = random.sample([x.id for x in questions], int(q_num))
    content = json.dumps([{'id': x, 'is_right': 0} for x in qids])
    role_id = ROLE[request.user.role]
    message_id = db.default.user_test_det.create(
        type=2, content=content, status=0, add_user=user_id,
        add_time=now, do_time=0, role=role_id)
    url = redirect(role_id, user_id, message_id)
    return ajax.ajax_ok(url)


def question_detail_web(request):
    """查看详情"""
    data = Struct()
    qid = request.QUERY.get('qid')
    h5 = request.QUERY.get('h5')
    data.question = get_question(qid)
    data.question["desc"] = data.question["desc"].replace('\r\n', '<br/>').replace('\n', '<br/>').replace('\s', '&nbsp;')
    data.q_count = get_q_count([qid]).get(int(qid), 0)
    if h5:
        return render_template(request, 'front/pages/question/question_detail_h5.html', data)
    else:
        return render_template(request, 'front/pages/question/question_detail.html', data)

