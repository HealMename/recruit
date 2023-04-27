import config from './config'
import axios from 'axios'

let tools = {
    install: null
};


// Promise 添加finally方法
Promise.prototype.finally = function (callback) {
    return this.then(
        () => Promise.resolve(callback()),
        () => Promise.reject(callback())
    )
};
// Date 添加format方法
Date.prototype.format = function () {
    return `${this.getFullYear()}-${this.getMonth() + 1}-${this.getDate()} ${this.getHours()}:${this.getMinutes()}:${this.getSeconds()}`
};

Date.prototype.formatDay = function () {
    return `${this.getFullYear()}-${this.getMonth() + 1}-${this.getDate()}`
};

Date.prototype.formatMonthDay = function () {
    return `${this.getMonth() + 1}-${this.getDate()} ${this.getHours()}:${this.getMinutes()}`
};

Date.prototype.formatDateTime = function () {
    return `${this.getHours()}:${this.getMinutes()}:${this.getSeconds()}`
};

// 数组包含判断
function isSubArray(parent, child) {
    for (let item of child) {
        if (!parent.includes(item.trim())) {
            return false
        }
    }
    return true
}


// response处理
function handleResponse(response, router) {
    if (response.status === 401) {
        localStorage.setItem('token', '');
        if (location.href.indexOf("/trialgtp") == -1) {
            router.push({ name: 'login' });
        }
        response.data.data = "";
        response['result'] = response.data.data;
        Vue.$layer_message("登录已过期，请重新登陆");
        return Promise.resolve(response)
    } else if (response.data.status === "201") {
        response['result'] = response.data.message;
        return Promise.resolve(response)
    } else if (response.data.hasOwnProperty('data') && response.data.hasOwnProperty('message')) {
        if (response.data.message) {
            response['result'] = response.data.message
            return Promise.reject(response)
        } else {
            response['result'] = response.data.data;
            return Promise.resolve(response)
        }
    } else if (response.status === 400) {
        response['result'] = '无效的数据格式';
        for (var key in response.data.message) {
            response['result'] = response.data.message[key];//key所对应的value
        }
    } else if (response.status === 200) {
        return Promise.resolve(response)
    } else if (response.status === 500) {
        response['result'] = '程序异常'
    } else {
        response['result'] = '无效的数据格式'
    }
    return Promise.reject(response)
}

tools.install = function (Vue, router) {
    Vue.prototype.$config = config;
    // 请求拦截器
    axios.interceptors.request.use(request => {
        if (!request.url.startsWith("http")) {
            request.headers['token'] = localStorage.getItem("Token");
            if (request.url.startsWith("/wx/") || request.url.startsWith("/qywx/")) {
                request.url = config.apiServer + "/api" + request.url;
            } else {
                request.url = config.apiServer + "/django7681v/" + request.url;
            }
            // 删除POST请求中值为空的字段
            for (let key in request.data) {
                let val = request.data[key]
                if (typeof val === 'undefined' || (typeof val === 'object' && !val) || val === '') {
                    // ||前边表示值为undefined，||后边表示值为null
                    // 如果直接判断值为 '' ，则用户删除某些字段传了空字符串将会失效
                    delete request.data[key]
                }
            }
            // 删除GET请求中值为空的字段
            for (let key in request.params) {
                let val = request.params[key]
                if (typeof val === 'undefined' || (typeof val === 'object' && !val) || val === '') {
                    // ||前边表示值为undefined，||后边表示值为null
                    // 如果直接判断值为 '' ，则用户删除某些字段传了空字符串将会失效
                    delete request.params[key]
                }
            }
        }
        request.timeout = 120000;
        return request
    });
    // 返回拦截器
    axios.interceptors.response.use(response => {
        return handleResponse(response, router, Vue)
    }, error => {
        if (error.response) {
            return handleResponse(error.response, router, Vue)
        }
        return Promise.reject({ result: '请求异常： ' + error.message })
    });
    Vue.prototype.$http = axios;
    Vue.prototype.$layer_message = function (message, type) {
        this.$message({
            showClose: true,
            duration: 5000,
            message: message,
            type: type || 'error'
        })
    };
    // 全局socket链接
    Vue.prototype.$sockets = function (namespace) {
        let token = localStorage.getItem('token');
        let socketUrl = namespace ? `${config.apiServer}/${namespace}?token=${token}` : `${config.apiServer}?token=${token}`;
        if (namespace.indexOf("?") > 1) {
            socketUrl = `${config.apiServer}/${namespace}&token=${token}`;
        }
        return io.connect(socketUrl)
    };
    // 权限判断
    Vue.prototype.has_permission = function (str_code) {
        // return true
        if (localStorage.getItem('is_super') === 'true' || localStorage.getItem('is_super') === "1") {
            return true
        }
        let permissions = localStorage.getItem('permissions');
        if (!str_code || !permissions) return false;
        permissions = permissions.split(',');
        for (let or_item of str_code.split('|')) {
            if (isSubArray(permissions, or_item.split('&'))) {
                return true
            }
        }
        return false
    };
    // 路由导航钩子
    // router.beforeEach((to, from, next) => {
    //     next()
    // });
    // 下载压缩文件包
    Vue.prototype.downloadFileTar = function (url, name) {
        axios({
            url: url,
            method: 'GET',
            responseType: 'blob', // important
        }).then((resp) => {
            let data = resp.data;
            let blob = new Blob([data], { type: 'application/octet-stream' });
            let url = window.URL.createObjectURL(blob);
            let link = document.createElement("a");
            link.style.display = "none";
            link.href = url;
            link.setAttribute("download", name);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url)
        }).catch(function (error) {
            console.log(error)
        });
    };
};

export default tools;