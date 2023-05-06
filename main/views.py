import time

from django.http import JsonResponse
from django.shortcuts import render
from util.codes import *

from libs.utils import ajax, db, auth_token
from libs.utils.common import Struct, render_template, num_to_ch
from main.users_model import users
from util.auth import Auth


def checkout_user_type(request):
    """
    切换用户身份
    """
    type_ = request.QUERY.get('type')  # 用户要切换的身份 1普通用户 2管理员 3教师 4企业用户 5面试官
    user = request.user
    print(type_, user)
    return ajax.ajax_ok()






