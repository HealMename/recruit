const axios = require('axios');

const dayjs = require('dayjs');
const crypto = require('crypto');
const querystring = require('querystring');

// shar256算法
const sha256 = data => crypto.createHash('SHA256').update(data).digest('hex')
// hmacsha256算法
const hmacsha256 = (data, key) => crypto.createHmac('sha256', key).update(data).digest('hex')

// SETUP1:获取AccessKey和SecurityKey
const securityKey = 'f3f220c94cb242f2b51065a92485ca3f'
const accessKey = '65038a8f227242ab987efef3acea40dd'

const body = {
    "action": "QuerySmsSignList",
    "pageIndex": 2,
    "pageSize": 10
}

function send(body) {

// SETUP2:构造时间戳
    const timestamp = dayjs().format('YYYYMMDDTHHmmss') + 'Z'
    // const timestamp = '20230525T094351Z'

// SETUP3:构造请求流水号
    const requestId = "3"

// SETUP4:构造待签名字符串
    const headerStr = `ctyun-eop-request-id:${requestId}\neop-date:${timestamp}\n\n`
    console.log(JSON.stringify(body))
    const calculateContentHash = sha256(JSON.stringify(body))
    console.log('calculateContentHash', calculateContentHash)
    const rawString = `${headerStr}\n${calculateContentHash}`
// console.log('headerStr',headerStr)
// console.log('calculateContentHash',calculateContentHash)
    console.log('rawString', rawString)
// SETUP5:构造签名
    const signTime = hmacsha256(timestamp, securityKey)
    console.log('signTime', signTime, accessKey)
    const signAK = hmacsha256(accessKey, Buffer.from(signTime, 'hex'))
    console.log('signAK', signAK)
    const signDate = hmacsha256(timestamp.slice(0, 8), Buffer.from(signAK, 'hex'))
    console.log('signDate', signDate)
    const sign = hmacsha256(rawString, Buffer.from(signDate, 'hex'))
    console.log('sign', sign)
    const signature = Buffer.from(sign, 'hex').toString('base64')
    console.log('signature', signature)

// SETUP:6 构造请求头
    const signatureHeader = `${accessKey} Headers=ctyun-eop-request-id;eop-date Signature=${signature}`
    const headers = {
        'Content-Type': 'application/json',
        'eop-date': timestamp,
        'Eop-Authorization': signatureHeader,
        'ctyun-eop-request-id': requestId,
    }
    console.log(headers)
    console.log(body)
// SETUP:7 构造请求
    axios
        .post('https://sms-global.ctapi.ctyun.cn/sms/api/v1', body, {
            headers,
        })
        .then(res => {
            console.log(res.data)
            return res.data
        })
        .catch(err => {
            console.log(err)
        })
}


var express = require('express');
var app = express();
//设置request的解释方式
app.use(express.json());
//设置跨域访问
app.all('*', function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    res.header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS");
    res.header("X-Powered-By", ' 3.2.1');
    res.header("Content-Type", "application/json;charset=utf-8");
    next();
});


//写个接口123
app.post('/sms/send/', function (req, res) {
    var text = send(req.body)
    res.status(200),

        res.json({"message": "ok"})
});

//配置服务端口
var server = app.listen(3000, function () {
    var host = server.address().address;
    var port = server.address().port;
    console.log('Example app listening at http://%s:%s', host, port);
})
