<template>
  <el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="基本信息" name="first">
      <div>
        <el-form
            v-loading="loading"
            class="detail-form-content"
            ref="ruleForm"
            :model="ruleForm"
            label-width="120px"
            style="background: transparent;"
        >
          <el-form-item label="手机" prop="shouji">
            <el-input v-model="ruleForm.phone_number" placeholder="手机" clearable :disabled="true"></el-input> <el-button type="primary" icon="el-icon-edit" circle></el-button>
          </el-form-item>
          <el-form-item label="邮箱" prop="youxiang">
            <el-input v-model="ruleForm.youxiang" placeholder="邮箱" clearable :disabled="true"></el-input> <el-button type="primary" icon="el-icon-edit" circle></el-button>
          </el-form-item>
          <el-form-item label="姓名" prop="yonghuxingming">
            <el-input v-model="ruleForm.name" placeholder="用户姓名" clearable></el-input>
          </el-form-item>


          <el-form-item label="身份证(正面)" prop="zhaopian">
            <el-upload
                v-loading="loading"
                element-loading-text="拼命识别中"
                element-loading-spinner="el-icon-loading"
                class="avatar-uploader"
                :action="upload_url"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
                :before-upload="beforeAvatarUpload">
              <img v-if="ruleForm.form.imageUrl1" :src="ruleForm.form.imageUrl1" class="avatar">
              <i v-else class="el-icon-plus avatar-uploader-icon"></i>
            </el-upload>
          </el-form-item>
          <el-form-item label="身份证" prop="shenfenzheng">
            <el-input v-model="ruleForm.number_id" placeholder="身份证" clearable></el-input>
          </el-form-item>
          <el-form-item label="身份证(背面)" prop="zhaopian">
            <el-upload
                v-loading="loading"
                element-loading-text="拼命识别中"
                element-loading-spinner="el-icon-loading"
                class="avatar-uploader"
                :action="upload_url"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
                :before-upload="beforeAvatarUpload">
              <img v-if="ruleForm.form.imageUrl2" :src="ruleForm.form.imageUrl2" class="avatar">
              <i v-else class="el-icon-plus avatar-uploader-icon"></i>
            </el-upload>
          </el-form-item>



          <el-form-item>
            <el-button type="primary" @click="onUpdateHandler">修 改</el-button>
          </el-form-item>
        </el-form>
      </div>

    </el-tab-pane>
    <el-tab-pane label="学历信息" name="second">学历信息</el-tab-pane>
    <el-tab-pane label="工作经历" name="third">工作经历</el-tab-pane>
    <el-tab-pane label="其他" name="fourth">其他</el-tab-pane>
  </el-tabs>

</template>
<script>
// 数字，邮件，手机，url，身份证校验
import {isNumber, isIntNumer, isEmail, isMobile, isPhone, isURL, checkIdCard} from "@/utils/validate";

export default {
  data() {
    return {
      upload_url: "",
      activeName: "first",
      loading: false,
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
    this.loading = true;
    this.$http.get(DOMAIN_API_SYS + "/tea/userinfo/?id=" + this.$storage.get("userId")).then(res => {
      console.log(res.data.data)
      this.loading = false;
      this.ruleForm = res.data.data;
      this.upload_url = res.data.data.upload_url;
    })
  },
  methods: {
    // 上传验证
                beforeAvatarUpload(file) {
                    const isJPG = file.type === 'image/jpeg' || file.type === 'image/png';
                    const isLt2M = file.size / 1024 / 1024 < 2;

                    if (!isJPG) {
                        this.$message.error('上传图片只能是 JPG 或 png 格式!');
                    }
                    if (!isLt2M) {
                        this.$message.error('上传图片大小不能超过 2MB!');
                    }
                    return isJPG && isLt2M;
                },
    handleClick(tab, event) {
      console.log(tab, event);
    },
    // 识别身份证正面
    handleAvatarSuccess(res) {
      this.imageUrl1 = this.web_file_url + res.data[0].file_url
      this.loading = true;

    },
    yonghuzhaopianUploadChange(fileUrls) {
      this.ruleForm.zhaopian = fileUrls;
    },
    gongsizhaopianUploadChange(fileUrls) {
      this.ruleForm.zhaopian = fileUrls;
    },
    onUpdateHandler() {
      if (this.role === '出题专家') {
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
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 328px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.avatar {
  width: 328px;
  height: 178px;
  display: block;
}
</style>
