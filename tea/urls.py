# coding:utf-8
__author__ = "ila"

import os
from django.urls import path
from tea import views, question


# url规则列表
urlpatterns = [
    path(r'add/', views.add_tea),
    path(r'login/', views.login),
    path(r'get_question_class/', question.get_question_class),
]

