import json
import time

from django.shortcuts import render

from libs.utils import ajax, db, auth_token
from libs.utils.common import Struct, render_template, num_to_ch, trancate_date


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
            'name': 'Python',
            'content': 'Python是一种通用、高级编程语言，由Guido van Rossum于1989年开发。Python具有简单易学、'
                       '代码可读性强、灵活多样的特点，广泛应用于Web开发、数据科学、人工智能等领域。',
            'image': '/media/img/k8s.png',
        },
        {
            'id': 4,
            'name': 'Vue',
            'content': 'Vue是一种流行的JavaScript框架，由Evan You于2014年开发。'
                       'Vue使用了响应式数据绑定和组件化的开发方式，可以帮助开发者更高效、更灵活地构建用户界面。',
            'image': '/media/img/mysql.png',
        },

    ]
    data.list = data.list * 2
    return ajax.ajax_ok(data=data)


def question_list(request):
    """
    题目列表
    """
    id_ = request.QUERY.get('id')
    page_id = request.QUERY.get('page_id', 1)
    page_size = request.QUERY.get('page_size', 5)
    user_id = request.user.id
    where_sql = ""
    if id_:
        if id_.isdigit():
            where_sql += f" and id = {id_}"
        else:
            where_sql += f" and (title like '%{id_}%' or content like '%{id_}%')"
    sql = f"""
        select * from question 
        where status in (0, 1) and add_user = {user_id}
        {where_sql}
        order by -id
        limit {(page_id -1) * page_size}, {page_size} ;
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
        q['level_name'] = {'1': "初级", "2": "中级", "3": "高级"}[str(q['level'])]
        q['level'] = str(q['level'])
        q['sid'] = str(q['sid'])
        q['sid_name'] = {'1': "K8s", "2": "Mysql", "3": "Vue"}[str(q['sid'])]
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

