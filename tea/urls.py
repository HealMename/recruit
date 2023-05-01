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
    re_path(r'^paper/$', question.paper),
    re_path(r'^paper_question/$', question.paper_det),
    re_path(r'^del_q/$', question.question_del),
    re_path(r'^del_p/$', question.paper_del),
    re_path(r'^save_paper_question/$', question.save_paper_question),
    re_path(r'^save_paper/$', question.save_paper),
    re_path(r'^question_list/$', question.question_list),
    re_path(r'^create_user_question/$', question.create_user_question),
    re_path(r'^get_paper_question/$', question.get_paper_question),

]
