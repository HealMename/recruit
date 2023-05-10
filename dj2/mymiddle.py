import json

from django.http import HttpResponse, HttpRequest
from django.utils.deprecation import MiddlewareMixin
import logging as log

from libs.utils import ajax, Struct

write_list = ['/']


def get_auth(request):
    return Struct()


def get_user(request):
    return Struct()


# 添加auth属性,保存账户ID和用户ID
HttpRequest.auth = get_auth
HttpRequest.user = get_user


class CoreMiddle(MiddlewareMixin):

    def process_request(self, request):
        try:
            return self._process_request(request)
        except Exception as e:
            log.error(e)

    @staticmethod
    def cross_domain(request, response=None):
        """
        添加跨域头
        """
        origin = request.META.get('HTTP_ORIGIN', '*')
        if request.method == 'OPTIONS' and not response:
            response = HttpResponse()
        if not response:
            return
        response['Access-Control-Allow-Origin'] = origin
        response['Access-Control-Allow-Methods'] = 'GET,POST'
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Allow-Headers'] = 'x-requested-with,content-type,HTTP_TOKEN,Token,App-Type,platform'
        response['Access-Control-Max-Age'] = '1728000'
        # response['X-Frame-Options'] = 'allow-from *'
        return response

    def _process_request(self, request):
        try:
            # REQUEST过期, 使用QUERY代替
            query = request.GET.copy()
            query.update(request.POST)
            # 把body参数合并到QUERY
            try:
                if request.body:
                    body = json.loads(request.body)
                    query.update(body)
            except Exception as e:
                pass
            r = self.cross_domain(request)

            request.QUERY = query

            if r:
                return r

        except Exception as e:
            log.error(e)


    def process_response(self, request, response):
        if request.method == 'OPTIONS':
            response['Access-Control-Allow-Headers'] = '*'  # 如果是 * 就代表全部IP都可以访问
        response['Access-Control-Allow-Origin'] = '*'
        return response
