define({ "api": [
  {
    "type": "get",
    "url": "/encode_password/",
    "title": "[公共接口]加密密码",
    "group": "common",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"password\": \"123456\"  密码\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"response\": \"ok\",\n    \"data\": \"sha1$4EPUN9mYQcWJ$fd217c695073f27e9a1ea21f7c8ba6d9576d1181\",\n    \"error\": \"\",\n    \"next\": \"\",\n    \"message\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "user/views.py",
    "groupTitle": "common",
    "name": "GetEncode_password"
  },
  {
    "type": "get",
    "url": "/verify_password/",
    "title": "[公共接口]验证密码是否正确",
    "group": "common",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"password\": \"123456\",  # 登陆密码\n    \"encoded\": \"sha1$awnulEq41wMD$e9ac1787d66808c1c431268f7ed779ba1d8d05a4\"    # 加密密码\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"response\": \"ok\",\n    \"data\": 1,  1正确 0错误\n    \"error\": \"\",\n    \"next\": \"\",\n    \"message\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "user/views.py",
    "groupTitle": "common",
    "name": "GetVerify_password"
  }
] });
