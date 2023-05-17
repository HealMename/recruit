<template>
  <el-row v-loading="loading">
    <el-col :span="12">
      <el-form ref="form" :model="form" label-width="120px" :rules="rules" >
        <el-form-item label="题目ID：">
          <el-input v-model="form.id" disabled></el-input>
        </el-form-item>
        <el-form-item label="状态："  v-if="role ==='管理员'">
          <el-radio-group v-model="form.status">
            <el-radio label="0" value="0">未审核</el-radio>
            <el-radio label="1" value="1">已审核</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="科目：">
          <el-radio-group v-model="form.sid">
            <el-radio label="1" value="1">K8s</el-radio>
            <el-radio label="2" value="2">Mysql</el-radio>
            <el-radio label="3" value="3">Vue</el-radio>
            <el-radio label="4" value="4">shell</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="版本：" prop="version">
          <el-input v-model="form.version"></el-input>
        </el-form-item>
        <el-form-item label="级别：">
          <el-radio-group v-model="form.level">
            <el-radio label="1" value="1">初级</el-radio>
            <el-radio label="2" value="2">中级</el-radio>
            <el-radio label="3" value="3">高级</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="规模：">
          <el-radio-group v-model="form.size">
            <el-radio label="1" value="1">单机</el-radio>
            <el-radio label="2" value="2">集群</el-radio>
            <el-radio label="3" value="3">多集群</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="做题时长(分)：" prop="do_time">
          <el-input v-model.number="form.do_time"></el-input>
        </el-form-item>
        <el-form-item label="考点：" prop="do_points">
          <el-input v-model="form.do_points"></el-input>
        </el-form-item>
        <el-form-item label="题目标题：" prop="title">
          <el-input v-model="form.title"></el-input>
        </el-form-item>
        <el-form-item label="题目描述：" prop="desc">
          <el-input type="textarea" v-model="form.desc"></el-input>
        </el-form-item>

        <el-form-item label="题目详情：" prop="content">
          <editor
                    style="min-width: 200px; max-width: 600px;"
                    v-model="form.content"
                    class="editor"
                    action="file/upload">
                </editor>
        </el-form-item>


        <el-form-item :label="'url' + (index+1)" v-for="(item,index) in form.urls" v-bind:key="index">
          <el-input v-model="item.value" v-bind:key="index" style="width: 92%"></el-input>
          <i class="el-icon-circle-plus-outline" style="padding-left: 12px;cursor:pointer;" @click="addUrl()" v-if="index+1 === 1"></i>
          <i class="el-icon-remove-outline" style="padding-left: 12px;cursor:pointer;" @click="delUrl(index)" v-if="index+1 > 1"></i>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit('form')">保存</el-button>
          <el-button type="primary" @click="go_bank">返回</el-button>

        </el-form-item>
      </el-form>
    </el-col>

    <el-col :span="24">


    </el-col>
  </el-row>

</template>

<script>
export default {
  data() {
    return {
      loading: false,
      role: this.$storage.get("role"),
      form: {
        urls: [{
          value: ''
        }],
        id: this.$route.params.id,
        sid: "1",
        do_time: 0,
        do_points: '',
        version: '',
        level: "1",
        title: "",
        content: "",
        desc: "",
        size: "1",
        add_user: this.$storage.get("userId"),

      },
      rules: {
        do_time: [{ required: true, message: '请输入做题时间', trigger: 'blur' }],
        version: [{ required: true, message: '请输入做题时间', trigger: 'blur' }],
        title: [{ required: true, message: '请输入做题时间', trigger: 'blur' }],
        do_points: [{ required: true, message: '请输入做题时间', trigger: 'blur' }],
        desc: [{ required: true, message: '请输入做题时间', trigger: 'blur' }],
        content: [{ required: true, message: '请输入做题时间', trigger: 'blur' }],
      }

    }
  },
  mounted() {

  },
  created() {
    console.log(this.role)
    if (this.form.id > 0){
        this.loading = true;
        this.$http.post(DOMAIN_API_SYS + "/tea/question_list/", {id: this.form.id}).then(res => {
          let r = res.data.data
          this.form = r.page_data[0]
          this.loading = false
      })
    }
  },
  methods: {
    go_bank: function () {
      this.$router.replace({path: "/question/"});
    },
    delUrl: function (index_) {
      this.$delete(this.form.urls, index_)
    },
    addUrl: function () {
      if (this.form.urls.length === 4){
          this.$layer_message("最多四个关联地址")
      }else{
        this.form.urls.push({value: ''})
      }
    },
    onSubmit: function (formName) {
       this.$refs[formName].validate((valid) => {
          if (valid) {

              this.$http.post(DOMAIN_API_SYS + "/tea/question/", this.form).then(res => {
                this.$layer_message('操作成功', 'success')
                this.$router.replace({path: "/question"});
              }).catch((res) => {
                this.$layer_message(res.result)
              }).finally(() => this.loading = false)
          } else {
            return false;
          }
        });
    },

  }
}
</script>

<style lang="css">
.editor{
  height: 500px;
  & /deep/ .ql-container {
	  height: 310px;
  }
}
</style>