from django.conf.urls import url
from upload import views

urlpatterns = [
    url(r'^$', views.upload),  # 上传文件
    url(r'^upload_key/$', views.upload_key),  # 上传文件密钥
]
