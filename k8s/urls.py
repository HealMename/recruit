# coding:utf-8
__author__ = "ila"

import os
from django.urls import path
from k8s import views

# url规则列表
urlpatterns = [
    path(r'namespace_api/', views.namespace_api),
    path(r'pods_api/', views.pods_api),

]