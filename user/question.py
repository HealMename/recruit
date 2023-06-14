import json
import time

import random

from libs.utils import ajax, db
from libs.utils.common import Struct, trancate_date

level_name = {'1': "初级", "2": "中级", "3": "高级"}
sid_name = {'1': "K8s", "2": "Mysql", "3": "Vue"}
size_name = {'1': '单机', "2": "集群", "3": "多集群"}


def get_question_class(request):
    """
    题目分类列表
    """
    data = Struct()
    data.list = [
        {
            'id': 1,
            'name': 'K8s',
            'content': 'Kubernetes（通常被简称为K8s）是一个开源的容器编排平台，可以管理和部署容器化应用程序。'
                       '它最初由Google设计并开源，目的是为了帮助开发人员更好地管理和扩展容器化应用程序。',
            'image': '/media/img/k8s.png',
        },
        {
            'id': 2,
            'name': 'Mysql',
            'content': 'MySQL是一个开源的关系型数据库管理系统（RDBMS），它使用SQL（结构化查询语言）作为操作语言，'
                       '可以在各种操作系统上运行。',
            'image': '/media/img/mysql.png',
        },
        {
            'id': 3,
            'name': 'Vue',
            'content': 'Vue是一种流行的JavaScript框架，由Evan You于2014年开发。'
                       'Vue使用了响应式数据绑定和组件化的开发方式，可以帮助开发者更高效、更灵活地构建用户界面。',
            'image': '/media/img/mysql.png',
        },

    ]
    data.list = data.list * 2
    return ajax.ajax_ok(data=data)


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
    id_ = db.default.user_test_det.create(type=2, content=content, status=0, add_user=user_id, add_time=now, do_time=0)
    return ajax.ajax_ok(id_)


def get_paper_question(request):
    """获取试卷关联题目"""
    type_ = int(request.QUERY.get('type'))  # 1 1考试试卷 2随机试卷
    paper_id = request.QUERY.get('paper_id')  # 试卷id
    if type_ == 1:
        sql = f"""
            select q.* from django7681v.paper_question p
            join django7681v.question q on q.id=p.question_id
            where p.paper_id ={paper_id} and p.status =1
        """
        data = db.default.fetchall_dict(sql)[:]
    else:
        ids = [x['id'] for x in json.loads(db.default.user_test_det.get(id=paper_id).content)]
        data = db.default.question.filter(id__in=ids)[:]
    for q in data:
        q['add_time'] = trancate_date(q['add_time'])
        q['sid'] = str(q['sid'])
        q['sid_name'] = sid_name[str(q['sid'])]
        q['level'] = str(q['level'])
        q['level_name'] = level_name[str(q['level'])]
        q['size'] = str(q['size'])
        q['size_name'] = size_name[str(q['size'])]
        q['urls'] = [{'value': x} for x in json.loads(q.pop('link_url'))]
    return ajax.ajax_ok(data)


def question_list(request):
    """
    题目列表
    """
    id_ = request.QUERY.get('id')
    sid = request.QUERY.get('sid')
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
    sql = f"""
        select * from question 
        where status in (0, 1)
        {where_sql}
        order by -id
        limit {(page_id -1) * page_size}, {page_size} ;
    """
    page_data = db.default.fetchall_dict(sql)
    for q in page_data:
        q['status'] = {1: '已审核', 0: '未审核'}[q['status']]
        q['add_time'] = trancate_date(q['add_time'])
        q['sid'] = str(q['sid'])
        q['sid_name'] = sid_name[str(q['sid'])]
        q['level'] = str(q['level'])
        q['level_name'] = level_name[str(q['level'])]
        q['size'] = str(q['size'])
        q['size_name'] = size_name[str(q['size'])]
        q['urls'] = [{'value': x} for x in json.loads(q.pop('link_url'))]
    data = Struct()
    data.page_data = page_data
    data.sum_len = get_page_len('question', where_sql)
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


def question_del(request):
    """
    删除题目
    status:1正常0未审核-1删除
    """
    id_ = request.QUERY.get('id')
    status = request.QUERY.get('status')
    db.default.question.filter(id=id_).update(status=status)
    return ajax.ajax_ok()


def question_add(request):
    """
    添加编辑
    """
    args = Struct({k: v for k, v in request.QUERY.items()})
    id_ = int(args.pop('id', 0))
    now = int(time.time())
    args.pop('add_time', '')
    args.pop('status', '')
    args.pop('level_name', '')
    args.pop('size_name', '')
    args.pop('sid_name', '')
    urls = args.pop('urls')
    args.link_url = json.dumps([x['value'] for x in urls])
    if not id_:
        db.default.question.create(add_time=now, **args)
    else:
        db.default.question.filter(id=id_).update(add_time=now, **args)
    return ajax.ajax_ok()


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
        where status in (0, 1)  and add_user = {user_id}
        {where_sql} 
        order by -id
        limit {(page_id -1) * page_size}, {page_size} ;
    """
    page_data = db.default.fetchall_dict(sql)
    for q in page_data:
        q['type_name'] = {1: '练习平台', 2: '考试平台'}[q['type']]
        q['type'] = str(q['type'])
        q['level_name'] = level_name[str(q['level'])]
        q['level'] = str(q['level'])
        q['sid'] = str(q['sid'])
        q['sid_name'] = sid_name[str(q['sid'])]
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
        q['urls'] = [{'value': x} for x in json.loads(q.pop('link_url'))]
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

