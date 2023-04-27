<template>
  <el-row>
    <el-col :span="12">
      <el-form ref="form" :model="form" label-width="120px">
        <el-form-item label="题目ID：">
          <el-input v-model="form.id" disabled></el-input>
        </el-form-item>
        <el-form-item label="科目：">
          <el-radio-group v-model="form.sid">
            <el-radio label="1" value="1">K8s</el-radio>
            <el-radio label="2" value="2">Mysql</el-radio>
            <el-radio label="3" value="3">Vue</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="版本：">
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
        <el-form-item label="题目标题：">
          <el-input v-model="form.title"></el-input>
        </el-form-item>
        <el-form-item label="题目描述：" prop="desc">
          <el-input type="textarea" v-model="form.content"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">保存</el-button>

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
      form: {
        id: 0,
        sid: "1",
        version: '',
        level: "1",
        title: "",
        content: "",
        size: "1",
        add_user: this.$storage.get("userId")
      },

    }
  },
  mounted() {

  },
  created() {

  },
  methods: {
    onSubmit: function () {
      this.$http.post(DOMAIN_API_SYS + "/tea/question/", this.form).then(res => {
      this.$message({
					       message: "操作成功",
					       type: "success",
					       duration: 1500,
					     });
      this.$router.replace({path: "/question"});
      }).catch((res) => {
                  this.$layer_message(res.result)
              }).finally(() => this.loading = false)
    }
  }
}
</script>

<style scoped>

</style>