
var projectName = 'IT学霸';
/**
 * 轮播图配置
 */
var swiper = {
	// 设定轮播容器宽度，支持像素和百分比
	width: '100%',
	height: '400px',
	// hover（悬停显示）
	// always（始终显示）
	// none（始终不显示）
	arrow: 'none',
	// default（左右切换）
	// updown（上下切换）
	// fade（渐隐渐显切换）
	anim: 'default',
	// 自动切换的时间间隔
	// 默认3000
	interval: 2000,
	// 指示器位置
	// inside（容器内部）
	// outside（容器外部）
	// none（不显示）
	indicator: 'outside'
}

/**
 * 个人中心菜单
 */
var centerMenu = [{
	name: '个人中心',
	url: '../' + localStorage.getItem('userTable') + '/center.html'
}, 
{
        name: '我的收藏',
        url: '../storeup/list.html'
}
]


var indexNav = [

{
	name: '招聘信息',
	url: './pages/zhaopinxinxi/list.html'
}, 

{
	name: '新闻资讯',
	url: './pages/news/list.html'
},
]

var adminurl =  "http://localhost:8080/django7681v/admin/dist/index.html";

var cartFlag = false

var chatFlag = false


chatFlag = true


var menu = [{"backMenu":[{"child":[{"appFrontIcon":"cuIcon-album","buttons":["新增","查看","修改","删除"],"menu":"用户","menuJump":"列表","tableName":"yonghu"}],"menu":"用户管理"},{"child":[{"appFrontIcon":"cuIcon-copy","buttons":["新增","查看","修改","删除","审核"],"menu":"公司","menuJump":"列表","tableName":"gongsi"}],"menu":"公司管理"},{"child":[{"appFrontIcon":"cuIcon-present","buttons":["新增","查看","修改","删除","查看评论"],"menu":"招聘信息","menuJump":"列表","tableName":"zhaopinxinxi"}],"menu":"招聘信息管理"},{"child":[{"appFrontIcon":"cuIcon-album","buttons":["查看","修改","删除"],"menu":"投递记录","menuJump":"列表","tableName":"toudijilu"}],"menu":"投递记录管理"},{"child":[{"appFrontIcon":"cuIcon-phone","buttons":["查看","修改","删除"],"menu":"打分记录","menuJump":"列表","tableName":"dafenjilu"}],"menu":"打分记录管理"},{"child":[{"appFrontIcon":"cuIcon-skin","buttons":["查看","修改","删除"],"menu":"投诉记录","menuJump":"列表","tableName":"tousujilu"}],"menu":"投诉记录管理"},{"child":[{"appFrontIcon":"cuIcon-circle","buttons":["查看","修改","删除"],"menu":"个人简历","menuJump":"列表","tableName":"gerenjianli"}],"menu":"个人简历管理"},{"child":[{"appFrontIcon":"cuIcon-full","buttons":["查看","修改","删除"],"menu":"岗位邀请","menuJump":"列表","tableName":"gangweiyaoqing"}],"menu":"岗位邀请管理"},{"child":[{"appFrontIcon":"cuIcon-cardboard","buttons":["查看","修改","删除"],"menu":"聊天记录","menuJump":"列表","tableName":"liaotianjilu"}],"menu":"聊天记录管理"},{"child":[{"appFrontIcon":"cuIcon-list","buttons":["查看","修改","删除"],"menu":"人才库","menuJump":"列表","tableName":"rencaiku"}],"menu":"人才库管理"},{"child":[{"appFrontIcon":"cuIcon-brand","buttons":["新增","查看","修改","删除"],"menu":"城市","menuJump":"列表","tableName":"chengshi"}],"menu":"城市管理"},{"child":[{"appFrontIcon":"cuIcon-goods","buttons":["新增","查看","修改","删除"],"menu":"岗位分类","menuJump":"列表","tableName":"gangweifenlei"}],"menu":"岗位分类管理"},{"child":[{"appFrontIcon":"cuIcon-news","buttons":["新增","查看","修改","删除"],"menu":"新闻资讯","tableName":"news"},{"appFrontIcon":"cuIcon-service","buttons":["新增","查看","修改","删除"],"menu":"客服咨询","tableName":"chat"},{"appFrontIcon":"cuIcon-news","buttons":["查看","修改"],"menu":"轮播图管理","tableName":"config"}],"menu":"系统管理"}],"frontMenu":[{"child":[{"appFrontIcon":"cuIcon-list","buttons":["查看","投递简历","公司打分","投诉","咨询"],"menu":"招聘信息列表","menuJump":"列表","tableName":"zhaopinxinxi"}],"menu":"招聘信息模块"}],"hasBackLogin":"是","hasBackRegister":"否","hasFrontLogin":"否","hasFrontRegister":"否","roleName":"管理员","tableName":"users"},{"backMenu":[{"child":[{"appFrontIcon":"cuIcon-album","buttons":["查看","修改","删除"],"menu":"投递记录","menuJump":"列表","tableName":"toudijilu"}],"menu":"投递记录管理"},{"child":[{"appFrontIcon":"cuIcon-phone","buttons":["查看","修改","删除"],"menu":"打分记录","menuJump":"列表","tableName":"dafenjilu"}],"menu":"打分记录管理"},{"child":[{"appFrontIcon":"cuIcon-skin","buttons":["查看","修改","删除"],"menu":"投诉记录","menuJump":"列表","tableName":"tousujilu"}],"menu":"投诉记录管理"},{"child":[{"appFrontIcon":"cuIcon-circle","buttons":["查看","新增","修改","删除"],"menu":"个人简历","menuJump":"列表","tableName":"gerenjianli"}],"menu":"个人简历管理"},{"child":[{"appFrontIcon":"cuIcon-full","buttons":["查看","咨询","投诉"],"menu":"岗位邀请","menuJump":"列表","tableName":"gangweiyaoqing"}],"menu":"岗位邀请管理"},{"child":[{"appFrontIcon":"cuIcon-cardboard","buttons":["查看","回复"],"menu":"聊天记录","menuJump":"列表","tableName":"liaotianjilu"}],"menu":"聊天记录管理"}],"frontMenu":[{"child":[{"appFrontIcon":"cuIcon-list","buttons":["查看","投递简历","公司打分","投诉","咨询"],"menu":"招聘信息列表","menuJump":"列表","tableName":"zhaopinxinxi"}],"menu":"招聘信息模块"}],"hasBackLogin":"是","hasBackRegister":"否","hasFrontLogin":"是","hasFrontRegister":"是","roleName":"用户","tableName":"yonghu"},{"backMenu":[{"child":[{"appFrontIcon":"cuIcon-present","buttons":["新增","查看","修改","删除","查看评论"],"menu":"招聘信息","menuJump":"列表","tableName":"zhaopinxinxi"}],"menu":"招聘信息管理"},{"child":[{"appFrontIcon":"cuIcon-album","buttons":["查看","人才信息保存","咨询"],"menu":"投递记录","menuJump":"列表","tableName":"toudijilu"}],"menu":"投递记录管理"},{"child":[{"appFrontIcon":"cuIcon-circle","buttons":["查看","人才信息保存","岗位邀请"],"menu":"个人简历","menuJump":"列表","tableName":"gerenjianli"}],"menu":"个人简历管理"},{"child":[{"appFrontIcon":"cuIcon-full","buttons":["查看","咨询"],"menu":"岗位邀请","menuJump":"列表","tableName":"gangweiyaoqing"}],"menu":"岗位邀请管理"},{"child":[{"appFrontIcon":"cuIcon-cardboard","buttons":["查看","回复"],"menu":"聊天记录","menuJump":"列表","tableName":"liaotianjilu"}],"menu":"聊天记录管理"},{"child":[{"appFrontIcon":"cuIcon-list","buttons":["查看","删除"],"menu":"人才库","menuJump":"列表","tableName":"rencaiku"}],"menu":"人才库管理"}],"frontMenu":[{"child":[{"appFrontIcon":"cuIcon-list","buttons":["查看","投递简历","公司打分","投诉","咨询"],"menu":"招聘信息列表","menuJump":"列表","tableName":"zhaopinxinxi"}],"menu":"招聘信息模块"}],"hasBackLogin":"是","hasBackRegister":"是","hasFrontLogin":"是","hasFrontRegister":"否","roleName":"公司","tableName":"gongsi"}]


var isAuth = function (tableName,key) {
    let role = localStorage.getItem("userTable");
    let menus = menu;
    for(let i=0;i<menus.length;i++){
        if(menus[i].tableName==role){
            for(let j=0;j<menus[i].backMenu.length;j++){
                for(let k=0;k<menus[i].backMenu[j].child.length;k++){
                    if(tableName==menus[i].backMenu[j].child[k].tableName){
                        let buttons = menus[i].backMenu[j].child[k].buttons.join(',');
                        return buttons.indexOf(key) !== -1 || false
                    }
                }
            }
        }
    }
    return false;
}

var isFrontAuth = function (tableName,key) {
    let role = localStorage.getItem("userTable");
    let menus = menu;
    for(let i=0;i<menus.length;i++){
        if(menus[i].tableName==role){
            for(let j=0;j<menus[i].frontMenu.length;j++){
                for(let k=0;k<menus[i].frontMenu[j].child.length;k++){
                    if(tableName==menus[i].frontMenu[j].child[k].tableName){
                        let buttons = menus[i].frontMenu[j].child[k].buttons.join(',');
                        return buttons.indexOf(key) !== -1 || false
                    }
                }
            }
        }
    }
    return false;
}
