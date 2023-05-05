"""dj2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.views.static import serve
from django.views.generic import TemplateView
from django.conf import settings

from . import views
from dj2.settings import dbName as schemaName

urlpatterns = [

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_SITE}),  # 静态文件路径
    url(r'^upload/(?P<path>.*)$', serve, {'document_root': 'templates/front/'}),  # 静态文件路径

    path('xadmin/', admin.site.urls),
    path(r'index/', views.index),
    re_path(r'admin/lib/(?P<p1>.*)/(?P<p2>.*)$', views.admin_lib2),
    re_path(r'admin/lib/(?P<p1>.*)/(?P<p2>.*)/(?P<p3>.*)$', views.admin_lib3),
    re_path(r'admin/lib/(?P<p1>.*)/(?P<p2>.*)/(?P<p3>.*)/(?P<p4>.*)$', views.admin_lib4),
    re_path(r'admin/page/(?P<p1>.*)$', views.admin_page),
    re_path(r'admin/page/(?P<p1>.*)/(?P<p2>.*)$', views.admin_page2),
    re_path(r'admin/pages/(?P<p1>.*)$', views.admin_pages),
    re_path(r'admin/pages/(?P<p1>.*)/(?P<p2>.*)$', views.admin_pages2),

    re_path(r'front/(?P<p1>.*)$', views.schema_front1),
    re_path(r'front/(?P<p1>.*)/(?P<p2>.*)$', views.schema_front2),
    re_path(r'front/(?P<p1>.*)/(?P<p2>.*)/(?P<p3>.*)$', views.schema_front3),
    re_path(r'front/(?P<p1>.*)/(?P<p2>.*)/(?P<p3>.*)/(?P<p4>.*)$', views.schema_front4),
    re_path(r'{}/front/(?P<p1>.*)$'.format(schemaName), views.schema_front1),
    re_path(r'{}/front/(?P<p1>.*)/(?P<p2>.*)$'.format(schemaName), views.schema_front2),
    re_path(r'{}/front/(?P<p1>.*)/(?P<p2>.*)/(?P<p3>.*)$'.format(schemaName), views.schema_front3),
    re_path(r'{}/front/(?P<p1>.*)/(?P<p2>.*)/(?P<p3>.*)/(?P<p4>.*)$'.format(schemaName), views.schema_front4),

    re_path(r'static/(?P<p1>.*)$', views.admin_file1),
    re_path(r'admin/(?P<p1>.*)/(?P<p2>.*)$', views.admin_file2),
    re_path(r'admin/(?P<p1>.*)/(?P<p2>.*)/(?P<p3>.*)$', views.admin_file3),
    re_path(r'admin/(?P<p1>.*)/(?P<p2>.*)/(?P<p3>.*)/(?P<p4>.*)$', views.admin_file4),
    re_path(r'layui/(?P<p1>.*)$', views.layui1),
    re_path(r'layui/(?P<p1>.*)/(?P<p2>.*)$', views.layui2),
    re_path(r'layui/(?P<p1>.*)/(?P<p2>.*)/(?P<p3>.*)$', views.layui3),
    re_path(r'layui/(?P<p1>.*)/(?P<p2>.*)/(?P<p3>.*)/(?P<p4>.*)$', views.layui4),
    re_path(r'pages/(?P<p1>.*)$', views.front_pages),
    re_path(r'pages/(?P<p1>.*)/(?P<p2>.*)$', views.front_pages2),
    re_path(r'modules/(?P<p1>.*)$', views.front_modules),
    re_path(r'css/(?P<p1>.*)$', views.css1),
    re_path(r'js/(?P<p1>.*)$', views.js1),
    re_path(r'img/(?P<p1>.*)$', views.img1),
    path(r'test/<str:p1>/', views.test),
    path(r'null', views.null),
    path(r'get_ip_city/', views.get_ip_city),
    path('{}/'.format(schemaName), include('main.urls')),  # 导入schemaName
]

urlpatterns.extend([
    path(r'admin/', TemplateView.as_view(template_name='front/admin/dist/index.html')),
])

urlpatterns.extend([
    path(r'index.html', TemplateView.as_view(template_name='front/index.html')),
    path(r'{}/index.html'.format(schemaName), TemplateView.as_view(template_name='front/index.html')),
    path(r'{}/front/index.html'.format(schemaName), TemplateView.as_view(template_name='front/index.html')),
    path(r'', TemplateView.as_view(template_name='front/index.html')),
])

urlpatterns += [
    url(r'tea/', include('tea.urls')),
    url(r'user/', include('user.urls')),

]
