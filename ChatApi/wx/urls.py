from django.conf.urls import url

from ChatApi.wx import views, pay, menu

urlpatterns = [
    url(r'^index/$', views.r_index),
    url(r'^login/$', views.login),
    url(r'^menu/$', menu.menu),
    url(r'^pay_index/$', pay.index),
    url(r'^oauth/$', views.r_oauth),  # 网页授权跳转
    url(r'^notify/$', pay.notify),  # 支付回调
    url(r'^oauth/user/$', views.r_user_info),  # 用户信息
    url(r'^create_login_img/$', views.create_login_img),  # 用户信息
    url(r'^pay/$', pay.Pay().as_view()),

]
