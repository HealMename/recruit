import json
import time

import random

from django.http import HttpResponseRedirect

from dj2.settings import K8S_URL
from libs.utils import ajax, db, auth_token
from libs.utils.common import Struct, trancate_date

level_name = {'1': "初级", "2": "中级", "3": "高级"}
sid_name = {'1': "K8s", "2": "Mysql", "3": "Vue"}
size_name = {'1': '单机', "2": "集群", "3": "多集群"}

ROLE = {"用户": 1, "教师": 2, "面试官": 3, "企业": 4}


def user_test_list(request):
    """"""
    return ajax.ajax_ok()