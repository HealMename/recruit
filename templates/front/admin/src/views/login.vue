<template>
  <div>
    <div class="container loginIn">

      <div :class="2 == 1 ? 'left' : 2 == 2 ? 'left center' : 'left right'">
        <el-form class="login-form" label-position="left" :label-width="3 == 3 || 3 == 2 ? '60px': '0px'">
          <div class="title-container"><h3 class="title">it学霸登录</h3></div>
          <el-form-item label="">
            <el-input placeholder="账号" name="username" type="text" v-model="rulesForm.username"/>
          </el-form-item>
          <el-form-item label="">
            <el-input placeholder="密码" name="password" type="password" v-model="rulesForm.password"/>
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

export default {
  data() {
    return {
      type: this.$route.query.type,
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
    if (this.type === '1'){
      this.rulesForm.role = '管理员'
    }
    this.getRandCode()
  },
  methods: {
    register(tableName) {
      this.$storage.set("loginTable", tableName);
      this.$router.push({path: '/register'})
    },
    // 登陆
    login() {
      if (!this.rulesForm.username) {
        this.$message.error("请输入用户名");
        return;
      }
      if (!this.rulesForm.password) {
        this.$message.error("请输入密码");
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
      if (this.rulesForm.role === '出题专家' || this.rulesForm.role === '面试官'){
        url = `${DOMAIN_API_SYS}/tea/login/?username=${this.rulesForm.username}&password=${this.rulesForm.password}&role=${this.rulesForm.role}`
        this.$http.post(url, {}).then(res => {
          console.log(res)
                this.$storage.set("Token", res.data.token);
                this.$storage.set("userId", res.data.id);
              this.$storage.set("role", this.rulesForm.role);
              this.$storage.set("sessionTable", "users");
              this.$storage.set("adminName", this.rulesForm.username);
              window.location.href = `${this.$base.indexUrl}`
              }).catch((res) => {
                  this.$layer_message(res.result)
              }).finally(() => this.loading = false)

      }else{
        this.$http.post(url, {"role": this.rulesForm.role}).then(({data}) => {
          if (data && data.code === 0) {
            this.$storage.set("userId", data.id);
            this.$storage.set("Token", data.token);
            this.$storage.set("role", this.rulesForm.role);
            this.$storage.set("sessionTable", this.tableName);
            this.$storage.set("adminName", this.rulesForm.username);
            if (this.rulesForm.role === '管理员'){
              this.$router.replace({path: "/index/"});
            }else{
              window.location.href = `${this.$base.indexUrl}`
            }

          } else {
            this.$message.error(data.msg);
          }
        });
      }


    },
    getRandCode(len = 4) {
      this.randomString(len)
    },
    randomString(len = 4) {
      let chars = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
        "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
        "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G",
        "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
        "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2",
        "3", "4", "5", "6", "7", "8", "9"
      ]
      let colors = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
      let sizes = ['14', '15', '16', '17', '18']

      let output = [];
      for (let i = 0; i < len; i++) {
        // 随机验证码
        let key = Math.floor(Math.random() * chars.length)
        this.codes[i].num = chars[key]
        // 随机验证码颜色
        let code = '#'
        for (let j = 0; j < 6; j++) {
          let key = Math.floor(Math.random() * colors.length)
          code += colors[key]
        }
        this.codes[i].color = code
        // 随机验证码方向
        let rotate = Math.floor(Math.random() * 60)
        let plus = Math.floor(Math.random() * 2)
        if (plus == 1) rotate = '-' + rotate
        this.codes[i].rotate = 'rotate(' + rotate + 'deg)'
        // 随机验证码字体大小
        let size = Math.floor(Math.random() * sizes.length)
        this.codes[i].size = sizes[size] + 'px'
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
  background-image: url(http://182.42.126.254:8087/media/img/admin/login-bg.jpg);

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
    border-color: #6bc5a4;
    background-color: #6bc5a4;
    box-shadow: 0 0 6px rgba(255, 0, 0, .1);
    font-size: 23px;
  }

  .loginInBt:hover {
    background: #688ac2;
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
        border: 1px solid #eaeaec;
        background: #eaeaec;
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
        color: #00c292;
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
        border-color: #00c292;
        background-color: #00c292;
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
