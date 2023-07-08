import datetime
import hashlib
import random
import time
import requests
import xmltodict
from libs.utils.common import Struct
from libs.utils import db


class WxPayConfig(object):

    def __init__(self, notify_root="", res_ip="", body="", attach="", order_no="", config_id=0):
        pay_config = db.default.wx_app.get(id=config_id, status=1)
        if not pay_config:
            self.active = False
        self.active = True                  # 支付方式存在
        self.app_id = pay_config.app_id
        self.body = body if body else pay_config.name
        self.app_secret = pay_config.app_secret
        self.mch_id = pay_config.mch_id
        self.app_key = pay_config.app_key
        self.wx_gate_way = pay_config.wx_gate_way
        self.redirect_uri = pay_config.redirect_uri
        self.spbill_create_ip = res_ip
        self.attach = attach
        self.notify_url = notify_root
        self.order_no = order_no

    @staticmethod
    def create_nonce_str():
        """生成随机字符串"""
        return str(random.randint(0, 10000))

    @staticmethod
    def create_trade_no():
        """创建用户订单号"""
        no = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        no += "%03d" % random.randint(0, 999)
        return no

    @staticmethod
    def result(resp=None, message=""):
        """结果处理
        1先判断请求微信接口返回状态是否正常
        2判断接口返回return_code 是否为SUCCESS
        3判断业务结果 result_code 是否为 SUCCESS
        """
        out = Struct()
        out.data = {}
        out.status = False
        out.message = message
        if not resp:
            return out
        if resp.status_code != 200:
            # 微信接口状态值异常
            out.message = '微信下单接口状态码异常: %s' % resp.status_code
            return out
        parse = xmltodict.parse(resp.content, encoding='utf-8').get("xml")
        if not parse:
            out.message = '微信下单接口未正常解析到数据 content={}'.format(parse)
            return out
        parse = Struct(parse)
        if parse.return_code != 'SUCCESS':
            # 当前支付微信未返回成功状态
            out.message = parse.return_msg
            return out
        result_code = parse.result_code
        err_code_des = parse.err_code_des
        if result_code != 'SUCCESS':
            # 业务结果微信未返回成功状态
            out.message = err_code_des
            return out
        out.data = parse
        out.status = True
        return out

    def create_sign(self, data):
        """生成参数签名"""
        keys = [k for k in data.keys() if k != 'sign']
        keys.sort()
        sign = "&".join("%s=%s" % (k, data[k]) for k in keys if data[k])
        sign += "&key=%s" % self.app_key
        m = hashlib.md5()
        sign = sign.encode(encoding='utf-8')
        m.update(sign)
        sign = m.hexdigest().upper()
        return sign

    def check_sign(self, d):
        """校验签名是否正确"""
        sign1 = d.get('sign')
        if not sign1:
            return False
        sign2 = self.create_sign(d)
        return sign1 == sign2

    @staticmethod
    def trans_dict_to_xml(data):
        """将 dict对象转换成微信支付交互所需的XML格式数据"""
        xml = []
        for k in sorted(data.keys()):
            v = data.get(k)
            if k == 'detail' and not v.startswith('<![CDATA['):
                v = '<![CDATA[{}]]>'.format(v)
            xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
        return '<xml>{}</xml>'.format(''.join(xml))

    def payExecute_open_id(self, trade_type="JSAPI", open_id="", price=0.01):
        """使用open_id支付"""
        total_fee = int(price * 100)
        args = dict(
            appid=self.app_id,
            mch_id=self.mch_id,
            nonce_str=self.create_nonce_str(),
            body=self.body,
            openid=open_id,
            total_fee=total_fee,
            spbill_create_ip=self.spbill_create_ip,
            notify_url=self.notify_url,
            trade_type=trade_type,
            out_trade_no=self.order_no
        )
        if trade_type == "JSAPI":
            args["sign_type"] = "MD5"
        args["sign"] = self.create_sign(args)
        r = requests.post(self.wx_gate_way + 'unifiedorder', data=self.trans_dict_to_xml(args).encode())
        r_json = self.result(r)
        if not r_json.status:
            return None, r_json.message
        if trade_type == "JSAPI":
            res_data = r_json.data
            data = dict(
                appId=res_data["appid"],
                timeStamp=int(time.time()),
                nonceStr=res_data["nonce_str"],
                package="prepay_id={prepay_id}".format(prepay_id=res_data['prepay_id']),
                signType="MD5",
            )
            data["paySign"] = self.create_sign(data)
            data["order_no"] = self.order_no
            return data, None
        return r_json.data, None
