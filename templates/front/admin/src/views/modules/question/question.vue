<template>
  <el-row>
    <el-col :span="12">
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="题目ID">
          <el-input v-model="form.name" placeholder="输入题目ID或内容"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">搜索</el-button><el-button type="primary" @click="onAdd">添加题目</el-button>
        </el-form-item>
      </el-form>
    </el-col>

    <el-col :span="24">
      <el-table
          :data="tableData"
          border
          style="width: 100%">
        <el-table-column
            prop="id"
            align="center"
            label="ID"
            width="50">
        </el-table-column>
        <el-table-column
            prop="sid"
            align="center"
            label="科目"
            width="100">
        </el-table-column>
        <el-table-column
            prop="version"
            align="center"
            label="版本" width="100">
        </el-table-column>
        <el-table-column
            prop="level"
            align="center"
            label="级别" width="100">
        </el-table-column>
        <el-table-column
            prop="title"
            align="center"
            label="题目标题">
        </el-table-column>
        <el-table-column
            prop="content"
            width="300"
            align="center"
            label="题目描述">
        </el-table-column>
        <el-table-column
            prop="status"
            width="100"
            align="center"
            label="状态">
        </el-table-column>
        <el-table-column
            prop=""
            width="100"
            align="center"
            label="操作">
          <template :slot-scope="scope">
            <el-button type="text" size="small">编辑</el-button>
            <el-button type="text" size="small" style="color: red">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

    </el-col>
  </el-row>

</template>

<script>
export default {
  data() {
    return {
      form: {
        name: ''
      },
      tableData: []
    }
  },
  mounted() {

  },
  created() {
    this.onSubmit()
  },
  methods: {
    onSubmit: function () {
      this.$http.post(DOMAIN_API_SYS + "/tea/question_list/", this.form).then(res => {
          this.tableData = res.data.data;
      }).catch((res) => {
          this.$layer_message(res.result)
      }).finally(() => this.loading = false)
    }
    ,
    onAdd: function () {
      this.$router.replace({path: "/question/add/"});
    }


  }
}
</script>

<style scoped>

</style>