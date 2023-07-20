$(function ($) {
    var post_login = false, $wrap = $(".login_wrap"), codeBtn = $("#getCodeBtn");
    var s = 60, timer = null;
    $wrap.on("input", ".input_ele", function () {
        if ($(this).hasClass("phone")) {
            if ($(this).val()) {
                $(this).next().show();
                if (s == 60) {
                    codeBtn.removeAttr("disabled");
                }
            } else {
                $(this).next().hide();
                codeBtn.attr("disabled", "disabled");
            }
        }
        $(this).val($(this).val().replace(/\D/g, ''));
        if ($("#account").val() && $("#ver_code").val()) {
            $(".login_btn").prop("disabled", false);
        } else {
            $(".login_btn").prop("disabled", true);
        }
    })
    $wrap.on("click", ".clear_icon", function () {
        $(this).prev().val("").focus();
        $(this).hide();
        $(".login_btn").prop("disabled", true);
        codeBtn.attr("disabled", "disabled");
    })


    $wrap.on("click", "#getCodeBtn", function () {
        if (!telNumberCheck($("#account").val())) {
            layer.tips("手机号输入不正确");
            return;
        }
        $(this).attr("disabled", "disabled");
        codeBtn.html('60s');
        $.post('/sms/send/', {
            'phone': $("#account").val(),
            'code_id': 2
        }, function (res) {
            if (res.response == 'ok') {
                layer.tips("验证码发送成功！");
            } else {
                layer.tips(res.message);
                clearFn();
            }
        });
        timer = setInterval(function () {
            s--;
            if (s == 0) {
                clearTimeout(timer)
                clearFn();
            } else {
                codeBtn.html(s + 's');
            }
        }, 1000)
    });

    function clearFn() {
        codeBtn.removeAttr("disabled");
        codeBtn.html("获取验证码");
        s = 60;
        clearInterval(timer);
    }


    $wrap.on("click", ".login_btn", function () {
        var phone = $("#account").val(), ver_code = $("#ver_code").val();
        if (!telNumberCheck(phone)) {
            layer.tips("登录手机号输入不正确");
            return false;
        } else if (ver_code.length != 6) {
            layer.tips("请输入6位数字的验证码");
            return false;
        }
        post_login = true;

        $.post("/sms/verify_code/", {
            'phone': phone,
            'code': ver_code,
            'code_id': 2
        }, function (res) {
            if (res.response == 'ok') {
                $.post('/chat/wx/login/', {
                    'phone': phone,
                    'open_id': open_id,
                }, function (res) {
                    localStorage.setItem("ZXT_OPEN_ID", open_id);
                    localStorage.setItem("ZXT_PHONE", phone);
                    post_login = false;
                    if (res.response == 'ok') {
                        layer.tips('绑定成功');
                    } else {
                        layer.tips(res.message);
                    }
                })

            } else {
                layer.tips(res.message);
            }
        })

    })

    function telNumberCheck(tel) {
        var pattern = /^[1][3-9][0-9]{9}$/;
        return pattern.test(tel)
    }


    $("#stu_wrap").on("click", ".use_btn", function () {
        var token = $(this).data("token");
        var user_id = $(this).data("userid"),
            userphone = $(this).data("phone");
        if (open_id) {
            $.post(wx_api_url + "/qm/bind/phone", {
                "phone": userphone,
                "user_id": user_id,
                "open_id": open_id,
                "user_type": 1,
                "open_type": 5
            }, function (res) {

            })
        }
        var url = '';
        if (redirect_url) {
            if (redirect_url.indexOf("?") > -1) {
                url = redirect_url + "&tbkt_token=" + token;
            } else {
                url = redirect_url + "?tbkt_token=" + token;
            }
        } else {

            if (user_type == 1 && !is_share.length) {  //学生地址
                url = task_vue_url + "/qualityStation/index?place=1&tbkt_token=" + token;
            } else if (user_type == 1 && is_share.length) {
                url = task_vue_url + "/qualityStation/tasklist?place=1&tbkt_token=" + token;
            }
        }
        // console.log(url)
        location.href = url;

    })
})