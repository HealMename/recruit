<template>
  <div>
    <el-form
        class="detail-form-content"
        ref="ruleForm"
        :model="ruleForm"
        label-width="80px"
        style="background: transparent;"
    >
      <el-row>
        <el-col :span="12">
          <el-form-item v-if="flag==='yonghu'" label="用户账号" prop="yonghuzhanghao">
            <el-input v-model="ruleForm.yonghuzhanghao" readonly placeholder="用户账号" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item v-if="flag==='yonghu'" label="用户姓名" prop="yonghuxingming">
            <el-input v-model="ruleForm.yonghuxingming" placeholder="用户姓名" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item v-if="flag==='yonghu'" label="性别" prop="xingbie">
            <el-select v-model="ruleForm.xingbie" placeholder="请选择性别">
              <el-option
                  v-for="(item,index) in yonghuxingbieOptions"
                  v-bind:key="index"
                  :label="item"
                  :value="item">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item v-if="flag==='yonghu'" label="手机" prop="shouji">
            <el-input v-model="ruleForm.shouji" placeholder="手机" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item v-if="flag==='yonghu'" label="邮箱" prop="youxiang">
            <el-input v-model="ruleForm.youxiang" placeholder="邮箱" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item v-if="flag==='yonghu'" label="身份证" prop="shenfenzheng">
            <el-input v-model="ruleForm.shenfenzheng" placeholder="身份证" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="24">
          <el-form-item v-if="flag==='yonghu'" label="照片" prop="zhaopian">
            <file-upload
                tip="点击上传照片"
                action="file/upload"
                :limit="3"
                :multiple="true"
                :fileUrls="ruleForm.zhaopian?ruleForm.zhaopian:''"
                @change="yonghuzhaopianUploadChange"
            ></file-upload>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item v-if="flag==='yonghu'" label="毕业院校" prop="biyeyuanxiao">
            <el-input v-model="ruleForm.biyeyuanxiao" placeholder="毕业院校" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item v-if="flag==='yonghu'" label="学历" prop="xueli">
            <el-input v-model="ruleForm.xueli" placeholder="学历" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item v-if="flag==='yonghu'" label="专业" prop="zhuanye">
            <el-input v-model="ruleForm.zhuanye" placeholder="专业" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item v-if="flag==='gongsi'" label="公司账号" prop="gongsizhanghao">
            <el-input v-model="ruleForm.gongsizhanghao" readonly placeholder="公司账号" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item v-if="flag==='gongsi'" label="公司名称" prop="gongsimingcheng">
            <el-input v-model="ruleForm.gongsimingcheng" placeholder="公司名称" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item v-if="flag==='gongsi'" label="注册编号" prop="zhucebianhao">
            <el-input v-model="ruleForm.zhucebianhao" placeholder="注册编号" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item v-if="flag==='gongsi'" label="注册时间" prop="zhuceshijian">
            <el-input v-model="ruleForm.zhuceshijian" placeholder="注册时间" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item v-if="flag==='gongsi'" label="公司地址" prop="gongsidizhi">
            <el-input v-model="ruleForm.gongsidizhi" placeholder="公司地址" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item v-if="flag==='gongsi'" label="负责人姓名" prop="fuzerenxingming">
            <el-input v-model="ruleForm.fuzerenxingming" placeholder="负责人姓名" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item v-if="flag==='gongsi'" label="性别" prop="xingbie">
            <el-select v-model="ruleForm.xingbie" placeholder="请选择性别">
              <el-option
                  v-for="(item,index) in gongsixingbieOptions"
                  v-bind:key="index"
                  :label="item"
                  :value="item">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item v-if="flag==='gongsi'" label="身份证" prop="shenfenzheng">
            <el-input v-model="ruleForm.shenfenzheng" placeholder="身份证" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item v-if="flag==='gongsi'" label="手机" prop="shouji">
            <el-input v-model="ruleForm.shouji" placeholder="手机" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item v-if="flag==='gongsi'" label="邮箱" prop="youxiang">
            <el-input v-model="ruleForm.youxiang" placeholder="邮箱" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="24">
          <el-form-item v-if="flag==='gongsi'" label="照片" prop="zhaopian">
            <file-upload
                tip="点击上传照片"
                action="file/upload"
                :limit="3"
                :multiple="true"
                :fileUrls="ruleForm.zhaopian?ruleForm.zhaopian:''"
                @change="gongsizhaopianUploadChange"
            ></file-upload>
          </el-form-item>
        </el-col>
        <el-form-item v-if="flag==='users' && role === '管理员'" label="用户名" prop="username">
          <el-input v-model="ruleForm.username"
                    placeholder="用户名"></el-input>
        </el-form-item>

        <!--       教师 开始-->
        <el-form-item v-if="role === '教师'" label="用户名" prop="username">
          <el-input v-model="ruleForm.username"
                    placeholder="账号"></el-input>
        </el-form-item>

        <el-form-item v-if="role === '教师'" label="姓名" prop="name">
          <el-input v-model="ruleForm.name"
                    placeholder="姓名"></el-input>
        </el-form-item>

        <el-form-item v-if="role === '教师'" label="性别" prop="age">
          <el-select v-model="ruleForm.age" placeholder="请选择性别">
            <el-option label="男" :value="1">男</el-option>
            <el-option label="女" :value="2">女</el-option>
          </el-select>
        </el-form-item>

        <el-form-item v-if="role === '教师'" label="手机号" prop="phone_number">
          <el-input v-model="ruleForm.phone_number"
                    placeholder="手机号"></el-input>
        </el-form-item>

        <el-form-item v-if="role === '教师'" label="邮箱" prop="email">
          <el-input v-model="ruleForm.email"
                    placeholder="邮箱"></el-input>
        </el-form-item>


        <el-form-item v-if="role === '教师'" label="身份证" prop="number_id">
          <el-input v-model="ruleForm.number_id"
                    placeholder="身份证"></el-input>
        </el-form-item>
        <el-form-item v-if="role === '教师'" label="毕业院校" prop="school">
          <el-input v-model="ruleForm.school"
                    placeholder="毕业院校"></el-input>
        </el-form-item>

        <el-form-item v-if="role === '教师'" label="学历" prop="school_level">
          <el-select v-model="ruleForm.school_level" placeholder="请选择学历">
            <el-option label="大专" value="1">大专</el-option>
            <el-option label="本科" value="2">本科</el-option>
            <el-option label="硕士" value="3">硕士</el-option>
            <el-option label="博士" value="4">博士</el-option>
          </el-select>
        </el-form-item>

        <el-form-item v-if="role === '教师'" label="专业" prop="speciality">
          <el-input v-model="ruleForm.speciality"
                    placeholder="专业"></el-input>
        </el-form-item>

        <el-col :span="24">
          <el-form-item>
            <el-button type="primary" @click="onUpdateHandler">修 改</el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>
<script>
// 数字，邮件，手机，url，身份证校验
import {isNumber, isIntNumer, isEmail, isMobile, isPhone, isURL, checkIdCard} from "@/utils/validate";

export default {
  data() {
    return {
      ruleForm: {},
      flag: '',
      role: "",
      usersFlag: false,
      yonghuxingbieOptions: "男,女".split(','),
      gongsixingbieOptions: "男,女".split(','),
    };
  },
  mounted() {
    var table = this.$storage.get("sessionTable");
    this.role = this.$storage.get("role");
    this.flag = table;
    if (this.role === '教师') {
      this.$http.get(DOMAIN_API_SYS + "/tea/userinfo/?id=" + this.$storage.get("userId")).then(res => {
        console.log(res.data.data)
        this.ruleForm = res.data.data;
      })
    } else {
      this.$http({
        url: `${this.$storage.get("sessionTable")}/session?id=${this.$storage.get('userId')}`,
        method: "get"
      }).then(({data}) => {
        if (data && data.code === 0) {
          this.ruleForm = data.data;
        } else {
          this.$message.error(data.msg);
        }
      });
    }
  },
  methods: {
    yonghuzhaopianUploadChange(fileUrls) {
      this.ruleForm.zhaopian = fileUrls;
    },
    gongsizhaopianUploadChange(fileUrls) {
      this.ruleForm.zhaopian = fileUrls;
    },
    onUpdateHandler() {
      if (this.role === '教师') {
        this.$http.post(DOMAIN_API_SYS + '/tea/add/', this.ruleForm).then(res => {


        }).catch((res) => {
          this.$message({
            message: "修改信息成功",
            type: "success",
            duration: 1500,
            onClose: () => {
            }
          });
        }).finally(() => this.loading = false)
      } else {
        if ((!this.ruleForm.yonghuzhanghao) && 'yonghu' === this.flag) {
          this.$message.error('用户账号不能为空');
          return
        }
        if ((!this.ruleForm.mima) && 'yonghu' === this.flag) {
          this.$message.error('密码不能为空');
          return
        }
        if ((!this.ruleForm.shouji) && 'yonghu' === this.flag) {
          this.$message.error('手机不能为空');
          return
        }
        if ('yonghu' === this.flag && this.ruleForm.shouji && (!isMobile(this.ruleForm.shouji))) {
          this.$message.error(`手机应输入手机格式`);
          return
        }
        if ('yonghu' === this.flag && this.ruleForm.youxiang && (!isEmail(this.ruleForm.youxiang))) {
          this.$message.error(`邮箱应输入邮箱格式`);
          return
        }
        if ((!this.ruleForm.shenfenzheng) && 'yonghu' === this.flag) {
          this.$message.error('身份证不能为空');
          return
        }
        if ('yonghu' === this.flag && this.ruleForm.shenfenzheng && (!checkIdCard(this.ruleForm.shenfenzheng))) {
          this.$message.error(`身份证应输入身份证格式`);
          return
        }
        if (this.ruleForm.zhaopian != null) {
          this.ruleForm.zhaopian = this.ruleForm.zhaopian.replace(new RegExp(this.$base.url, "g"), "");
        }
        if ((!this.ruleForm.gongsizhanghao) && 'gongsi' === this.flag) {
          this.$message.error('公司账号不能为空');
          return
        }
        if ((!this.ruleForm.mima) && 'gongsi' === this.flag) {
          this.$message.error('密码不能为空');
          return
        }
        if ((!this.ruleForm.shenfenzheng) && 'gongsi' === this.flag) {
          this.$message.error('身份证不能为空');
          return
        }
        if ('gongsi' === this.flag && this.ruleForm.shenfenzheng && (!checkIdCard(this.ruleForm.shenfenzheng))) {
          this.$message.error(`身份证应输入身份证格式`);
          return
        }
        if ((!this.ruleForm.shouji) && 'gongsi' === this.flag) {
          this.$message.error('手机不能为空');
          return
        }
        if ('gongsi' === this.flag && this.ruleForm.shouji && (!isMobile(this.ruleForm.shouji))) {
          this.$message.error(`手机应输入手机格式`);
          return
        }
        if ('gongsi' === this.flag && this.ruleForm.youxiang && (!isEmail(this.ruleForm.youxiang))) {
          this.$message.error(`邮箱应输入邮箱格式`);
          return
        }
        if (this.ruleForm.zhaopian != null) {
          this.ruleForm.zhaopian = this.ruleForm.zhaopian.replace(new RegExp(this.$base.url, "g"), "");
        }
        if ('users' === this.flag && this.ruleForm.username.trim().length < 1) {
          this.$message.error(`用户名不能为空`);
          return
        }
        this.$http({
          url: `${this.$storage.get("sessionTable")}/update`,
          method: "post",
          data: this.ruleForm
        }).then(({data}) => {
          if (data && data.code === 0) {
            this.$message({
              message: "修改信息成功",
              type: "success",
              duration: 1500,
              onClose: () => {
              }
            });
          } else {
            this.$message.error(data.msg);
          }
        });
      }

    }
  }
};
</script>
<style lang="scss" scoped>
</style>
