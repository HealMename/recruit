<template>
  <el-row>
    <el-col :span="12">
      <el-form ref="form" :model="form" label-width="100px">
        <el-form-item label="做题记录ID">
          <el-input v-model="form.id" placeholder=""></el-input>
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="form.phone" placeholder=""></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit(1)">搜索</el-button>
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
            width="150">
        </el-table-column>
        <el-table-column
            prop="phone"
            align="center"
            label="手机号"
            width="200">
        </el-table-column>
      <el-table-column
            prop="name"
            align="center"
            label="姓名"
            >
        </el-table-column>
        <el-table-column
            prop="add_time"
            width="180"
            align="center"
            label="添加时间">
        </el-table-column>
        <el-table-column
            prop=""
            width="200"
            align="center"
            label="操作">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="onAdd(scope.row.id)">查看详情</el-button>
            <el-button type="text" size="small" style="color: red" @click="delQ(scope.row.id)">删除记录</el-button>
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
      this.$http.post(DOMAIN_API_SYS + "/user/test_list/", this.form).then(res => {
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