<template>
  <el-row>
    <el-col :span="12">
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="题目ID">
          <el-input v-model="form.id" placeholder="输入题目ID或内容"></el-input>
        </el-form-item>
        <el-form-item label="状态：" >
          <el-radio-group v-model="form.status">
            <el-radio label="" value="">全部</el-radio>
            <el-radio label="0" value="0">未审核</el-radio>
            <el-radio label="1" value="1">已审核</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button  @click="onSubmit(1)">搜索</el-button>
          <el-button  @click="onAdd(0)">添加题目</el-button>
        </el-form-item>
      </el-form>
    </el-col>

    <el-col :span="24">
      <el-table
          v-loading="loading"
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
            prop="sid_name"
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
            prop="level_name"
            align="center"
            label="级别" width="100">
        </el-table-column>
        <el-table-column
            prop="size_name"
            align="center"
            label="规模" width="100">
        </el-table-column>
        <el-table-column
            prop="title"
            align="center"
            label="题目标题">
        </el-table-column>
        <el-table-column
            prop="desc"
            width="300"
            align="desc"
            label="题目描述">
        </el-table-column>
        <el-table-column
            prop="status_name"
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
            <el-button type="text" size="small" @click="onAdd(scope.row.id)">编辑</el-button>
            <el-button type="text" size="small" style="color: red" @click="delQ(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

    </el-col>
    <el-col :span="24">
      <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[5, 10, 20, 50]"
          :page-size="page_size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total">
      </el-pagination>
    </el-col>

  </el-row>

</template>

<script>
export default {
  data() {
    return {
      loading: false,
      currentPage: 1,
      total: 0,
      page_size: 5,
      form: {
        id: '',
        status: '',
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
      this.form.page_id = page_id ? page_id: this.currentPage;
      this.form.page_size = this.page_size;
      this.loading = true;
      this.$http.post(DOMAIN_API_SYS + "/tea/question_list/", this.form).then(res => {
        let r = res.data.data
        this.tableData = r.page_data;
        this.total = r.sum_len
      }).catch((res) => {
        this.$layer_message(res.result)
      }).finally(() => this.loading = false)
    },
    onAdd: function (id_) {
      this.$router.replace({path: "/question/add/" + id_});
    },
    handleSizeChange: function (val) {
      this.page_size = val;
      this.onSubmit()
    },
    handleCurrentChange(val) {
      this.currentPage = val;
      this.onSubmit();
    },
    delQ(id_){
      this.loading = true;
      this.$http.post(DOMAIN_API_SYS + "/tea/del_q/", {id: id_, status: -1}).then(res => {
          this.$layer_message("已删除", 'success')
          this.onSubmit()
      }).catch((res) => {
        this.$layer_message(res.result)
      })
    },
  }
}
</script>

<style scoped>

</style>