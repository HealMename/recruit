# coding: utf-8
import datetime
import json
import logging
import os
import time
from urllib.parse import quote

import requests
from django.http import HttpResponseRedirect

from libs.WeChat.base import WebChatBase
from libs.utils import Struct, ajax, db
from requests_toolbelt import MultipartEncoder

log = logging.getLogger(__name__)


class WebChatUser(WebChatBase):

    def get_oauth_url(self, urls, scope="snsapi_base", state="STATE"):
        """
        返回认证的url
        :param scope:
        :param state:
        :return:
        """
        domain = "open.weixin.qq.com"
        oauth_url = "https://{0}/connect/oauth2/authorize?appid={1}&" \
                    "redirect_uri={2}&" \
                    "response_type=code&" \
                    "scope={3}&" \
                    "state={4}&" \
                    "connect_redirect=1" \
                    "#wechat_redirect"
        return HttpResponseRedirect(oauth_url.format(domain, self.app_id, self.encode_url(urls), scope, self.encode_url(str(state))))

    @staticmethod
    def encode_url(url):
        # url编码
        return quote(url, safe='')

    def _get_access_token(self, code):
        """
        根据code获取access_token/openid
        :param code:
        :return:
        """
        path = "sns/oauth2/access_token"
        args = "appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (self.app_id, self.app_secret, code)
        # logging.error('***args***:%s', args)
        return self.request_api(path, args)

    def _refresh_access_token(self, code):
        # 刷新token
        pass

    def create_share(self, open_id):
        """分享二维码"""
        access_token = self.get_access_token()
        args = f"access_token={access_token}"
        path = f"cgi-bin/qrcode/create"
        data = {
            "action_name": "QR_LIMIT_STR_SCENE",
            "action_info": {
                "scene": {
                    "scene_str": open_id
                }
            }
        }

        res = self.request_api(path, args, body=data, method='post')
        res['img_url'] = f"https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={self.encode_url(res['ticket'])}"
        return res

    def upload_media(self, url, user_id):
        """
        上传资源
        type_ 1联系我 2分享二维码
        """
        now = int(time.time())
        media = db.default.wechat_user_share.filter(user_id=user_id, app_id=2)
        if media:
            media = media.first()
            return media.media_id
        access_token = self.get_access_token()
        data = {"access_token": access_token,
                  "type": "image"}
        f = open(url, 'rb')
        m = MultipartEncoder(
            fields={
                'type': "image",
                "title": "filename.png",
                "introduction": "图片",
                'data': ('', json.dumps(data), 'application/image'),
                'media': (
                    "filename.png",  # 上传的文件名，这里为filename
                    f,
                    'application/image'
                )})
        post_url = f"https://{self.webChat_domain}/cgi-bin/material/add_material?access_token={access_token}&type=image"
        res = requests.post(url=post_url, headers={'Content-Type': m.content_type}, data=m)
        res = res.json()
        media_id = res['media_id']
        f.close()
        os.remove(url)
        # 分享二维码
        db.default.wechat_user_share.create(app_id=2, user_id=user_id, media_id=media_id, path=f"|{user_id}|", add_date=now)
        # 返回素材ID
        return media_id

    def open_wx_app(self):
        """拉起小程序"""
        access_token = self.get_access_token()
        args = f"access_token={access_token}"
        path = f"wxa/generatescheme"
        data = {
            "jump_wxa": {
                "path": "pages/index/index"
            }

        }
        res = self.request_api(path, args, body=data, method='post')
        return res

    def login(self, code):
        args = f"appid={self.app_id}&secret={self.app_secret}&js_code={code}&grant_type=authorization_code"
        path = f"sns/jscode2session"
        res = self.request_api(path, args, method='post')
        return res

    def create_qr(self, scene_str):
        """公众号二维码"""
        access_token = self.get_access_token()
        args = f"access_token={access_token}"
        path = f"cgi-bin/qrcode/create"
        data = {
            "action_name": "QR_LIMIT_STR_SCENE",
            "action_info": {
                "scene": {
                    "scene_str": scene_str
                }
            }
        }
        log.info(data)
        res = self.request_api(path, args, body=data, method='post')
        print(res)
        res['img_url'] = f"https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={self.encode_url(res['ticket'])}"
        return res

    def login_img(self):
        """获取登陆二维码"""
        access_token = self.get_access_token()
        args = f"access_token={access_token}"
        path = f"wxa/getwxacodeunlimit"
        body = {
            "page": "pages/index/index",
            "scene": "a=1",
            "env_version": "develop"
        }
        res = self.request_api(path, args, body=body, method='post')
        return res

    def get_unionid(self, open_id):
        """获取公众平台唯一id"""
        access_token = self.get_access_token()
        args = f"access_token={access_token}&openid={open_id}&lang=zh_CN"
        path = f"cgi-bin/user/info"
        res = self.request_api(path, args, method='post')
        return res

    def get_phone_number(self, code):
        """获取手机号"""
        access_token = self.get_access_token()
        args = f"access_token={access_token}"
        body = {'code': code}
        headers = {
            "content-type": "application/json"
        }
        path = f"wxa/business/getuserphonenumber"
        res = self.request_api(path, args, body=body, headers=headers, method='post')
        return res

    def user(self, code):
        base_map = self._get_access_token(code)
        access_token = base_map.get("access_token")
        open_id = base_map.get("openid")
        if not access_token or not open_id:
            return {}
        r = Struct(base_map)
        return r

    def send_text(self, open_id, content):
        """发送文字消息"""
        access_token = self.get_access_token()
        path = "cgi-bin/message/custom/send"
        args = f"access_token={access_token}"
        headers = {
            "content-type": "application/json",
            "charset": "utf-8",
        }
        data = {
            "touser": open_id,
            "msgtype": "text",
            "text":
            {
                 "content": content
            }
        }
        res = self.request_api(path, args, body=data, headers=headers, method='post')
        if res.get('errcode', 0):
            return False, "推送异常"
        else:
            return True, "推送成功"

    def send_message(self, user_id, status):
        """发送模板消息"""
        access_token = self.get_access_token()
        path = "cgi-bin/message/template/send"
        args = f"access_token={access_token}"
        phone = db.default.users.get(id=user_id).username
        bind = db.default.wechat_user.get(phone=phone, status=1)
        if not bind:
            return False, "当前用户未绑定"
        openid = bind.open_id
        name = db.default.user_tea_det.get(user_id=user_id).name
        data = self.generate_push_message_data(openid, name, status)
        res = self.request_api(path, args, data=data, method='post')
        if res.get('errcode', 0):
            log.error(f"推送异常：{res}")
            print(f"推送异常：{res}")
            return False, "推送异常"
        else:
            return True, "推送成功"

    def open_send_message(self, open_id, city, type_, url):
        """发送模板消息"""
        access_token = self.get_access_token()
        path = "cgi-bin/message/template/send"
        args = f"access_token={access_token}"
        data = self.send_open_message(open_id, city, type_, url)
        res = self.request_api(path, args, data=data, method='post')
        if res.get('errcode', 0):
            return False, "推送异常"
        else:
            return True, "推送成功"

    def is_follow(self, user_id):
        """
        获取用户信息
        https://api.weixin.qq.com/cgi-bin/user/info?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN
        """
        access_token = self.get_access_token()
        path = "cgi-bin/user/info"
        bind = db.default.tbkt_bind.get(tbkt_user_id=user_id, status=1, open_type=1)
        if not bind:
            return 0
        openid = bind.open_id
        args = f"access_token={access_token}&openid={openid}&lang=zh_CN"
        res = self.request_api(path, args, method='get')
        return res.get('subscribe', 0)

    def send_login_message(self, user_id, ip):
        """发送模板消息"""
        now = int(time.time())
        access_token = self.get_access_token()
        path = "cgi-bin/message/template/send"
        args = f"access_token={access_token}"
        phone = db.default.users.get(id=user_id).username
        bind = db.default.wechat_user.get(phone=phone, status=1)
        if not bind:
            return False, "当前用户未绑定"
        openid = bind.open_id
        name = db.default.user_tea_det.get(user_id=user_id).name
        data = self.login_message_data(openid, name, ip)
        res = self.request_api(path, args, data=data, method='post')
        if res.get('errcode', 0):
            log.error(f"推送异常：{res}")
            print(f"推送异常：{res}")
            return False, "推送异常"
        else:
            db.default.logins.create(ip=ip, phone=phone, user_id=user_id, add_date=now)
            return True, "推送成功"

    def login_message_data(self, openid, name, ip):
        """登陆成功消息"""
        now = datetime.datetime.now()
        minute = int(now.minute)
        if minute < 10:
            minute = f"0{minute}"

        data = {
            "touser": openid,
            "template_id": "aF0h75Dv3S0wUJNnaLtoYOuiUh8f6-a4mHfzRaUJz-8",
            # "miniprogram": {
            #     "appid": "wx8df523611cfc0418",
            #     "pagepath": "pages/center/login"
            # },
            # "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx494761502aee644d&redirect_uri=https%3A%2F%2Fwww.ittest008.com%2Fchat%2Fwx%2Flogin%2F&response_type=code&scope=snsapi_base&state=4&connect_redirect=1#wechat_redirect",
            "data": {
                "thing1": {
                    "value": f"{name}",
                    "color": "#173177"
                },
                "character_string2": {
                    "value": f"{ip}",
                    "color": "#173177"
                },
                "time3": {
                    "value": "{}月{}日 {}:{}".format(now.month, now.day, now.hour, str(minute)),
                    "color": "#173177"
                },
            }
        }
        return json.dumps(data)


    def generate_push_message_data(self, openid, name, status):
        """获取模板消息json"""
        now = datetime.datetime.now()
        minute = int(now.minute)
        if minute < 10:
            minute = f"0{minute}"
        if status == 1:
            # 通过
            template_id = "vtmT1Yo84CemZ7se_7wciN8-CxGiL_uKgoqZdRmzZXc"
        else:
            # 驳回
            template_id = "u4YfqO54Jrvb4mFMJMcQ95paYGS6P7u9R5D6Tra-8EA"
        data = {
            "touser": openid,
            "template_id": template_id,
            # "miniprogram": {
            #     "appid": "wx8df523611cfc0418",
            #     "pagepath": "pages/center/login"
            # },
            "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx494761502aee644d&redirect_uri=https%3A%2F%2Fwww.ittest008.com%2Fchat%2Fwx%2Flogin%2F&response_type=code&scope=snsapi_base&state=4&connect_redirect=1#wechat_redirect",
            "data": {
                "phrase1": {
                    "value": f"{name}",
                    "color": "#173177"
                },
                "thing1": {
                    "value": f"{name}",
                    "color": "#173177"
                },
                "time2": {
                    "value": "{}月{}日 {}:{}".format(now.month, now.day, now.hour, str(minute)),
                    "color": "#173177"
                },
            }
        }
        return json.dumps(data)

    def send_open_message(self, openid, city, type_, url=""):
        """
        测试
        获取模板消息json
        """
        timeStamp = int(time.time())
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d", timeArray)

        data_dict = self.get_weath(city, type_)
        title = self.get_title(otherStyleTime)
        value = f"{city} {otherStyleTime} {data_dict['wea']}" if type_ == 0 else f"{city} 明天 {data_dict['wea']}"
        data = {
            "touser": openid,
            "template_id": "IvSUC69kKBYppen_4W-3yijuAsgLNIW5HMOfKR72jwE",
            "url": url,
            "data": {
                "first": {
                    "value": value,
                    "color": "#FF6100"
                },
                "keyword1": {
                    "value": data_dict['tmp'],
                    "color": "#33A1C9",
                },
                "keyword2": {
                    "value": data_dict['qlt'],
                    "color": "#173177"
                },
                "keyword3": {
                    "value": title,
                    "color": "#FF7F50"
                },
            }
        }
        return json.dumps(data)

    def get_title(self, title):
        """词霸每日一句名言"""
        url = f"http://sentence.iciba.com/index.php?c=dailysentence&m=getdetail&title={title}"
        wea_data = requests.post(url).json()
        title = wea_data['note']
        content = wea_data['content']
        return f"""
        {title}
        {content}
"""

    def get_weath(self, city, type_):
        """获取天气"""

        api_key = "f57aa9e300284184b8dd400000a1daa6"
        # 获取温度和天气情况api
        wea_api = "https://free-api.heweather.com/v5/forecast?city=%s&key=%s" % (city, api_key)
        # 获取空气质量api
        qlt_api = "https://free-api.heweather.com/v5/aqi?city=%s&key=%s" % (city, api_key)

        # 无缓存重新请求接口获取数据
        # 温度和天气数据
        wea_data = requests.post(wea_api).json()['HeWeather5'][0]['daily_forecast'][type_]
        # 组合数据格式
        tmp_data = wea_data['tmp']
        wea_txt = u"%s" % wea_data["cond"]["txt_d"]
        tmp_txt = u"%s~%s%s" % (tmp_data['min'], tmp_data['max'], u"℃")
        # 空气质量数据
        qlt_data = requests.post(qlt_api).json()['HeWeather5'][0]['aqi']['city']['qlty']
        data_dict = {"wea": wea_txt, "tmp": tmp_txt, "qlt": qlt_data, "school_city": city}
        return data_dict


def wx_user(f):
    def inner(request):
        args = request.QUERY.casts(code=str)
        code = args.code
        if not code:
            return ajax.jsonp_fail(request, message='not found code!')
        if not getattr(request, 'user', {}):
            user = WebChatUser(1).user(code)
            request.user = user
        return f(request)
    return inner


