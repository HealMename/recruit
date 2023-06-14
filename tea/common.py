from libs.utils import db


def all_subjects():
    """获取所有科目"""
    data = {x.id: x.name for x in db.default.subjects.filter(status=1).select('id', 'name')}
    return data

