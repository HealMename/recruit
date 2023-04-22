import Vue from 'vue';
//配置路由
import VueRouter from 'vue-router'
Vue.use(VueRouter);
//1.创建组件
import Index from '@/views/index'
import Home from '@/views/home'
import Login from '@/views/login'
import NotFound from '@/views/404'
import UpdatePassword from '@/views/update-password'
import pay from '@/views/pay'
import register from '@/views/register'
import center from '@/views/center'
    import news from '@/views/modules/news/list'
    import gongsi from '@/views/modules/gongsi/list'
    import rencaiku from '@/views/modules/rencaiku/list'
    import liaotianjilu from '@/views/modules/liaotianjilu/list'
    import chengshi from '@/views/modules/chengshi/list'
    import discusszhaopinxinxi from '@/views/modules/discusszhaopinxinxi/list'
    import zhaopinxinxi from '@/views/modules/zhaopinxinxi/list'
    import gangweiyaoqing from '@/views/modules/gangweiyaoqing/list'
    import gerenjianli from '@/views/modules/gerenjianli/list'
    import yonghu from '@/views/modules/yonghu/list'
    import chat from '@/views/modules/chat/list'
    import gangweifenlei from '@/views/modules/gangweifenlei/list'
    import dafenjilu from '@/views/modules/dafenjilu/list'
    import tousujilu from '@/views/modules/tousujilu/list'
    import toudijilu from '@/views/modules/toudijilu/list'
    import config from '@/views/modules/config/list'


//2.配置路由   注意：名字
const routes = [{
    path: '/index',
    name: '首页',
    component: Index,
    children: [{
      // 这里不设置值，是把main作为默认页面
      path: '/',
      name: '首页',
      component: Home,
      meta: {icon:'', title:'center'}
    }, {
      path: '/updatePassword',
      name: '修改密码',
      component: UpdatePassword,
      meta: {icon:'', title:'updatePassword'}
    }, {
      path: '/pay',
      name: '支付',
      component: pay,
      meta: {icon:'', title:'pay'}
    }, {
      path: '/center',
      name: '个人信息',
      component: center,
      meta: {icon:'', title:'center'}
    }
      ,{
	path: '/news',
        name: '新闻资讯',
        component: news
      }
      ,{
	path: '/gongsi',
        name: '公司',
        component: gongsi
      }
      ,{
	path: '/rencaiku',
        name: '人才库',
        component: rencaiku
      }
      ,{
	path: '/liaotianjilu',
        name: '聊天记录',
        component: liaotianjilu
      }
      ,{
	path: '/chengshi',
        name: '城市',
        component: chengshi
      }
      ,{
	path: '/discusszhaopinxinxi',
        name: '招聘信息评论',
        component: discusszhaopinxinxi
      }
      ,{
	path: '/zhaopinxinxi',
        name: '招聘信息',
        component: zhaopinxinxi
      }
      ,{
	path: '/gangweiyaoqing',
        name: '岗位邀请',
        component: gangweiyaoqing
      }
      ,{
	path: '/gerenjianli',
        name: '个人简历',
        component: gerenjianli
      }
      ,{
	path: '/yonghu',
        name: '用户',
        component: yonghu
      }
      ,{
	path: '/chat',
        name: '客服咨询',
        component: chat
      }
      ,{
	path: '/gangweifenlei',
        name: '岗位分类',
        component: gangweifenlei
      }
      ,{
	path: '/dafenjilu',
        name: '打分记录',
        component: dafenjilu
      }
      ,{
	path: '/tousujilu',
        name: '投诉记录',
        component: tousujilu
      }
      ,{
	path: '/toudijilu',
        name: '投递记录',
        component: toudijilu
      }
      ,{
	path: '/config',
        name: '轮播图管理',
        component: config
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: {icon:'', title:'login'}
  },
  {
    path: '/register',
    name: 'register',
    component: register,
    meta: {icon:'', title:'register'}
  },
  {
    path: '/',
    name: '首页',
    redirect: '/index'
  }, /*默认跳转路由*/
  {
    path: '*',
    component: NotFound
  }
]
//3.实例化VueRouter  注意：名字
const router = new VueRouter({
  mode: 'hash',
  /*hash模式改为history*/
  routes // （缩写）相当于 routes: routes
})

export default router;
