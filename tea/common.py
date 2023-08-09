from libs.utils import db


level_name = {'1': "初级", "2": "中级", "3": "高级"}
size_name = {'1': '单机', "2": "集群", "3": "多集群"}


def all_subjects():
    """获取所有科目"""
    data = {x.id: x.name for x in db.default.subjects.filter(status=1).select('id', 'name')}
    return data


def get_question(qid):
    q = db.default.question.get(id=qid)
    step_list = db.default.question_step_detail.filter(question_id=qid, status=1)
    step_answer = db.default.question_step_answer.filter(question_id=qid, status=1)
    os_detail = db.default.question_os_detail.filter(question_id=qid, status=1)
    data = {
        "id": qid,
        "sid": q.sid,
        "do_time": q.do_time,
        "do_points": q.do_points,
        "version": str(q.version),
        "is_free": str(q.is_free),
        "level": str(q.level),
        "title": q.title,
        "desc": q.desc,
        "size": str(q.size),
        "status": str(q.status),
        "step_list": [{'content': x.content} for x in step_list] if step_list else [{'content': ''}],
        "answer_list": [{'content': x.content} for x in step_answer] if step_answer else [{'content': ''}],
        "os_detail": [{'content': x.content} for x in os_detail] if os_detail else [{'content': ''}],
    }
    sid_name = all_subjects()
    data['status_name'] = {-1: '已删除', 1: '已审核', 0: '未审核'}[q['status']]
    data['level_name'] = level_name[str(q['level'])]
    data['size_name'] = size_name[str(q['size'])]
    data['sid_name'] = sid_name[q['sid']]
    return data


def get_q_count(qids):
    """获取做题人数"""
    sql = f"""
        select question_id, count(id) num  from recruit.user_test_det_content where question_id in ({','.join(map(str, qids))})
        group by question_id;
    """
    data = db.default.fetchall_dict(sql)
    q_count = {x.question_id: x.num for x in data}
    return q_count


def get_fa_count(qids):
    """获取收藏人数"""
    # 收藏人数
    sql = f"""
            select question_id, count(user_id) num from user_question_favorites 
            where status=1 and question_id in ({','.join(map(str, qids))}) group by question_id;
        """
    data = db.default.fetchall_dict(sql)
    fa_count = {x.question_id: x.num for x in data}
    return fa_count

