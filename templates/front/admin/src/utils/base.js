const base = {
    get() {
        return {
            url : "http://localhost:8080/django7681v/",
            name: "django7681v",
            // 退出到首页链接
            indexUrl: 'http://localhost:8080/front/index.html'
        };
    },
    getProjectName(){
        return {
            projectName: "网上求职招聘系统"
        } 
    }
}
export default base
