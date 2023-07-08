# coding: utf-8
import json
import requests
import sys
import os
# 设置工作目录
from tbkt.settings import GHAT_ID

sys_base_path = os.path.abspath(__file__)
sys.path.append(os.path.normpath(os.path.join(sys_base_path, '../..')))


from libs.WeChat.base import WebChatBase, BaseClient
from libs.utils import ajax


class Client(BaseClient):
    """ 
    操作菜单创建、删除、查询的客户端
    """
    base_path = 'cgi-bin/menu/'

    def get_menu(self):
        path = self.base_path + 'get'
        d = self.get(path)
        return d

    def create_menu(self, menu_data):
        path = self.base_path + 'create'
        d = self.post(path, menu_data)
        return d

    def delete_menu(self):
        path = self.base_path + 'delete'
        d = self.get(path)
        return d



beta_data = {
    "button": [
        {
            "name": "🔥Chat会员",
            "type": "view",
            "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx4cd38efa15b6b208&redirect_uri=https%3A%2F%2Flzfdapi-beta.m.xueceping.cn%2Fchatapi%2Fwx%2Fpay_index%2F&response_type=code&scope=snsapi_base&state=1&connect_redirect=1#wechat_redirect"
        },
        {
            "name": "获取邀请码",
            "sub_button": [
                {
                    "type": "click",
                    "name": "获取邀请码",
                    "key": "get_code"
                },
                {
                    "type": "click",
                    "name": "联系我",
                    "key": "customer"
                }

            ]
        }
    ]
}


lzkx_data = {
    "button": [
        {
            "name": "辅导助手",
            "type": "miniprogram",
            "url": "http://mp.weixin.qq.com",
            "appid": "wx89a94e9607692d37",
            "pagepath": "pages/index/index"
        }
    ]
}


def menu(request):
    token = WebChatBase(GHAT_ID).get_access_token()
    print(token)
    data = json.dumps(beta_data, ensure_ascii=False)
    Client(token).create_menu(data.encode('utf-8'))
    return ajax.ajax_ok()

