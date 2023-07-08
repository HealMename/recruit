import time

from libs.WeChat.user import WebChatUser
from libs.utils import ajax, db, auth_token, Struct
from tbkt.settings import GHAT_ID

#
# def r_user_info(request):
#     """
#     根据code获取 用户信息
#     :param request:
#     :return:
#     """
#     args = request.QUERY.casts(code=str)
#     code = args.code
#     if not code:
#         return ajax.jsonp_fail(request, message='not found code!')
#     wx = WebChatUser(GHAT_ID)
#     user = wx.user(code)
#     open_id = user.get('open_id', '')
#     if not open_id:
#         return ajax.ajax_fail(message='not found open_id')
#     res = wx.get_unionid(user.get('open_id', ''))
#     unionid = res.get('unionid', '-1')
#     now = int(time.time())
#     user = db.wechat_lzfd.auth_user.filter(open_id=open_id, type=2)
#     if not user:
#         user_id = db.wechat_lzfd.auth_user.create(
#             name='微信用户', open_id=open_id, type=2, unionid=unionid, add_time=now)
#     else:
#         user_id = user.first().id
#     db.wechat_lzfd.auth_user.filter(id=user_id).update(last_login=now)
#     token = auth_token.create_token(user_id)
#     data = Struct()
#     data.token = token
#     return ajax.ajax_ok(data)

