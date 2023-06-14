import json

from libs.utils import ajax
from libs.utils.comapi import Hub
from libs.utils.redis_com import rd


K8S_API = {
    "namespace_api": "https://www.ittest008.com:8088/namespace_api/",
    "pods": "https://www.ittest008.com:8088/workload/pods_api/?namespace=%s&page=1&limit=10"
}


def namespace_api(request):
    """
    获取项目空间
    """
    redis_key = "namespace_api"
    k8s = rd.k8s.get(redis_key)
    if k8s:
        data = json.loads(k8s)
    else:
        pass
        api = Hub(request)
        res = api.k8s.get('/namespace_api/')
        # 接口缓存10分钟
        data = []
        for obj in res['data']:
            data.append({'name': obj['name']})
        rd.k8s.set(redis_key, json.dumps(data), timeout=60 * 10)
    return ajax.ajax_ok(data)


def pods_api(request):
    """
    获取项目空间下的pods
    """
    # 接口缓存10分钟
    redis_key = "pods_api"
    k8s = rd.k8s.get(redis_key)
    name = request.QUERY.get('name')
    page = request.QUERY.get('page', 1)
    if k8s:
        res = json.loads(k8s)
    else:
        api = Hub(request)
        res = api.k8s.get(f'/workload/pods_api/?namespace={name}&page={page}&limit=10')
        # 接口缓存10分钟
        rd.k8s.set(redis_key, json.dumps(res), timeout=60 * 10)
    return ajax.ajax_ok(res)

