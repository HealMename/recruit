const base = {
    get() {
        return {
            url : "http://127.0.0.1:8087/",
            name: "django7681v",
            // 退出到首页链接
            indexUrl: 'http://127.0.0.1:8087/'
        };
    },
    getProjectName(){
        return {
            projectName: "面霸王"
        } 
    }
}
export default base
