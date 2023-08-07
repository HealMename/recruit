# coding: utf-8
# 开发平台文档：https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html
import datetime
import logging
import time
import xml.etree.ElementTree as ET

from libs.WeChat.user import WebChatUser
from libs.utils import db

log = logging.getLogger(__name__)


def parse_xml(xml):
    # 解析xml 并返回指定消息给发送者
    root = ET.fromstring(xml)
    open_id = root.findtext(".//FromUserName")
    from_user = root.findtext(".//ToUserName")
    user_content = root.findtext(".//Content")
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg_type = root.findtext(".//MsgType")
    content = "1"
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
            if event_key:
                event_key = event_key.split(':')
                type_, event_key = event_key[0], event_key[1]
                """
                type: 1 扫码登陆 event_key=表wechat_login的id
                """

            if event == "subscribe":  # 关注事件
                content = """欢迎关注“云数智学堂”[玫瑰][玫瑰]"""
                type_ = type_.replace('qrscene_', '') if 'qrscene_' in type_ else type_
                log.info(f"未关注用户扫码：{type_}--{event_key}")
                if type_ == '1':
                    db.default.wechat_login.filter(id=event_key).update(open_id=open_id, status=1, phone=phone)
            elif event == "unsubscribe":  # 取关事件
                pass
            elif event == "SCAN":  # 已关注用户扫码
                log.info(f"已关注用户扫码：{type_}--{event_key}")
                if type_ == '1':
                    content = "扫码成功"
                    db.default.wechat_login.filter(id=event_key).update(open_id=open_id, status=1, phone=phone)
            elif event == "CLICK":  # 点击菜单事件
                pass
        except Exception as e:
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

