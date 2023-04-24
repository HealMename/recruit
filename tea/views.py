from django.shortcuts import render
from libs.utils.common import Struct, render_template, num_to_ch


def add_tea(request):
    """
    教师注册
    """
    data = Struct()

    return render_template(request, 'tea/index.html', data)

