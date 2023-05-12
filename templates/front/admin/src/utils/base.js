const base = {
    get() {
        return {
            url : DOMAIN_API_SYS + '/',
            name: "django7681v",
            // 退出到首页链接
            indexUrl: DOMAIN_API_SYS + '/'
        };
    },
    getProjectName(){
        return {
            projectName: "it学霸"
        } 
    }
}
export default base
