import datetime
import hashlib
import os
import uuid
from io import BytesIO

import requests
from PIL import ImageFont, ImageDraw, Image

from dj2.settings import UPLOAD_URL, web_file_url, MEDIA_SITE
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


def detail_img_subject(name, subject, level, img_url, star_status):
    """
    生成战报
    """
    code_info_id = str(uuid.uuid4())
    data = requests.get(img_url)
    qr_code_image = Image.open(BytesIO(data.content))
    qr_code_image.convert("RGBA")
    qr_bk_image = Image.open(MEDIA_SITE + f"/img/subject_{star_status}.png")
    box = (124, 475, 221, 571)
    region = qr_code_image.resize((box[2] - box[0], box[3] - box[1]))
    qr_bk_image.paste(region, box)
    draw_table = ImageDraw.Draw(im=qr_bk_image)
    # 姓名
    position = (159, 277)
    draw_table.text(position, name, (255, 231, 195), font=ImageFont.truetype(MEDIA_SITE + "/img/msyh.ttc", 17))
    # 学科
    position = (100, 335)
    draw_table.text(position, subject, (255, 231, 195), font=ImageFont.truetype(MEDIA_SITE + "/img/msyh.ttc", 18))
    # 级别
    position = (100, 362)
    draw_table.text(position, level, (255, 231, 195), font=ImageFont.truetype(MEDIA_SITE + "/img/msyh.ttc", 22))

    qr_bk_image.save(MEDIA_SITE + "/img/qr_image_{}.png".format(code_info_id))
    path = MEDIA_SITE + "/img/qr_image_{}.png".format(code_info_id)
    file = upload_service(path)
    os.remove(path)
    return file


def get_upload_key():
    """
    功能:生成上传key
    """
    # 上传key
    now = datetime.datetime.now()
    m = hashlib.md5()
    key_var = '%s%s' % ('bannei_upload', now.strftime("%Y%m%d"))
    m.update(key_var.encode())
    return m.hexdigest()


def upload_service(new_url):
    """文件上传服务器"""
    url = f"{UPLOAD_URL}?upcheck={get_upload_key()}&up_type=subjects"
    files = {"file": open(new_url, 'rb')}
    response = requests.post(url, files=files)
    file_name = f"{web_file_url}{response.json()['data'][0]['file_url']}"
    return file_name

