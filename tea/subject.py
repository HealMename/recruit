import time

from libs.utils import ajax, db
from libs.utils.common import Struct


def index(request):
    """
    科目管理
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
            db.default.subjects.create(add_time=now, add_user=user_id, **args)
    else:
        pass
    return ajax.ajax_ok(data=data)


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
            db.default.subjects.create(add_time=now, add_user=user_id, **args)
    else:
        pass
    return ajax.ajax_ok(data=data)

