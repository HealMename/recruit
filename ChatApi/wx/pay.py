# coding: utf-8

from rest_framework.decorators import api_view
from rest_framework.views import APIView

import time
import xmltodict
import random
import requests
from django.conf import settings
from django.http import HttpResponse

from libs.WeChat.pay import WxPayConfig
from libs.WeChat.user import WebChatUser
from libs.utils import ajax, get_client_ip, db, Struct, render_template
from dj2.settings import GHAT_ID

ROOT_URL = settings.ROOT_URL


def index(request):
    """
    支付首页
    """
    data = Struct()
    code = request.GET.get('code')
    open_id = request.GET.get('open_id')
    if not code:
        url = f"https://{ROOT_URL}/chatapi/wx/pay_index/"
        scope = 'snsapi_base'
        state = ""
        return WebChatUser(GHAT_ID).get_oauth_url(url, scope=scope, state=state)
    if not open_id:
        user_info = WebChatUser(GHAT_ID).user(code)
        open_id = user_info.get('openid')
    data.open_id = open_id
    user = db.wechat_lzfd.auth_user.filter(open_id=open_id, status=1, type=2)
    if user:
        user_id = user.first().id
        open_info = db.wechat_lzfd.chatapi_open_detail.get(user_id=user_id)
        data.sun_count = open_info.speak_num if open_info.is_free == 0 else '永久有效'
    return render_template(request, 'wx/pay.html', data)


class Pay(APIView):

    def post(self, request):
        """
        @api {get} /api/wx/pay/ [支付]
        @apiGroup pay
        @apiParamExample {json} 请求示例
            {
                "type_id": 1, # 1 30天 2 90天 3 180天 4 永久
            }
        @apiSuccessExample {json} 成功返回
            {
                "response": "ok",
                "data": {
                    "appId": "wxd518ff8d7d88ebeb",
                    "timeStamp": 1676515080,
                    "nonceStr": "xEQOZOXIUBgWKtUL",
                    "package": "prepay_id=wx16103802683181aaa8d49855ef0d010000",
                    "signType": "MD5",
                    "paySign": "50E32D21822A69E7F57036130546FA30",
                    "order_no": "20230216103759734"
                },
                "error": "",
                "next": "",
                "message": ""
            }
       """


        open_id = request.POST.get('open_id')
        user_id = 0
        user = db.wechat_lzfd.auth_user.filter(open_id=open_id, status=1, type=2)
        if user:
            user_id = user.first().id
        phone = ''
        config_id = GHAT_ID
        type_id = int(request.POST.get('type_id'))
        ip = get_client_ip(request).split(",")[0]
        order_no = WxPayConfig.create_trade_no()
        notify_url = ROOT_URL + "/chatapi/wx/notify/"
        if type_id not in [5, 6, 7, 8, 9]:
            return ajax.jsonp_fail(request, message="参数错误")

        wxPay = WxPayConfig(notify_root=notify_url, res_ip=ip, order_no=order_no, config_id=config_id)
        if not wxPay.active:
            return ajax.jsonp_fail(request, message="参数错误")
        product = db.wechat_lzfd.pay_product.get(id=type_id)
        price = product.price
        res, error = wxPay.payExecute_open_id(trade_type="JSAPI", open_id=open_id, price=price)
        print(error)
        if res:
            print(res)
            add_order(user_id, type_id, order_no, 1, price, config_id, phone, open_id, product.content)
            return ajax.ajax_ok(res)
        return ajax.ajax_fail(message=error)


def add_order(user_id, type_id, out_trade_no, pay_type, price, config_id, phone, open_id, content):
    """添加订单"""
    ctime = int(time.time())
    db.wechat_lzfd.other_pay_order.create(
        user_id=user_id,
        product_id=type_id,
        open_id=open_id,
        remark=f'用户购买{content}服务',
        phone_number=phone,
        out_trade_no=out_trade_no,
        wechat_type=pay_type,
        status=0,
        pay_money=price,
        add_date=ctime,
        config_id=config_id
    )


@api_view(['POST'])
def notify(request):
    body = request.body
    content = xmltodict.parse(body, encoding='utf-8').get("xml")
    out_trade_no = content.get("out_trade_no", "")
    order_db = db.wechat_lzfd.other_pay_order.get(out_trade_no=out_trade_no)
    config_id = order_db.config_id if order_db else 0
    wxpay_class = WxPayConfig(config_id=config_id)
    is_sign = wxpay_class.check_sign(content)
    if is_sign:
        args = dict(
            appid=content.get("appid", ""),
            mch_id=content.get("mch_id", ""),
            transaction_id=content.get("transaction_id", ""),
            nonce_str=str(random.randint(0, 10000))
        )
        args["sign"] = wxpay_class.create_sign(args)
        url = wxpay_class.wx_gate_way + "orderquery"
        r = requests.post(url, data=wxpay_class.trans_dict_to_xml(args).encode())
        pay_data = wxpay_class.result(r)
        if pay_data.data:
            data = pay_data.data
            time_end = data.time_end  # 支付完成时间
            my_trade_no = data.out_trade_no
            trade_state_desc = data.trade_state_desc
            update_order(my_trade_no, time_end, data.trade_state, data.transaction_id, trade_state_desc)
            if data.trade_state == "SUCCESS":
                resp = HttpResponse(wxpay_class.trans_dict_to_xml({'return_code': 'SUCCESS', 'return_msg': 'OK'}))
                return resp
    resp = HttpResponse(wxpay_class.trans_dict_to_xml({'return_code': 'FAIL', 'return_msg': 'error'}))
    return resp


def update_order(out_trade_no, time_end, trade_state, transaction_id, trade_state_desc):
    """更新订单"""
    order_no_db = db.wechat_lzfd.other_pay_order.get(out_trade_no=out_trade_no)
    if order_no_db:
        db.wechat_lzfd.other_pay_order.filter(out_trade_no=out_trade_no).update(
            third_order_no=transaction_id,
            pay_date=int(time.mktime(time.strptime(time_end, "%Y%m%d%H%M%S"))),
            status=1 if trade_state == "SUCCESS" else 0,
            trade_state_desc=trade_state_desc
        )
    if trade_state == "SUCCESS":
        product_id = order_no_db.product_id
        user_id = order_no_db.user_id
        if product_id in (5, 6, 7, 8):
            speak_num = db.wechat_lzfd.pay_product.get(id=product_id).period  # 开通周期
            sql = f"""
                update wechat_lzfd.chatapi_open_detail set speak_num = speak_num+{speak_num} where user_id={user_id}
            """
            db.wechat_lzfd.execute(sql)
        elif product_id == 9:
            sql = f"""
                update wechat_lzfd.chatapi_open_detail set is_free = 1 where user_id={user_id};
            """
            db.wechat_lzfd.execute(sql)




