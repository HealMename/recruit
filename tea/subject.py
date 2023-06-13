import json
import time

from libs.utils import ajax, db
from libs.utils.common import Struct, trancate_date


def index(request):
    """
    科目管理
    """
    id_ = request.QUERY.get('id')
    page_id = int(request.QUERY.get('page_id', 1))
    page_size = int(request.QUERY.get('page_size', 5))
    where_sql = ""
    if id_:
        if id_.isdigit():
            where_sql += f" and id = {id_}"
        else:
            where_sql += f" and (title like '%{id_}%' or content like '%{id_}%')"
    sql = f"""
            select * from subjects 
            where status in (0, 1)
            {where_sql}
            order by -id
            limit {(page_id - 1) * page_size}, {page_size} ;
        """
    page_data = db.default.fetchall_dict(sql)
    for obj in page_data:
        obj['add_time'] = trancate_date(obj['add_time'])
    data = Struct()
    data.page_data = page_data
    data.sum_len = get_page_len('subjects', where_sql)
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


def add(request):
    """
    编辑科目
    """
    data = Struct()

    if request.method == 'POST':
        now = int(time.time())
        user_id = request.user.id
        args = {k: v for k, v in request.QUERY.items()}
        id_ = args.pop('id', 0)
        if id_:
            db.default.subjects.filter(id=id_).update(update_time=now, update_user=user_id, **args)
        else:
            db.default.subjects.create(add_time=now, status=1, add_user=user_id, **args)
    else:
        id_ = request.QUERY.get('id')
        data.name = ""
        data.namespace = ""
        if id_:
            sub = db.default.subjects.get(id=id_)
            data.name = sub.name
            data.id = sub.id
            data.namespace = sub.namespace
    return ajax.ajax_ok(data=data)


def status(request):
    """
    删除科目
    """
    now = int(time.time())
    user_id = request.user.id
    data = Struct()
    id_ = request.QUERY.get('id')
    db.default.subjects.filter(id=id_).update(update_time=now, update_user=user_id, status=-1)
    return ajax.ajax_ok(data=data)
