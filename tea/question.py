import time

from django.shortcuts import render

from libs.utils import ajax, db, auth_token
from libs.utils.common import Struct, render_template, num_to_ch


def get_question_class(request):
    """
    教师注册
    """
    data = Struct()
    data.list = [
        {
            'id': 1,
            'name': 'K8s',
            'content': 'Kubernetes（通常被简称为K8s）是一个开源的容器编排平台，可以管理和部署容器化应用程序。'
                       '它最初由Google设计并开源，目的是为了帮助开发人员更好地管理和扩展容器化应用程序。',
            'image': '/media/img/k8s.png',
        },
        {
            'id': 2,
            'name': 'Mysql',
            'content': 'MySQL是一个开源的关系型数据库管理系统（RDBMS），它使用SQL（结构化查询语言）作为操作语言，'
                       '可以在各种操作系统上运行。',
            'image': '/media/img/mysql.png',
        },
        {
            'id': 3,
            'name': 'Python',
            'content': 'Python是一种通用、高级编程语言，由Guido van Rossum于1989年开发。Python具有简单易学、'
                       '代码可读性强、灵活多样的特点，广泛应用于Web开发、数据科学、人工智能等领域。',
            'image': '/media/img/k8s.png',
        },
        {
            'id': 4,
            'name': 'Vue',
            'content': 'Vue是一种流行的JavaScript框架，由Evan You于2014年开发。'
                       'Vue使用了响应式数据绑定和组件化的开发方式，可以帮助开发者更高效、更灵活地构建用户界面。',
            'image': '/media/img/mysql.png',
        },

    ]
    data.list = data.list * 2
    return ajax.ajax_ok(data=data)


