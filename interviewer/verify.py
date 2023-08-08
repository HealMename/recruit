
from libs.WeChat.user import WebChatUser
from libs.utils import ajax, db
from libs.utils.common import Struct


def index(request):
    """
    面试官
    """
    id_ = request.QUERY.get('id')
    type_ = request.QUERY.get('type', 0)
    status = request.QUERY.get('status', 0)
    page_id = request.QUERY.get('page_id', 1)
    page_size = request.QUERY.get('page_size', 5)
    where_sql = ""
    if id_:
        where_sql += f" and (u.id = {id_} or u.username like '%{id_}%')"
    if type_:
        where_sql += f" and u.type = {type_}"
    else:
        where_sql += f" and u.type in (2, 3)"
    if status:
        where_sql += f" and u.status = {status}"
    sql = f"""
            select u.id, u.type, u.addtime as add_time, u.status, u.username phone  
            from recruit.users u where status>=-1
            {where_sql} 
            order by -u.addtime
            limit {(page_id - 1) * page_size}, {page_size} ;
        """
    page_data = db.default.fetchall_dict(sql)
    phones = [x.phone for x in page_data]
    name_dict = {x.phone_number: x.name for x in db.default.user_tea_det.filter(phone_number__in=phones, status=1, name__ne='')}
    for q in page_data:
        q['type_name'] = {2: '出题专家', 3: '面试官'}[q['type']]
        q['status'] = {-1: "未通过", 0: "未审核", 1: "已通过"}[q['status']]
        q['name'] = name_dict.get(q.phone, '')
    data = Struct()
    data.page_data = page_data
    data.sum_len = data.sum_len = get_page_len(where_sql)
    return ajax.ajax_ok(data)


def get_page_len(where_sql):
    """获取总页数"""
    sql = f"""
    select count(u.id) num
    from recruit.users u where status>=-1
        {where_sql} 
    """
    num = db.default.fetchone_dict(sql)
    return num.num if num else 0


def set_status(request):
    """修改审核状态"""
    id_ = request.QUERY.get('id')
    status = request.QUERY.get('status')
    feedback = request.QUERY.get('feedback', '')
    db.default.users.filter(id=id_).update(status=status, feedback=feedback)
    if status in (1, -1):
        wx = WebChatUser(2)
        wx.send_message(id_, status)
    return ajax.ajax_ok()


