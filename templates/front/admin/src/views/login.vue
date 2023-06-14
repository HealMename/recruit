<template>
  <div>
    <div class="container loginIn">

      <div :class="2 == 1 ? 'left' : 2 == 2 ? 'left center' : 'left right'">
        <el-form class="login-form" label-position="left" :label-width="3 == 3 || 3 == 2 ? '60px': '0px'">
          <div class="title-container"><h3 class="title">
            <img src="https://www.ittest008.com/file/number_id_img/2023/06/14/20230614061057325629.png" alt="">
          </h3></div>
          <el-form-item label="">
            <el-input placeholder="手机号" name="username" type="text" v-model="rulesForm.username"/>
          </el-form-item>
          <Vcode :show="isShow" @success="success" @close="close"/>
          <el-form-item label="">
            <div style="display: initial">
              <el-input style="float: left;width: 65%;" placeholder="短信验证码" name="password" type="text" maxlength="6"
                        v-model="rulesForm.password"/>
              <button type="button" class="btn btn-normal" id="getcode" @click="sendMessage()"
                      style="float: left;margin-left: 10px; background-color: #00a7d0; color: white;" :disabled="disabled">获取验证码
              </button>
            </div>

          </el-form-item>
          <el-form-item label="">
            <el-radio-group v-model="rulesForm.role">


              <el-radio
                  v-if="type !='1' && item.roleName !== '管理员'"
                  v-for="item in roles"
                  v-bind:key="item.roleName"
                  v-model="rulesForm.role"
                  :label="item.roleName"
              >{{ item.roleName }}
              </el-radio>

            </el-radio-group>
          </el-form-item>
          <el-form-item v-if="roles.length==1" label=" " prop="loginInRole" class="role"
                        style="display: flex;align-items: center;">
          </el-form-item>
          <el-button type="primary" @click="login()" class="loginInBt"><i class="glyphicon glyphicon-ok"></i>
          </el-button>
          <el-form-item class="setting">
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>
<script>

import menu from "@/utils/menu";

import Vcode from "vue-puzzle-vcode";

export default {
  components: {
    Vcode
  },
  data() {

    return {
      disabled: false,
      buttonDefaultValue: "获取验证码",
      type: this.$route.query.type,
      isShow: false,
      rulesForm: {
        username: "",
        password: "",
        role: "出题专家",
        code: '',
      },
      menus: [],
      roles: [],
      tableName: "",
      codes: [{
        num: 1,
        color: '#000',
        rotate: '10deg',
        size: '16px'
      }, {
        num: 2,
        color: '#000',
        rotate: '10deg',
        size: '16px'
      }, {
        num: 3,
        color: '#000',
        rotate: '10deg',
        size: '16px'
      }, {
        num: 4,
        color: '#000',
        rotate: '10deg',
        size: '16px'
      }],
    };
  },
  mounted() {
    let menus = menu.list();
    this.menus = menus;
    for (let i = 0; i < this.menus.length; i++) {
      if (this.menus[i].hasBackLogin == '是') {
        this.roles.push(this.menus[i])
      }
    }
  },
  created() {
    if (this.type === '1') {
      this.rulesForm.role = '管理员'
    }
  },
  methods: {
    countDown(obj, second) {
      // 如果秒数还是大于0，则表示倒计时还没结束
      var thsi = this;
      if (second >= 0) {
        this.disabled = true;

        // 按钮置为不可点击状态
        obj.disabled = true;
        this.$("#getcode").css('background-color', 'grey')
        // 按钮里的内容呈现倒计时状态
        this.$(obj).text(String(second) + '秒后重发');
        // 时间减一
        second--;
        // 一秒后重复执行
        setTimeout(function () {
          thsi.countDown(obj, second);
        }, 1000);
        // 否则，按钮重置为初始状态
      } else {
        // 按钮置未可点击状态
        obj.disabled = false;
        this.disabled = false;
        this.$("#getcode").css('background-color', '#00a7d0')
        // 按钮里的内容恢复初始状态
        obj.value = this.buttonDefaultValue;
      }
    },
    // 用户通过了验证
    success(msg) {
      var thsi = this;
      this.isShow = false; // 通过验证后，需要手动隐藏模态框
      // 发送验证码
      this.countDown(this.$('#getcode'), 60)

      this.$.post(DOMAIN_API_SYS + '/sms/send/', {phone: this.rulesForm.username, type: this.rulesForm.role, code_id: 2}, function (res) {
        if (res.response === 'ok'){
          thsi.$message.success('验证码已发送, 2分钟内有效')
        }else{
          thsi.$message.error(res.message)
        }

      })
    },
    close() {
      this.isShow = false;
    },
    sendMessage() {
      // 打开验证码弹窗
      if (!this.rulesForm.username) {
        this.$message.error("请输入账号");
        return;
      }
      this.isShow = true;
    },
    register(tableName) {
      this.$storage.set("loginTable", tableName);
      this.$router.push({path: '/register'})
    },
    // 登陆
    login() {
      // 用户点击遮罩层，应该关闭模态框

      if (!this.rulesForm.username) {
        this.$message.error("请输入用户名");
        return;
      }
      if (!this.rulesForm.password) {
        this.$message.error("请输入短信验证码");
        return;
      }
      if (this.roles.length > 1) {
        if (!this.rulesForm.role) {
          this.$message.error("请选择角色");
          return;
        }
        let menus = this.menus;
        for (let i = 0; i < menus.length; i++) {
          if (menus[i].roleName == this.rulesForm.role) {
            this.tableName = menus[i].tableName;
          }
        }
      } else {
        this.tableName = this.roles[0].tableName;
        this.rulesForm.role = this.roles[0].roleName;
      }
      let url = `${DOMAIN_API_SYS}/django7681v/${this.tableName}/login?username=${this.rulesForm.username}&password=${this.rulesForm.password}&role=${this.rulesForm.role}`
      // if (this.rulesForm.role === '出题专家' || this.rulesForm.role === '面试官') {
      if (url) {
        url = `${DOMAIN_API_SYS}/tea/login/?username=${this.rulesForm.username}&password=${this.rulesForm.password}&role=${this.rulesForm.role}`
        this.$http.post(url, {}).then(res => {
          console.log(res)
          this.$storage.set("Token", res.data.token);
          this.$storage.set("userId", res.data.id);
          this.$storage.set("role", this.rulesForm.role);
          this.$storage.set("sessionTable", this.tableName);
          this.$storage.set("adminName", this.rulesForm.username);
          if (this.rulesForm.role === '管理员') {
              this.$router.replace({path: "/index/"});
            } else {
              window.location.href = `${this.$base.indexUrl}`
            }
        }).catch((res) => {
          this.$layer_message(res.result)
        }).finally(() => this.loading = false)

      } else {
        // this.$http.post(url, {"role": this.rulesForm.role}).then(({data}) => {
        //   if (data && data.code === 0) {
        //     this.$storage.set("userId", data.id);
        //     this.$storage.set("Token", data.token);
        //     this.$storage.set("role", this.rulesForm.role);
        //     this.$storage.set("sessionTable", this.tableName);
        //     this.$storage.set("adminName", this.rulesForm.username);
        //     if (this.rulesForm.role === '管理员') {
        //       this.$router.replace({path: "/index/"});
        //     } else {
        //       window.location.href = `${this.$base.indexUrl}`
        //     }
        //
        //   } else {
        //     this.$message.error(data.msg);
        //   }
        // });
      }
    },
  }
};
</script>
<style lang="scss" scoped>
.loginIn {
  min-height: 100vh;
  position: relative;
  background-repeat: no-repeat;
  background-size: cover;
  width: 100%;
  height: 100%;
  background-image: url(https://www.ittest008.com/file/number_id_img/2023/06/14/20230614060328613832.jpg);

  .loginInBt {
    width: 100%;
    height: 44px;
    line-height: 44px;
    margin: 0;
    padding: 0;
    color: rgba(255, 255, 255, 1);
    font-size: 16px;
    border-radius: 5px;
    border-width: 0;
    border-style: solid;
    border-color: rgba(52, 128, 154, 0.8);
    background-color: rgba(52, 128, 154, 0.69);
    box-shadow: 0 0 6px rgba(255, 0, 0, .1);
    font-size: 23px;
  }

  .loginInBt:hover {
    background: rgb(52, 128, 154);
    -webkit-transition: all 0.3s;
    -moz-transition: all 0.3s;
    transition: all 0.3s;
  }

  .register {
    width: auto;
    height: 24px;
    line-height: 24px;
    margin: 10px 0 0 15%;
    padding: 0;
    color: rgba(242, 248, 184, 1);
    font-size: 12px;
    border-radius: 0;
    border-width: 0;
    border-style: solid;
    border-color: rgba(64, 158, 255, 1);
    background-color: rgba(255, 255, 255, 0);
    box-shadow: 0 0 6px rgba(255, 0, 0, 0);
    cursor: pointer;
  }

  .reset {
    width: auto;
    height: 24px;
    line-height: 24px;
    margin: 0;
    padding: 0;
    color: rgba(246, 247, 203, 1);
    font-size: 12px;
    border-radius: 0;
    border-width: 0;
    border-style: solid;
    border-color: rgb(247, 247, 247);
    background-color: rgba(255, 255, 255, 0);
    box-shadow: 0 0 6px rgba(255, 0, 0, 0);
  }


  .left {
    position: absolute;
    left: 0;
    top: 0;
    box-sizing: border-box;
    width: 370px;
    height: auto;
    margin: 0;
    padding: 0 12px;
    border-radius: 0;
    border-width: 0;
    border-style: solid;
    border-color: rgba(0, 0, 0, .3);
    background-color: #fff;

    .login-form {
      background-color: transparent;
      width: 100%;
      right: inherit;
      padding: 0;
      box-sizing: border-box;
      display: flex;
      position: initial;
      justify-content: center;
      flex-direction: column;
    }

    .title-container {
      text-align: center;
      font-size: 24px;

      .title {
        width: 100%;
        margin: 50px auto;
        padding: 0;
        font-size: 24px;
        border-radius: 0;
        border-width: 0;
        border-style: solid;
        border-color: rgba(0, 0, 0, .3);
        background-color: rgba(0, 0, 0, 0);
        box-shadow: 0 0 6px rgba(0, 0, 0, 0);
      }
    }

    .el-form-item {
      position: relative;

      & /deep/ .el-form-item__content {
        line-height: initial;
        margin-left: 0 !important;
      }

      & /deep/ .el-form-item__content input[type="text"], & /deep/ .el-form-item__content input[type="password"] {
        border-radius: 5px;
        -webkit-border-radius: 5px;
        border: 1px solid #c0c4cc;
        background: #ffffff;
        box-shadow: none;
        font-size: 12px;
      }

      & /deep/ .el-radio__label {
        width: auto;
        height: 14px;
        line-height: 14px;
        margin: 0;
        padding: 0 0 0 10px;
        font-size: 14px;
        border-radius: 0;
        border-width: 0;
        border-style: solid;
        border-color: rgba(255, 255, 255, 0);
        background-color: rgba(255, 255, 255, 0);
        box-shadow: 0 0 6px rgba(255, 0, 0, 0);
        text-align: left;
      }

      & /deep/ .el-radio.is-checked .el-radio__label {
        width: auto;
        height: 14px;
        line-height: 14px;
        margin: 0;
        padding: 0 0 0 10px;
        color: rgb(23, 70, 171);
        font-size: 14px;
        border-radius: 0;
        border-width: 0;
        border-style: solid;
        border-color: rgba(255, 255, 255, 0);
        background-color: rgba(255, 255, 255, 0);
        box-shadow: 0 0 6px rgba(255, 0, 0, 0);
        text-align: left;
      }

      & /deep/ .el-radio__inner {
        width: 14px;
        height: 14px;
        margin: 0;
        padding: 0;
        border-radius: 100%;
        border-width: 1px;
        border-style: solid;
        border-color: #dcdfe6;
        background-color: rgba(255, 255, 255, 1);
        box-shadow: 0 0 6px rgba(255, 0, 0, 0);
      }

      & /deep/ .el-radio.is-checked .el-radio__inner {
        width: 14px;
        height: 14px;
        margin: 0;
        padding: 0;
        border-radius: 100%;
        border-width: 1px;
        border-style: solid;
        border-color: #1746ab;
        background-color: #1746ab;
        box-shadow: 0 0 6px rgba(255, 0, 0, 0);
      }

      .svg-container {
        padding: 6px 5px 6px 15px;
        color: #889aa4;
        vertical-align: middle;
        display: inline-block;
        position: absolute;
        left: 0;
        top: 0;
        z-index: 1;
        padding: 0;
        line-height: 40px;
        width: 30px;
        text-align: center;
      }

      .el-input {
        display: inline-block;
        // height: 40px;
        width: 100%;

        & /deep/ input {
          //background: transparent;
          //border: 0px;
          //-webkit-appearance: none;
          //padding: 0 15px 0 30px;
          //color: #fff;
          //height: 40px;
          //
          //width: 100%;
          //height: 50px;
          //line-height: 50px;
          //margin: 0;
          //padding: 0 30px;
          //color: rgba(33, 30, 30, 1);
          //font-size: 16px;
          //border-radius: 15px;
          //border-width: 0;
          //border-style: solid;
          //border-color: rgba(0, 0, 0, 0);
          //background-color: rgba(73, 71, 71, 0.42);
          //box-shadow: 0 0 6px rgba(255, 0, 0, 0);
        }
      }

    }


  }

  .center {
    position: absolute;
    left: 50%;
    top: 30%;
    -webkit-border-radius: 5px;
    transform: translate3d(-50%, -50%, 0);
  }

  .right {
    position: absolute;
    left: inherit;
    right: 0;
    top: 0;
  }

  .code {
    .el-form-item__content {
      position: relative;

      .getCodeBt {
        position: absolute;
        right: 0;
        top: 50%;
        transform: translate3d(0, -50%, 0);
        line-height: 40px;
        width: 100px;
        background-color: rgba(51, 51, 51, 0.4);
        color: #fff;
        text-align: center;
        border-radius: 0 4px 4px 0;
        height: 40px;
        overflow: hidden;
        padding: 0;
        margin: 0;
        width: 100px;
        height: 30px;
        line-height: 30px;
        border-radius: 0;
        border-width: 0;
        border-style: solid;
        border-color: rgba(64, 158, 255, 1);
        background-color: rgba(51, 51, 51, 0.4);
        box-shadow: 0 0 6px rgba(255, 0, 0, 0);

        span {
          padding: 0 5px;
          display: inline-block;
          font-size: 16px;
          font-weight: 600;
        }
      }

      .el-input {
        & /deep/ input {
          padding: 0 130px 0 30px;
        }
      }
    }
  }

  .setting {
    & /deep/ .el-form-item__content {
      // padding: 0 15px;
      box-sizing: border-box;
      line-height: 32px;
      height: 32px;
      font-size: 14px;
      color: #999;
      margin: 0 !important;
      display: flex;

      .register {
        // float: left;
        // width: 50%;
        text-align: center;
      }

      .reset {
        float: right;
        width: 50%;
        text-align: right;
      }
    }
  }

  .style2 {
    padding-left: 30px;

    .svg-container {
      left: -60px !important;
    }

    .el-input {
      & /deep/ input {
        padding: 0 15px !important;
      }
    }
  }

  .code.style2, .code.style3 {
    .el-input {
      & /deep/ input {
        padding: 0 115px 0 15px;
      }
    }
  }

  .style3 {
    & /deep/ .el-form-item__label {
      padding-right: 6px;
      height: 50px;
      line-height: 50px;
    }

    .el-input {
      & /deep/ input {
        padding: 0 15px !important;
      }
    }
  }

  & /deep/ .el-form-item__label {
    width: 60px;
    height: 30px;
    line-height: 30px;
    margin: 0;
    padding: 0;
    color: rgba(136, 154, 164, 1);
    font-size: 14px;
    border-radius: 0;
    border-width: 0;
    border-style: solid;
    border-color: rgba(0, 0, 0, 0);
    background-color: rgba(0, 0, 0, 0);
    box-shadow: 0 0 6px rgba(0, 0, 0, 0);
  }

  .role {
    & /deep/ .el-form-item__label {
      width: 56px !important;
      height: 38px;
      line-height: 38px;
      margin: 0;
      padding: 0;
      color: rgba(101, 126, 253, 1);
      font-size: 14px;
      border-radius: 0;
      border-width: 0;
      border-style: solid;
      border-color: rgba(64, 158, 255, 1);
      background-color: rgba(255, 255, 255, 0);
      box-shadow: 0 0 6px rgba(255, 0, 0, 0);
      text-align: left;
    }

    & /deep/ .el-radio {
      margin-right: 12px;
    }
  }
}
</style>
