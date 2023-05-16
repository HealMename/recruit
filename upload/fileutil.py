#coding=utf-8
import os, datetime, logging
from django.conf import settings

log = logging.getLogger('file.fileutil')


def save_upload_file(new_file_path, raw_file):
    """
    功能说明：保存上传文件
    ------------------------------------
    修改人        修改时间        修改原因
    ------------------------------------
    杜祖永        2010-10-18
    ------------------------------------
    raw_file:原始文件对象
    new_file_path:新文件绝对路径
    new_file_dir:新文件目录
    """
    try:
        # 如果新文件存在则删除
        if os.path.exists(new_file_path):
            try:
                os.remove(new_file_path)
            except:
                pass
        
        content = raw_file.read()
        fp = open(new_file_path, 'wb')
        fp.write(content)
        fp.close()
        return True
    except Exception as ex:
        log.error('save_upload_file:'+str(ex))
        return False


def reset_file_name(raw_file_name, prefix='', type=0):
    """
    功能说明：重命名文件，
    ------------------------------------
    修改人        修改时间        修改原因
    ------------------------------------
    杜祖永        2010-10-18
    ------------------------------------
    raw_file_name:原始文件名
    prefix:新文件名前缀
    type:命名方式 0:以时间命名（默认），1：md5加密串命名
    """
    
    x = raw_file_name.rindex('.') + 1
  
    y = len(raw_file_name)
    
    ext_name = raw_file_name[x:y]
    now_time = datetime.datetime.now()

    new_file_name = '%s.%s' % (now_time.strftime("%Y%m%d%H%M%S")+str(now_time.microsecond), ext_name)
    if type == 1:
        pass
    if prefix:
        new_file_name = prefix + new_file_name
    return new_file_name


def get_absolute_file_path(file_name, prefix_dir='', media_root=''):
    """
    功能说明：返回绝对路径字符串
    ------------------------------------
    修改人        修改时间        修改原因
    ------------------------------------
    杜祖永        2010-10-18
    ------------------------------------
    file_name:格式：2010/12/25/test.zip

    """
    absolute_file_path = ''
    if media_root == '':
        media_root = settings.MEDIA_URL
    if prefix_dir:
        absolute_file_path = os.path.join(media_root, prefix_dir, file_name)
    else:
        absolute_file_path = os.path.join(media_root, file_name)

    # 返回文件绝对路径中目录路径
    file_dir = os.path.dirname(absolute_file_path)
    if not os.path.exists(file_dir):
        # 创建路径
        os.makedirs(file_dir)
    return absolute_file_path
