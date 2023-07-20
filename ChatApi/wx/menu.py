# coding: utf-8
import json
import requests
import sys
import os
# 设置工作目录
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


lzkx_data = {
    "button": [
        {
            "name": "题库浏览",
            "type": "view",
            "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx494761502aee644d&redirect_uri=https%3A%2F%2Fwww.ittest008.com%2Fchat%2Fwx%2Flogin%2F&response_type=code&scope=snsapi_base&state=4&connect_redirect=1#wechat_redirect",
            # "appid": "wx8df523611cfc0418",
            # "pagepath": "pages/index/index"
        },
        {
            "name": "个人中心",
            "sub_button": [
                {
                    "name": "个人中心",
                    "type": "view",
                    "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx494761502aee644d&redirect_uri=https%3A%2F%2Fwww.ittest008.com%2Fchat%2Fwx%2Flogin%2F&response_type=code&scope=snsapi_base&state=1&connect_redirect=1#wechat_redirect",
                    # "appid": "wx8df523611cfc0418",
                    # "pagepath": "pages/index/index"
                },
                {
                    "name": "联系客服",
                    "type": "view",
                    "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx494761502aee644d&redirect_uri=https%3A%2F%2Fwww.ittest008.com%2Fchat%2Fwx%2Flogin%2F&response_type=code&scope=snsapi_base&state=2&connect_redirect=1#wechat_redirect",
                    # "appid": "wx8df523611cfc0418",
                    # "pagepath": "pages/index/index"
                },
                {
                    "name": "投诉建议",
                    "type": "view",
                    "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx494761502aee644d&redirect_uri=https%3A%2F%2Fwww.ittest008.com%2Fchat%2Fwx%2Flogin%2F&response_type=code&scope=snsapi_base&state=3&connect_redirect=1#wechat_redirect",
                    # "appid": "wx8df523611cfc0418",
                    # "pagepath": "pages/index/index"
                }

            ]
        }
    ]
}


def menu(request):
    token = WebChatBase(2).get_access_token()
    print(token)
    data = json.dumps(lzkx_data, ensure_ascii=False)
    Client(token).create_menu(data.encode('utf-8'))
    return ajax.ajax_ok()

