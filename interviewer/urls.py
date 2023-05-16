# coding:utf-8
__author__ = "ila"

import os
from django.urls import path, re_path
from interviewer import views

# url规则列表
urlpatterns = [
    path(r'userinfo/', views.user_info),
    path(r'add/', views.add_tea),
    path(r'login/', views.login),
]
