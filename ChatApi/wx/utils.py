# coding: utf-8
# 开发平台文档：https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html
import datetime
import json
import logging
import os
import time
import uuid
from io import BytesIO

from PIL import Image

import requests

from libs.WeChat.user import WebChatUser
from libs.utils import db, get_upload_key
import xml.etree.ElementTree as ET

from libs.utils.thread_pool import start_thiread
from tbkt import settings
from tbkt.settings import GHAT_ID

log = logging.getLogger(__name__)


def give(is_new_user, open_id):
    """邀请新用户 赠送5次"""
    if is_new_user:
        user = db.wechat_lzfd.auth_user.filter(open_id=open_id, status=1, type=2)
        if user:
            user_id = user.first().id
            sql = f"""
                update wechat_lzfd.chatapi_open_detail set speak_num= speak_num+5 where user_id={user_id}
            """
            db.wechat_lzfd.execute(sql)


def parse_xml(xml):
    # 解析xml 并返回指定消息给发送者
    root = ET.fromstring(xml)
    print(root)
    open_id = root.findtext(".//FromUserName")
    from_user = root.findtext(".//ToUserName")
    user_content = root.findtext(".//Content")
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg_type = root.findtext(".//MsgType")
    if msg_type == "text":
        user_id = db.wechat_lzfd.auth_user.filter(open_id=open_id, status=1, type=2).first().id
        open_info = db.wechat_lzfd.chatapi_open_detail.filter(user_id=user_id)
        is_ok = True
        is_free = 0
        if sum([x.is_free for x in open_info]):
            # 终身免费用户
            is_ok = True
            is_free = 1
            print("终身免费")
        else:
            # 正常用户
            if not open_info:  # 未开通
                is_ok = False
                print("未查询到开通记录")
            elif sum([x.speak_num for x in open_info]) == 0:  # 已耗尽次数
                is_ok = False
                print("已耗尽次数")
        if not is_ok:
            text_content = """\
您的次数已用完，请购买后使用！
"""
        else:
            speak_num = sum([x.speak_num for x in open_info]) if not is_free else '∞'
            text_content = f"""\
 ChatGPT机器人正在思考中...
 
 请稍候~ 
 
 温馨提醒：如果感觉ChatGPT回答的不完整，可以回复“继续”  
 
 剩余对话次数: ({speak_num-1 if speak_num != '∞' else speak_num})"""

            start_thiread(send_text, open_info, user_id, open_id, user_content)
        return customer_content % (open_id, from_user, create_time, "text", text_content)
    elif msg_type == "event":
        event = root.findtext(".//Event")
        event_key = root.findtext(".//EventKey")
        wx = WebChatUser(GHAT_ID)
        res = wx.get_unionid(open_id)
        unionid = res.get('unionid', '-1')
        now = int(time.time())
        bind = db.wechat_lzfd.wechat_bind.filter(open_id=open_id, unionid=unionid, type=2)
        if not bind:
            db.wechat_lzfd.wechat_bind.create(open_id=open_id, unionid=unionid, type=2, add_time=now)
        user = db.wechat_lzfd.auth_user.filter(open_id=open_id, type=2)
        is_new_user = False
        if not user:
            # 新用户
            is_new_user = True
            id_ = db.wechat_lzfd.auth_user.create(open_id=open_id, unionid=unionid, type=2, add_time=now, status=1)
            db.wechat_lzfd.chatapi_open_detail.create(user_id=id_, speak_num=10, key='', add_date=now, is_free=0)
        print(event)
        print(event_key)
        content = """\
你好，我是ChatGpt聊天机器人，我可以回答你所有的问题，点击左下角键盘图标，开始和我对话吧！
"""
        if event == "subscribe":  # 关注事件
            if "qrscene_" in event_key:  # 未关注用户扫描带参数二维码
                lod_open_id = event_key.replace('qrscene_', '')  # 老用户open_id
                give(is_new_user, lod_open_id)
            content = """\
你好，我是ChatGpt聊天机器人，我可以回答你所有的问题，点击左下角键盘图标，开始和我对话吧！
"""
            db.wechat_lzfd.wechat_bind.filter(open_id=open_id, unionid=unionid, type=2).update(is_follow=1)
            send_content = """\
你可以这样问我
1.写一篇关于春的作文
2.出10道口算题
3.推荐一个最好的股票
4.写一个Python的抓取代码
5.写一段英文文章
6.王者荣耀用什么英雄打上单容易
7.如何和心仪的女生表白
"""
            start_thiread(subscribe_send_text, open_id, send_content)
        elif event == "unsubscribe":  # 取关事件
            db.wechat_lzfd.wechat_bind.filter(open_id=open_id, unionid=unionid, type=2).update(is_follow=2)
        elif event == "SCAN":  # 已关注用户扫码
            give(is_new_user, event_key)
        elif event == "CLICK":  # 点击菜单事件
            if event_key == 'get_code':  # 获取邀请码
                res = wx.create_share(open_id)
                service_url = detail_img_one_school(res['img_url'])
                media_id = wx.upload_media(service_url, open_id)
                return img_content % (open_id, from_user, create_time, "image", media_id)
            elif event_key == "customer":  # 联系我
                media_id = "Mxopz_pztkhZ-kM039T2so187neCdfjyY2bOedZkMO9emGzJoqoM2AiX1_MJZewo"
                return img_content % (open_id, from_user, create_time, "image", media_id)
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


customer_content = """\
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>{%s}</CreateTime>
<MsgType><![CDATA[%s]]></MsgType>
<Content><![CDATA[%s]]></Content>
</xml>"""

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


def send_text(open_info, user_id, open_id, user_content):
    """回复消息"""
    now = int(time.time())
    record = db.wechat_lzfd.user_speak_detail.filter(user_id=user_id).order_by('-add_date')[:2]
    content_list = []
    prompt = user_content
    for obj in record:
        if not prompt:
            prompt = obj.user
        content_list.append({"role": "user", "content": obj.user})
        content_list.append({"role": "assistant", "content": obj.ai})
    content_list.append({"role": "user", "content": user_content})
    print(prompt)
    print(content_list)
    url = f"""http://www.chatgpt368.com/api/admin/auth/chat/?token=123&prompt={prompt}&model=gpt-3.5-turbo&messages={json.dumps(content_list)}"""
    data = dict(
        token='11233322',
        prompt=prompt,
        model='gpt-3.5-turbo',
        messages=json.dumps(content_list)
    )
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    i = 0
    res_content = {'result': prompt}
    while i < 3:
        try:
            res = requests.post(url, headers=headers, data=json.dumps(data))
            print(res)
            data = res.json()
            print(data)
            res_content = data.get('data')
            if res_content.get('code') not in (201, 200, 202):
                # 异常请求
                time.sleep(2)
                i += 1
            else:
                break
        except Exception as e:
            print(e)
            time.sleep(2)
            log.error(f"chatgpt 接口异常: {e}")
            i += 1
            res_content = {'result': "chatgpt 接口异常 请联系管理员！"}
    if not res_content:
        res_content = {'result': "chatgpt 接口异常 请联系管理员！"}
    if res_content.get('code') == 200:
        res_content = res_content['result']
        db.wechat_lzfd.user_speak_detail.create(user_id=user_id, add_date=now, user=user_content, ai=res_content)
        for obj in open_info:
            if obj.speak_num > 0:
                speak_num = obj.speak_num - 1
                db.wechat_lzfd.chatapi_open_detail.filter(id=obj.id).update(speak_num=speak_num)
                break

    wx = WebChatUser(GHAT_ID)
    wx.send_text(open_id, res_content)
    return True


def subscribe_send_text(open_id, send_content):
    """关注发送消息"""
    time.sleep(3)
    wx = WebChatUser(GHAT_ID)
    wx.send_text(open_id, send_content)
    return True


def upload_service(new_url):
    """文件上传服务器"""
    # url = "http://upload.m.xueceping.cn/swf_upload/?upcheck=" + get_upload_key() + "&upType=qrcode"
    url = settings.FILE_UPLOAD_URLROOT + "/swf_upload/?upcheck=" + get_upload_key() + "&upType=qrcode"
    files = {"file": open(new_url, 'rb')}
    response = requests.post(url, files=files)
    file_name = response.content.decode("utf8").split(',')[2].split(":")[1].replace("'", "")
    return file_name


def detail_img_one_school(img_url):
    """
    给（一校一码）二维码加上文字信息
    code_info_id: code_info表id
    img_url: 待处理的二维码链接(后半截)
    type_: 单校二维码类型
    school_name: 二维码上要加入的文字 一般为学校名字
    :return:
    """
    code_info_id = str(uuid.uuid4())
    path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    data = requests.get(img_url)
    qr_code_image = Image.open(BytesIO(data.content))
    qr_code_image.convert("RGBA")
    try:
        qr_bk_image = Image.open(path + "/site_media/img/bj_image.png")
    except Exception as e:
        print(e)
        return ""
    box = (425, 1500, 825, 1900)
    region = qr_code_image.resize((box[2] - box[0], box[3] - box[1]))
    qr_bk_image.paste(region, box)
    qr_bk_image.save(path + "/site_media/img/qr_image_{}.png".format(code_info_id))
    # 保存及返回
    code_path = path + "/site_media/img/qr_image_{}.png".format(code_info_id)
    return code_path
