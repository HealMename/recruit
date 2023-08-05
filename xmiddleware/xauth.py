# coding:utf-8
__author__ = "ila"

import logging

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.apps import apps

from util.auth import Auth
from util.codes import *
from dj2.settings import dbName as schemaName


class Xauth(MiddlewareMixin):
    def process_request(self, request):
        fullPath = request.path

        token = request.QUERY.get("token") \
                or request.META.get('HTTP_TOKEN')
        if request.method == 'GET':

            filterList = [
                "/index",
                "/favicon.ico",
                "/login",
                "/register",
                '.js',
                ".css",
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".mp4",
                'mp3',
                ".ttf",
                ".wotf",
                ".woff",
                ".woff2",
                ".otf",
                ".eot",
                ".svg",
                ".csv",
                ".xls",
                ".xlsx",
                ".doc",
                ".docx",
                ".ppt",
                ".pptx",
                ".html",
                ".htm",
                "detail",
                "/forum/flist",
                "/forum/list",
                "/admin",
                "/xadmin",
                "/file/download",
                "/{}/remind/".format(schemaName),
                "/{}/option/".format(schemaName),
                "resetPass",
                "/tea/add/",
                "/tea/get_question_class/",
                "create_login_img",
                "encode_password",
                "/chat/wx/menu/",
                "/chat/wx/index/",
                "verify_password",
                "config/list",
                "/tea/subject/all/",
                "/tea/question_list/",
                "/user/info/",
                "/interviewer/add/",
                "/interviewer/save/",
                "/about/",
                "/chat/wx/jsconfig/",
                "/django7681v/option/chengshi/chengshi",
                "/pages/zhaopinxinxi/list.html",
                "/cms/"
            ]
            allModels = apps.get_app_config('main').get_models()
            for m in allModels:
                try:
                    foreEndList = m.__foreEndList__
                except:
                    foreEndList = None
                if foreEndList is not None and foreEndList != "前要登":
                    filterList.append("/{}/sendemail".format(m.__tablename__))
                    filterList.append("/{}/list".format(m.__tablename__))

            auth = True
            if fullPath == '/':
                pass
            else:
                for i in filterList:
                    if i in fullPath:
                        auth = False
                # if token and len(token) > 10:
                #     auth = True
                if auth == True:
                    result = Auth.identify(Auth, request)
                    if result.get('code') != normal_code:
                        logging.error(fullPath, result)
                        return JsonResponse(result)
        elif request.method == 'POST':
            post_list = [
                '/chat/wx/index/',
                '/{}/defaultuser/register'.format(schemaName),
                '/{}/defaultuser/login'.format(schemaName),
                '/{}/users/register'.format(schemaName),
                '/{}/users/login'.format(schemaName),
                "/{}/examusers/login".format(schemaName),
                "/{}/examusers/register".format(schemaName),
                "/tea/add/",
                "/uploads/",
                "/interviewer/ocr_sfz/",
                "/interviewer/save/",
                "/interviewer/add/",
                "/tea/login/",
                "/chat/wx/index/",
                '/sms/send/',
                "/chat/wx/oauth/user/",
                "/tea/do_question/",
                "/sms/verify_code/",
                "/sms/send_email/"
            ]  # 免认证list
            if fullPath not in post_list and "register" not in fullPath and "login" not in fullPath \
                    and request.path not in post_list or (token and len(token) > 10):  # 注册时不检测token。
                result = Auth.identify(Auth, request, token)
                if result.get('code') != normal_code:
                    return JsonResponse(result)
