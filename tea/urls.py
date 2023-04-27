# coding:utf-8
__author__ = "ila"

import os
from django.urls import path, re_path
from tea import views, question


# url规则列表
urlpatterns = [
    path(r'userinfo/', views.user_info),
    path(r'add/', views.add_tea),
    path(r'login/', views.login),
]

# 题库
urlpatterns += [
    re_path(r'^get_question_class/$', question.get_question_class),
    re_path(r'^question/$', question.question_add),
    re_path(r'^question_list/$', question.question_list),
]
