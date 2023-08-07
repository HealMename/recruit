# coding: utf-8
# 开发平台文档：https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html
import datetime
import logging
import xml.etree.ElementTree as ET

log = logging.getLogger(__name__)


def parse_xml(xml):
    # 解析xml 并返回指定消息给发送者
    root = ET.fromstring(xml)
    open_id = root.findtext(".//FromUserName")
    from_user = root.findtext(".//ToUserName")
    user_content = root.findtext(".//Content")
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg_type = root.findtext(".//MsgType")
    content = ""
    if msg_type == "text":
        pass
    elif msg_type == "event":
        event = root.findtext(".//Event")
        event_key = root.findtext(".//EventKey")
        log.info(f"{event}--{event_key}")
        type_, event_key = event_key.split(':')
        if event == "subscribe":  # 关注事件
            content = """\
            欢迎关注“云数智学堂”[玫瑰][玫瑰]
            """
            type_ = type_.replace('qrscene_', '')
            log.info(f"未关注用户扫码：{type_, event_key}")
        elif event == "unsubscribe":  # 取关事件
            pass
        elif event == "SCAN":  # 已关注用户扫码
            log.info(f"已关注用户扫码：{type_, event_key}")
        elif event == "CLICK":  # 点击菜单事件
            pass
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

