# coding:utf-8
__author__ = "ila"

import os
from django.urls import path
from tea import views


# url规则列表
urlpatterns = [
    path(r'add/', views.add_tea),
]

