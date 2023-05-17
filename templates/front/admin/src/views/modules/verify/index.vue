<template>
  <el-row>
    <el-col :span="12">
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="手机号">
          <el-input v-model="form.id" placeholder="输入用户ID或手机号"></el-input>
        </el-form-item>
        <el-form-item label="状态：" >
          <el-radio-group v-model="form.status">
            <el-radio label="" value="">全部</el-radio>
            <el-radio label="0" value="0">未审核</el-radio>
            <el-radio label="-1" value="-1">未通过</el-radio>
            <el-radio label="1" value="1">已通过</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="类型：" >
          <el-radio-group v-model="form.type">
            <el-radio label="" value="">全部</el-radio>
            <el-radio label="2" value="2">出题专家</el-radio>
            <el-radio label="3" value="3">面试官</el-radio>
          </el-radio-group>
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
            width="50">
        </el-table-column>
        <el-table-column
            prop="type_name"
            align="center"
            label="类型"
            width="100">
        </el-table-column>
        <el-table-column
            prop="name"
            align="center"
            label="名称">
        </el-table-column>
        <el-table-column
            prop="phone"
            align="center"
            label="手机号">
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
            width="300"
            align="center"
            label="操作">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="onAdd(scope.row.id)">详情</el-button>

            <el-button type="text" size="small" style="color: red" @click="delQ(scope.row.id, 1)" v-if="scope.row.status === '未审核'">通过</el-button>
            <el-button type="text" size="small" style="color: red" @click="delQ(scope.row.id, -1)"  v-if="scope.row.status === '未审核'">不通过</el-button>
            <el-button type="text" size="small" style="color: red" @click="delQ(scope.row.id, 0)"  v-if="scope.row.status === '已通过'">禁用</el-button>
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
        type: '',
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
      this.$http.post(DOMAIN_API_SYS + "/interviewer/verify/index/", this.form).then(res => {
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
    delQ(id_, status){
      this.$confirm('确定执行吗, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.loading = true;
          this.$http.post(DOMAIN_API_SYS + "/interviewer/verify/status/", {id: id_, status: status}).then(res => {
              this.onSubmit()
          }).catch((res) => {
            this.$layer_message(res.result)
          })

          this.$message({
            type: 'success',
            message: '操作成功!'
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          });
        });


    },
  }
}
</script>

<style scoped>

</style>