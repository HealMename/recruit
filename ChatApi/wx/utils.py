# coding: utf-8
# 开发平台文档：https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html
import datetime
import logging
import time
import xml.etree.ElementTree as ET
import os
import uuid
from io import BytesIO

import requests
from PIL import Image

from dj2 import settings
from libs.WeChat.user import WebChatUser
from libs.utils import db, get_upload_key

log = logging.getLogger(__name__)


def parse_xml(xml):
    # 解析xml 并返回指定消息给发送者
    root = ET.fromstring(xml)
    open_id = root.findtext(".//FromUserName")
    from_user = root.findtext(".//ToUserName")
    user_content = root.findtext(".//Content")
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg_type = root.findtext(".//MsgType")
    content = "您好有什么可以帮到您？"
    now = int(time.time())
    if msg_type == "text":
        pass
    elif msg_type == "event":
        try:
            event = root.findtext(".//Event")
            event_key = root.findtext(".//EventKey")
            wx = WebChatUser(2)
            res = wx.get_unionid(open_id)
            unionid = res.get('unionid', '')
            if unionid:
                user = db.default.wechat_user.filter(unionid=unionid, status=1)
            else:
                user = db.default.wechat_user.filter(open_id=open_id, status=1, app_id=2)
            phone = ''
            if user:
                phone = user.first().phone
            else:
                db.default.wechat_user.create(open_id=open_id, status=1, unionid=unionid, app_id=2, add_date=now)

            log.info(f"unionid:{unionid}--{event}--{event_key}")
            type_, event_key = '', event_key
            if ":" in event_key:
                event_key = event_key.split(':')
                type_, event_key = event_key[0], event_key[1]
                """
                type: 1 扫码登陆 event_key=表wechat_login的id
                type: 2 分享扫码 event_key=user_id
                """

            if event == "subscribe":  # 关注事件
                content = """欢迎关注“云数智学堂”[玫瑰][玫瑰]"""
                type_ = type_.replace('qrscene_', '') if 'qrscene_' in type_ else type_
                log.info(f"未关注用户扫码：{type_}--{event_key}")
                if type_ == '1':
                    db.default.wechat_login.filter(id=event_key).update(open_id=open_id, status=1, phone=phone)
                elif type_ == '2':
                    if not phone:  # 新用户扫码
                        share = db.default.wechat_user_share.get(user_id=event_key, status=1)
                        path = f"{share.path}{unionid}|"
                        db.default.wechat_user_share.filter(user_id=event_key, status=1).update(path=path, add_date=now)
            elif event == "unsubscribe":  # 取关事件
                pass
            elif event == "SCAN":  # 已关注用户扫码
                log.info(f"已关注用户扫码：{type_}--{event_key}")
                if type_ == '1':
                    content = "扫码成功"
                    db.default.wechat_login.filter(id=event_key).update(open_id=open_id, status=1, phone=phone)
                elif type_ == '2':
                    if not phone:   # 新用户扫码
                        share = db.default.wechat_user_share.get(user_id=event_key, status=1)
                        path = f"{share.path}{unionid}|"
                        db.default.wechat_user_share.filter(user_id=event_key, status=1).update(path=path, add_date=now)
            elif event == "CLICK":  # 点击菜单事件
                if event_key == 'get_code':  # 获取邀请码
                    if phone:
                        user_id = db.default.users.get(username=phone, type=4).id
                        media = db.default.wechat_user_share.filter(user_id=user_id, app_id=2)
                        if media:
                            media_id = media.first().media_id
                        else:
                            scene_str = f"2:{user_id}"
                            res = wx.create_qr(scene_str)
                            service_url = detail_qr_img(res['img_url'])
                            media_id = wx.upload_media(service_url, user_id)
                        return img_content % (open_id, from_user, create_time, "image", media_id)
                    else:
                        content = "请先点击下方菜单，注册账号！"
        except Exception as e:
            content = "服务器开小差，请联系管理员！"
            log.error(f"微信回调异常: {e}")
    else:
        content = "1"
    wx_test = """\
    <xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>{%s}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    </xml>""" % (open_id, from_user, create_time, content)
    return wx_test


img_content = """\
<xml>
  <ToUserName><![CDATA[%s]]></ToUserName>
  <FromUserName><![CDATA[%s]]></FromUserName>
  <CreateTime>%s</CreateTime>
  <MsgType><![CDATA[%s]]></MsgType>
  <Image>
    <MediaId><![CDATA[%s]]></MediaId>
  </Image>
</xml>"""


def detail_qr_img(img_url):
    """
    合成个人推广海报
    """
    code_info_id = str(uuid.uuid4())
    path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    data = requests.get(img_url)
    qr_code_image = Image.open(BytesIO(data.content))
    qr_code_image.convert("RGBA")
    try:
        qr_bk_image = Image.open(path + "/media/img/yaoqing.png")
    except Exception as e:
        print(e)
        return ""
    box = (50, 1540, 489, 1972)
    region = qr_code_image.resize((box[2] - box[0], box[3] - box[1]))
    qr_bk_image.paste(region, box)
    qr_bk_image.save(path + "/media/img/qr_image_{}.png".format(code_info_id))
    code_path = path + "/media/img/qr_image_{}.png".format(code_info_id)
    return code_path


def upload_service(new_url):
    """文件上传服务器"""
    # url = "http://upload.m.xueceping.cn/swf_upload/?upcheck=" + get_upload_key() + "&upType=qrcode"
    url = settings.FILE_UPLOAD_URLROOT + "/swf_upload/?upcheck=" + get_upload_key() + "&upType=qrcode"
    files = {"file": open(new_url, 'rb')}
    response = requests.post(url, files=files)
    file_name = response.content.decode("utf8").split(',')[2].split(":")[1].replace("'", "")
    return file_name

