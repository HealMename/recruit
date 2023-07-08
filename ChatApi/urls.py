from django.conf.urls import url
from django.urls import include

urlpatterns = [
    url(r'^wx/', include('ChatApi.wx.urls')),      # 微信平台服务
]