<template>
  <el-row  v-loading="loading">
    <el-col :span="12">
      <el-button type="primary" @click="onAdd(0)">引用题目</el-button>
          <el-button type="primary" @click="go_bank">返回</el-button>
    </el-col>

    <el-dialog title="引用题目" :visible.sync="dialogFormVisible">
      <el-form :model="form_q">
        <el-form-item label="引用题目ID" label-width="200">
          <el-input v-model.number="form_q.id" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveQuestion()">确 定</el-button>
      </div>
    </el-dialog>

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
            prop="add_time"
            width="180"
            align="center"
            label="添加时间">
        </el-table-column>
        <el-table-column
            prop=""
            width="100"
            align="center"
            label="操作">
          <template slot-scope="scope">
            <el-button type="text" size="small" style="color: red" @click="delQ(scope.row.id)">移除</el-button>
          </template>
        </el-table-column>
      </el-table>

    </el-col>
    <el-col :span="24">

    </el-col>

  </el-row>

</template>

<script>
export default {
  data() {
    return {
      dialogFormVisible: false,
      id: this.$route.params.id,
      loading: false,
      currentPage: 1,
      total: 0,
      page_size: 5,
      form_q: {
        id: 0
      },
      form: {
        paper_id: this.$route.params.id,
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
    onSubmit: function (page_id) {
      this.loading = true;
      this.$http.post(DOMAIN_API_SYS + "/tea/paper_question/", this.form).then(res => {
        this.tableData = res.data.data.page_data;
      }).catch((res) => {
        this.$layer_message(res.result)
      }).finally(() => this.loading = false)
    },
    onAdd: function (id_) {
      this.dialogFormVisible = true
    },
    handleSizeChange: function (val) {
      this.page_size = val;
      this.onSubmit()
    },
    handleCurrentChange(val) {
      this.currentPage = val;
      this.onSubmit();
    },
    saveName(){
      this.loading = true;
      this.$http.post(DOMAIN_API_SYS + "/tea/save_paper_question/", this.form).then(res => {
          this.form.id = res.data.data
          this.$layer_message("已保存", 'success')
      }).catch((res) => {
        this.$layer_message(res.data.message)
      }).finally(() => this.loading = false)
    },
    saveQuestion() {
      this.loading = true;
      this.$http.post(DOMAIN_API_SYS + "/tea/save_paper_question/", {qid: this.form_q.id, ...this.form}).then(res => {
          this.form.id = res.data.data
          this.$layer_message("已添加", 'success')
          this.dialogFormVisible = false
          this.onSubmit()
      }).catch((res) => {
        this.$layer_message(res.data.message)
      }).finally(() => this.loading = false)
    },
    delQ(id_){
      this.loading = true;
      this.$http.post(DOMAIN_API_SYS + "/tea/del_p/", {id: id_, status: -1}).then(res => {
          this.$layer_message("已删除", 'success')
          this.onSubmit()
      }).catch((res) => {
        this.$layer_message(res.result)
      })
    },
    go_bank: function () {
      this.$router.replace({path: "/paper/"});
    },
  }
}
</script>

<style scoped>

</style>