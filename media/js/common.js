
// 成功提醒
function msg_ok(message, callback) {
    layer.msg(message, {icon: 1, time: 1500}, callback)
}

// 失败提醒
function msg_fail(message, callback) {
    layer.msg(message, {icon: 2, time: 1500}, callback)
}