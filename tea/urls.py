# coding:utf-8
__author__ = "ila"

from django.urls import path, re_path
from tea import views, question, user, subject

# url规则列表
urlpatterns = [
    path(r'userinfo/', views.user_info),
    path(r'add/', views.add_tea),
    path(r'register_role/', views.register_role),  # 注册选择角色
    path(r'register_yonghu/', views.register_yonghu),  # 注册选择用户角色
    path(r'login/', views.login),
]

# 题库
urlpatterns += [
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
    re_path(r'^redirect/$', question.redirect),  # 跳转到做题页
    re_path(r'^do_question/$', question.do_question),  # 单个题目做题
]

urlpatterns += [
    re_path(r'^user/test_list/$', user.user_test_list),  # 获取做题记录
    re_path(r'^user/user_test_del/$', user.user_test_del),  # 删除做题记录
    re_path(r'^user/user_test_det/$', user.get_user_test_det),  # 获取做题详情
]

urlpatterns += [
    re_path(r'^subject/add/$', subject.add),  # 编辑科目
    re_path(r'^subject/status/$', subject.status),  # 删除科目
    re_path(r'^subject/index/$', subject.index),  # 科目列表
    re_path(r'^subject/all/$', subject.all_subjects),  # 所有科目
]
