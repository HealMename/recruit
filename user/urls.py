# coding:utf-8
__author__ = "ila"

from django.urls import path, re_path
from user import views


# url规则列表
urlpatterns = [
    re_path(r'^login/$', views.login),
]
