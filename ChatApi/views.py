from libs.utils import upload_key, ajax


def uploadkey(request):
    """
    @api {get} /api/get_upload_key/ [公共]获取上传密钥
    @apiGroup common
    @apiParamExample {json} 请求示例
        {}
    @apiSuccessExample {json} 成功返回
        {
            "response": "ok",
            "data": {
                "key": "60ad5d3339e50f96fb311947d6cfebe7"
            },
            "error": "",
            "next": "",
            "message": ""
        }
    """
    key = upload_key()
    return ajax.ajax_ok({"key": key})
