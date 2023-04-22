#coding:utf-8
__author__ = "ila"
from django.db import models

from .model import BaseModel

from datetime import datetime



class yonghu(BaseModel):
    __doc__ = u'''yonghu'''
    __tablename__ = 'yonghu'

    __loginUser__='yonghuzhanghao'


    __authTables__={}
    __authPeople__='是'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __loginUserColumn__='yonghuzhanghao'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    yonghuzhanghao=models.CharField ( max_length=255,null=False,unique=True, verbose_name='用户账号' )
    mima=models.CharField ( max_length=255,null=False, unique=False, verbose_name='密码' )
    yonghuxingming=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户姓名' )
    xingbie=models.CharField ( max_length=255, null=True, unique=False, verbose_name='性别' )
    shouji=models.CharField ( max_length=255,null=False, unique=False, verbose_name='手机' )
    youxiang=models.CharField ( max_length=255, null=True, unique=False, verbose_name='邮箱' )
    shenfenzheng=models.CharField ( max_length=255,null=False, unique=False, verbose_name='身份证' )
    zhaopian=models.CharField ( max_length=255, null=True, unique=False, verbose_name='照片' )
    biyeyuanxiao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='毕业院校' )
    xueli=models.CharField ( max_length=255, null=True, unique=False, verbose_name='学历' )
    zhuanye=models.CharField ( max_length=255, null=True, unique=False, verbose_name='专业' )
    '''
    yonghuzhanghao=VARCHAR
    mima=VARCHAR
    yonghuxingming=VARCHAR
    xingbie=VARCHAR
    shouji=VARCHAR
    youxiang=VARCHAR
    shenfenzheng=VARCHAR
    zhaopian=VARCHAR
    biyeyuanxiao=VARCHAR
    xueli=VARCHAR
    zhuanye=VARCHAR
    '''
    class Meta:
        db_table = 'yonghu'
        verbose_name = verbose_name_plural = '用户'
class gongsi(BaseModel):
    __doc__ = u'''gongsi'''
    __tablename__ = 'gongsi'

    __loginUser__='gongsizhanghao'


    __authTables__={}
    __authPeople__='是'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __loginUserColumn__='gongsizhanghao'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='是'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    gongsizhanghao=models.CharField ( max_length=255,null=False,unique=True, verbose_name='公司账号' )
    mima=models.CharField ( max_length=255,null=False, unique=False, verbose_name='密码' )
    gongsimingcheng=models.CharField ( max_length=255, null=True, unique=False, verbose_name='公司名称' )
    zhucebianhao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='注册编号' )
    zhuceshijian=models.CharField ( max_length=255, null=True, unique=False, verbose_name='注册时间' )
    gongsidizhi=models.CharField ( max_length=255, null=True, unique=False, verbose_name='公司地址' )
    fuzerenxingming=models.CharField ( max_length=255, null=True, unique=False, verbose_name='负责人姓名' )
    xingbie=models.CharField ( max_length=255, null=True, unique=False, verbose_name='性别' )
    shenfenzheng=models.CharField ( max_length=255,null=False, unique=False, verbose_name='身份证' )
    shouji=models.CharField ( max_length=255,null=False, unique=False, verbose_name='手机' )
    youxiang=models.CharField ( max_length=255, null=True, unique=False, verbose_name='邮箱' )
    zhaopian=models.CharField ( max_length=255, null=True, unique=False, verbose_name='照片' )
    sfsh=models.CharField ( max_length=255, null=True, unique=False,default='否', verbose_name='是否审核' )
    shhf=models.TextField   (  null=True, unique=False, verbose_name='审核回复' )
    '''
    gongsizhanghao=VARCHAR
    mima=VARCHAR
    gongsimingcheng=VARCHAR
    zhucebianhao=VARCHAR
    zhuceshijian=VARCHAR
    gongsidizhi=VARCHAR
    fuzerenxingming=VARCHAR
    xingbie=VARCHAR
    shenfenzheng=VARCHAR
    shouji=VARCHAR
    youxiang=VARCHAR
    zhaopian=VARCHAR
    sfsh=VARCHAR
    shhf=Text
    '''
    class Meta:
        db_table = 'gongsi'
        verbose_name = verbose_name_plural = '公司'
class zhaopinxinxi(BaseModel):
    __doc__ = u'''zhaopinxinxi'''
    __tablename__ = 'zhaopinxinxi'



    __authTables__={'gongsizhanghao':'gongsi',}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    biaoti=models.CharField ( max_length=255, null=True, unique=False, verbose_name='标题' )
    chengshi=models.CharField ( max_length=255, null=True, unique=False, verbose_name='城市' )
    fabushijian=models.DateTimeField  (  null=True, unique=False, verbose_name='发布时间' )
    gongsizhanghao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='公司账号' )
    gongsimingcheng=models.CharField ( max_length=255, null=True, unique=False, verbose_name='公司名称' )
    zhucebianhao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='注册编号' )
    zhaopingangwei=models.CharField ( max_length=255, null=True, unique=False, verbose_name='招聘岗位' )
    gangweileixing=models.CharField ( max_length=255, null=True, unique=False, verbose_name='岗位类型' )
    zhaopinrenshu=models.IntegerField  (  null=True, unique=False, verbose_name='招聘人数' )
    gangweidaiyu=models.CharField ( max_length=255, null=True, unique=False, verbose_name='岗位待遇' )
    gangweiyaoqiu=models.TextField   (  null=True, unique=False, verbose_name='岗位要求' )
    fengmian=models.CharField ( max_length=255, null=True, unique=False, verbose_name='封面' )
    gongsijieshao=models.TextField   (  null=True, unique=False, verbose_name='公司介绍' )
    '''
    biaoti=VARCHAR
    chengshi=VARCHAR
    fabushijian=DateTime
    gongsizhanghao=VARCHAR
    gongsimingcheng=VARCHAR
    zhucebianhao=VARCHAR
    zhaopingangwei=VARCHAR
    gangweileixing=VARCHAR
    zhaopinrenshu=Integer
    gangweidaiyu=VARCHAR
    gangweiyaoqiu=Text
    fengmian=VARCHAR
    gongsijieshao=Text
    '''
    class Meta:
        db_table = 'zhaopinxinxi'
        verbose_name = verbose_name_plural = '招聘信息'
class toudijilu(BaseModel):
    __doc__ = u'''toudijilu'''
    __tablename__ = 'toudijilu'



    __authTables__={'yonghuzhanghao':'yonghu','gongsizhanghao':'gongsi',}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='前要登'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    yonghuzhanghao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户账号' )
    yonghuxingming=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户姓名' )
    biyeyuanxiao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='毕业院校' )
    xueli=models.CharField ( max_length=255, null=True, unique=False, verbose_name='学历' )
    zhuanye=models.CharField ( max_length=255, null=True, unique=False, verbose_name='专业' )
    toudishijian=models.DateTimeField  (  null=True, unique=False, verbose_name='投递时间' )
    biaoti=models.CharField ( max_length=255, null=True, unique=False, verbose_name='标题' )
    zhaopingangwei=models.CharField ( max_length=255, null=True, unique=False, verbose_name='招聘岗位' )
    gongsizhanghao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='公司账号' )
    gongsimingcheng=models.CharField ( max_length=255, null=True, unique=False, verbose_name='公司名称' )
    gangweidaiyu=models.CharField ( max_length=255, null=True, unique=False, verbose_name='岗位待遇' )
    gangweiyaoqiu=models.CharField ( max_length=255, null=True, unique=False, verbose_name='岗位要求' )
    wenjianmingcheng=models.CharField ( max_length=255, null=True, unique=False, verbose_name='文件名称' )
    jianli=models.CharField ( max_length=255, null=True, unique=False, verbose_name='简历' )
    jianyaojieshao=models.TextField   (  null=True, unique=False, verbose_name='简要介绍' )
    '''
    yonghuzhanghao=VARCHAR
    yonghuxingming=VARCHAR
    biyeyuanxiao=VARCHAR
    xueli=VARCHAR
    zhuanye=VARCHAR
    toudishijian=DateTime
    biaoti=VARCHAR
    zhaopingangwei=VARCHAR
    gongsizhanghao=VARCHAR
    gongsimingcheng=VARCHAR
    gangweidaiyu=VARCHAR
    gangweiyaoqiu=VARCHAR
    wenjianmingcheng=VARCHAR
    jianli=VARCHAR
    jianyaojieshao=Text
    '''
    class Meta:
        db_table = 'toudijilu'
        verbose_name = verbose_name_plural = '投递记录'
class dafenjilu(BaseModel):
    __doc__ = u'''dafenjilu'''
    __tablename__ = 'dafenjilu'



    __authTables__={'yonghuzhanghao':'yonghu','gongsizhanghao':'gongsi',}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='前要登'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    dafen=models.CharField ( max_length=255, null=True, unique=False, verbose_name='打分' )
    shuoming=models.TextField   (  null=True, unique=False, verbose_name='说明' )
    yonghuzhanghao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户账号' )
    yonghuxingming=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户姓名' )
    gongsizhanghao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='公司账号' )
    gongsimingcheng=models.CharField ( max_length=255, null=True, unique=False, verbose_name='公司名称' )
    shijian=models.DateTimeField  (  null=True, unique=False, verbose_name='时间' )
    '''
    dafen=VARCHAR
    shuoming=Text
    yonghuzhanghao=VARCHAR
    yonghuxingming=VARCHAR
    gongsizhanghao=VARCHAR
    gongsimingcheng=VARCHAR
    shijian=DateTime
    '''
    class Meta:
        db_table = 'dafenjilu'
        verbose_name = verbose_name_plural = '打分记录'
class tousujilu(BaseModel):
    __doc__ = u'''tousujilu'''
    __tablename__ = 'tousujilu'



    __authTables__={'gongsizhanghao':'gongsi','yonghuzhanghao':'yonghu',}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='前要登'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    shijian=models.DateTimeField  (  null=True, unique=False, verbose_name='时间' )
    tousuneirong=models.TextField   (  null=True, unique=False, verbose_name='投诉内容' )
    gongsizhanghao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='公司账号' )
    gongsimingcheng=models.CharField ( max_length=255, null=True, unique=False, verbose_name='公司名称' )
    yonghuzhanghao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户账号' )
    yonghuxingming=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户姓名' )
    '''
    shijian=DateTime
    tousuneirong=Text
    gongsizhanghao=VARCHAR
    gongsimingcheng=VARCHAR
    yonghuzhanghao=VARCHAR
    yonghuxingming=VARCHAR
    '''
    class Meta:
        db_table = 'tousujilu'
        verbose_name = verbose_name_plural = '投诉记录'
class gerenjianli(BaseModel):
    __doc__ = u'''gerenjianli'''
    __tablename__ = 'gerenjianli'



    __authTables__={'yonghuzhanghao':'yonghu',}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='前要登'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    yonghuzhanghao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户账号' )
    yonghuxingming=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户姓名' )
    biyeyuanxiao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='毕业院校' )
    xueli=models.CharField ( max_length=255, null=True, unique=False, verbose_name='学历' )
    zhuanye=models.CharField ( max_length=255, null=True, unique=False, verbose_name='专业' )
    wenjianmingcheng=models.CharField ( max_length=255, null=True, unique=False, verbose_name='文件名称' )
    jianli=models.CharField ( max_length=255, null=True, unique=False, verbose_name='简历' )
    jianyaojieshao=models.TextField   (  null=True, unique=False, verbose_name='简要介绍' )
    '''
    yonghuzhanghao=VARCHAR
    yonghuxingming=VARCHAR
    biyeyuanxiao=VARCHAR
    xueli=VARCHAR
    zhuanye=VARCHAR
    wenjianmingcheng=VARCHAR
    jianli=VARCHAR
    jianyaojieshao=Text
    '''
    class Meta:
        db_table = 'gerenjianli'
        verbose_name = verbose_name_plural = '个人简历'
class gangweiyaoqing(BaseModel):
    __doc__ = u'''gangweiyaoqing'''
    __tablename__ = 'gangweiyaoqing'



    __authTables__={'yonghuzhanghao':'yonghu','gongsizhanghao':'gongsi',}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    yonghuzhanghao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户账号' )
    yonghuxingming=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户姓名' )
    gongsizhanghao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='公司账号' )
    gongsimingcheng=models.CharField ( max_length=255, null=True, unique=False, verbose_name='公司名称' )
    gongsidizhi=models.CharField ( max_length=255, null=True, unique=False, verbose_name='公司地址' )
    zhucebianhao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='注册编号' )
    yaoqinggangwei=models.CharField ( max_length=255, null=True, unique=False, verbose_name='邀请岗位' )
    gangweidaiyu=models.CharField ( max_length=255, null=True, unique=False, verbose_name='岗位待遇' )
    shijian=models.DateTimeField  (  null=True, unique=False, verbose_name='时间' )
    '''
    yonghuzhanghao=VARCHAR
    yonghuxingming=VARCHAR
    gongsizhanghao=VARCHAR
    gongsimingcheng=VARCHAR
    gongsidizhi=VARCHAR
    zhucebianhao=VARCHAR
    yaoqinggangwei=VARCHAR
    gangweidaiyu=VARCHAR
    shijian=DateTime
    '''
    class Meta:
        db_table = 'gangweiyaoqing'
        verbose_name = verbose_name_plural = '岗位邀请'
class liaotianjilu(BaseModel):
    __doc__ = u'''liaotianjilu'''
    __tablename__ = 'liaotianjilu'



    __authTables__={'yonghuzhanghao':'yonghu','gongsizhanghao':'gongsi',}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    shijian=models.DateTimeField  (  null=True, unique=False, verbose_name='时间' )
    neirong=models.TextField   (  null=True, unique=False, verbose_name='内容' )
    yonghuzhanghao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户账号' )
    yonghuxingming=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户姓名' )
    gongsizhanghao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='公司账号' )
    gongsimingcheng=models.CharField ( max_length=255, null=True, unique=False, verbose_name='公司名称' )
    '''
    shijian=DateTime
    neirong=Text
    yonghuzhanghao=VARCHAR
    yonghuxingming=VARCHAR
    gongsizhanghao=VARCHAR
    gongsimingcheng=VARCHAR
    '''
    class Meta:
        db_table = 'liaotianjilu'
        verbose_name = verbose_name_plural = '聊天记录'
class rencaiku(BaseModel):
    __doc__ = u'''rencaiku'''
    __tablename__ = 'rencaiku'



    __authTables__={'yonghuzhanghao':'yonghu','gongsizhanghao':'gongsi',}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    yonghuzhanghao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户账号' )
    yonghuxingming=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户姓名' )
    biyeyuanxiao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='毕业院校' )
    xueli=models.CharField ( max_length=255, null=True, unique=False, verbose_name='学历' )
    zhuanye=models.CharField ( max_length=255, null=True, unique=False, verbose_name='专业' )
    jianli=models.CharField ( max_length=255, null=True, unique=False, verbose_name='简历' )
    jianyaojieshao=models.TextField   (  null=True, unique=False, verbose_name='简要介绍' )
    gongsizhanghao=models.CharField ( max_length=255, null=True, unique=False, verbose_name='公司账号' )
    gongsimingcheng=models.CharField ( max_length=255, null=True, unique=False, verbose_name='公司名称' )
    cunrushijian=models.DateTimeField  (  null=True, unique=False, verbose_name='存入时间' )
    '''
    yonghuzhanghao=VARCHAR
    yonghuxingming=VARCHAR
    biyeyuanxiao=VARCHAR
    xueli=VARCHAR
    zhuanye=VARCHAR
    jianli=VARCHAR
    jianyaojieshao=Text
    gongsizhanghao=VARCHAR
    gongsimingcheng=VARCHAR
    cunrushijian=DateTime
    '''
    class Meta:
        db_table = 'rencaiku'
        verbose_name = verbose_name_plural = '人才库'
class chengshi(BaseModel):
    __doc__ = u'''chengshi'''
    __tablename__ = 'chengshi'



    __authTables__={}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    chengshi=models.CharField ( max_length=255, null=True, unique=False, verbose_name='城市' )
    '''
    chengshi=VARCHAR
    '''
    class Meta:
        db_table = 'chengshi'
        verbose_name = verbose_name_plural = '城市'
class gangweifenlei(BaseModel):
    __doc__ = u'''gangweifenlei'''
    __tablename__ = 'gangweifenlei'



    __authTables__={}
    __authPeople__='否'#用户表，表属性loginUserColumn对应的值就是用户名字段，mima就是密码字段
    __sfsh__='否'#表sfsh(是否审核，”是”或”否”)字段和sfhf(审核回复)字段，后台列表(page)的操作中要多一个”审核”按钮，点击”审核”弹出一个页面，包含”是否审核”和”审核回复”，点击确定调用update接口，修改sfsh和sfhf两个字段。
    __authSeparate__='否'#后台列表权限
    __thumbsUp__='否'#表属性thumbsUp[是/否]，新增thumbsupnum赞和crazilynum踩字段
    __intelRecom__='否'#智能推荐功能(表属性：[intelRecom（是/否）],新增clicktime[前端不显示该字段]字段（调用info/detail接口的时候更新），按clicktime排序查询)
    __browseClick__='否'#表属性[browseClick:是/否]，点击字段（clicknum），调用info/detail接口的时候后端自动+1）、投票功能（表属性[vote:是/否]，投票字段（votenum）,调用vote接口后端votenum+1
    __foreEndListAuth__='否'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    __foreEndList__='否'#表属性[foreEndList]前台list:和后台默认的list列表页相似,只是摆在前台,否:指没有此页,是:表示有此页(不需要登陆即可查看),前要登:表示有此页且需要登陆后才能查看
    __isAdmin__='否'#表属性isAdmin=”是”,刷出来的用户表也是管理员，即page和list可以查看所有人的考试记录(同时应用于其他表)
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    gangweileixing=models.CharField ( max_length=255, null=True, unique=False, verbose_name='岗位类型' )
    '''
    gangweileixing=VARCHAR
    '''
    class Meta:
        db_table = 'gangweifenlei'
        verbose_name = verbose_name_plural = '岗位分类'
class chat(BaseModel):
    __doc__ = u'''chat'''
    __tablename__ = 'chat'



    __authTables__={}
    __foreEndListAuth__='是'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    userid=models.BigIntegerField  ( null=False, unique=False, verbose_name='用户id' )
    adminid=models.BigIntegerField  (  null=True, unique=False, verbose_name='管理员id' )
    ask=models.TextField   (  null=True, unique=False, verbose_name='提问' )
    reply=models.TextField   (  null=True, unique=False, verbose_name='回复' )
    isreply=models.IntegerField  (  null=True, unique=False, verbose_name='是否回复' )
    '''
    userid=BigInteger
    adminid=BigInteger
    ask=Text
    reply=Text
    isreply=Integer
    '''
    class Meta:
        db_table = 'chat'
        verbose_name = verbose_name_plural = '客服咨询'
class storeup(BaseModel):
    __doc__ = u'''storeup'''
    __tablename__ = 'storeup'



    __authTables__={}
    __authSeparate__='是'#后台列表权限
    __foreEndListAuth__='是'#前台列表权限foreEndListAuth[是/否]；当foreEndListAuth=是，刷的表新增用户字段userid，前台list列表接口仅能查看自己的记录和add接口后台赋值userid的值
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    userid=models.BigIntegerField  ( null=False, unique=False, verbose_name='用户id' )
    refid=models.BigIntegerField  (  null=True, unique=False, verbose_name='收藏id' )
    tablename=models.CharField ( max_length=255, null=True, unique=False, verbose_name='表名' )
    name=models.CharField ( max_length=255,null=False, unique=False, verbose_name='收藏名称' )
    picture=models.CharField ( max_length=255,null=False, unique=False, verbose_name='收藏图片' )
    type=models.CharField ( max_length=255, null=True, unique=False,default='1', verbose_name='类型(1:收藏,21:赞,22:踩)' )
    inteltype=models.CharField ( max_length=255, null=True, unique=False, verbose_name='推荐类型' )
    '''
    userid=BigInteger
    refid=BigInteger
    tablename=VARCHAR
    name=VARCHAR
    picture=VARCHAR
    type=VARCHAR
    inteltype=VARCHAR
    '''
    class Meta:
        db_table = 'storeup'
        verbose_name = verbose_name_plural = '收藏表'
class news(BaseModel):
    __doc__ = u'''news'''
    __tablename__ = 'news'



    __authTables__={}
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    title=models.CharField ( max_length=255,null=False, unique=False, verbose_name='标题' )
    introduction=models.TextField   (  null=True, unique=False, verbose_name='简介' )
    picture=models.CharField ( max_length=255,null=False, unique=False, verbose_name='图片' )
    content=models.TextField   ( null=False, unique=False, verbose_name='内容' )
    '''
    title=VARCHAR
    introduction=Text
    picture=VARCHAR
    content=Text
    '''
    class Meta:
        db_table = 'news'
        verbose_name = verbose_name_plural = '新闻资讯'
class discusszhaopinxinxi(BaseModel):
    __doc__ = u'''discusszhaopinxinxi'''
    __tablename__ = 'discusszhaopinxinxi'



    __authTables__={}
    addtime = models.DateTimeField(auto_now_add=False, verbose_name=u'创建时间')
    refid=models.BigIntegerField  ( null=False, unique=False, verbose_name='关联表id' )
    userid=models.BigIntegerField  ( null=False, unique=False, verbose_name='用户id' )
    nickname=models.CharField ( max_length=255, null=True, unique=False, verbose_name='用户名' )
    content=models.TextField   ( null=False, unique=False, verbose_name='评论内容' )
    reply=models.TextField   (  null=True, unique=False, verbose_name='回复内容' )
    '''
    refid=BigInteger
    userid=BigInteger
    nickname=VARCHAR
    content=Text
    reply=Text
    '''
    class Meta:
        db_table = 'discusszhaopinxinxi'
        verbose_name = verbose_name_plural = '招聘信息评论表'
