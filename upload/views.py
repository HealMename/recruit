# coding: utf-8
import base64
import datetime
import hashlib
import logging
import time

from django.conf import settings

from upload import fileutil
from libs.utils import ajax, db, get_upload_key, UPLOAD_FILE_KEY_VALUE

log = logging.getLogger(__name__)


def upload_key(request):
    key = get_upload_key()
    return ajax.ajax_ok({'key': key})


def upload(request):
    """
    @api {post} /upload/ [系统]上传文件
    @apiGroup system
    @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {},
            "response": "ok",
            "error": ""
        }
    @apiErrorExample {json} 失败返回
        {
            "message": "....出问题了",
            "next": "",
            "data": {},
            "response": "fail",
            "error": ""
        }
    """
    now_time = datetime.datetime.now()
    md5 = hashlib.md5()
    md5.update(('%s%s' % (UPLOAD_FILE_KEY_VALUE, now_time.strftime("%Y%m%d"))).encode("utf8"))
    up_check1 = md5.hexdigest()
    up_check2 = request.QUERY.get('upcheck', '')
    if up_check1 != up_check2:
        log.info(u"[{'file_name':'','file_size':0,'status':0,'msg':'无权限访问！'}]")
        return ajax.ajax_ok([{'file_name': '', 'file_size': 0, 'status': 0, 'msg': '无权限访问！'}])
    up_type = request.QUERY.get('up_type')
    return other_upload_file(request, up_type)


def other_upload_file(request, up_type):
    """
     功能说明：其他文件上传
    ------------------------------------
    修改人        修改时间        修改原因
    ------------------------------------
    刘鑫鹏        2023-03-13
    """
    print(request.FILES)
    raw_file = request.FILES.get('file', None)
    if not raw_file:
        raw_file = request.FILES.get('Filedata', None)
    if not raw_file:
        raw_file = request.FILES.get('field1', None)
    if not raw_file:
        raw_file = request.FILES.get('obj', None)
    if not raw_file:
        raw_file = request.FILES.get('image', None)
    if not raw_file:
        raw_file = request.POST.get('file', None)
    if raw_file:

        raw_file_name = raw_file.name.replace("'", "")
        file_size = raw_file.size

        now = datetime.datetime.now()
        new_file_dir = '%s/%s' % (up_type, now.strftime("%Y/%m/%d"))
        # 重命名文件
        new_file_name = fileutil.reset_file_name(raw_file_name)
        # 新文件相对路径
        new_file_path = '%s/%s' % (new_file_dir, new_file_name)
        # 新文件绝对路径
        new_absolute_file_path = fileutil.get_absolute_file_path('%s/%s' % (new_file_dir, new_file_name))
        if fileutil.save_upload_file(new_absolute_file_path, raw_file):
            return ajax.ajax_ok([{'file_name': raw_file_name,'file_size': file_size,'file_url': new_file_path,'status':1}])
        else:
            log.info("[{'file_name':'%s','file_size':%s,'file_url':'%s','status':1}]" % (
                raw_file_name, file_size, new_file_path))
            return ajax.ajax_ok([{'file_name': raw_file_name,'file_size': file_size,'file_url': new_file_path,'status':1}])
    else:
        log.info("[{'file_name':'','file_size':0,'status':0}]")
        return ajax.ajax_ok([{'file_name':'','file_size':0,'status':0}])


def D_BASE64(origStr):
    origStr = origStr.split(",")[-1]
    if (len(origStr) % 3 == 1):
        origStr += "=="
    elif (len(origStr) % 3 == 2):
        origStr += "="
    temp = base64.b64decode(origStr)
    return temp
