<template>
  <el-row>
    <el-col :span="12">
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="form.id" placeholder="输入学科名称或ID"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button @click="onSubmit(1)">搜索</el-button>
          <el-button @click="detail('')">新增</el-button>
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
            prop="name"
            align="center"
            label="名称"
        >
        </el-table-column>
        <el-table-column
            prop="namespace"
            align="center"
            label="关联项目空间">
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
            <el-button type="text" size="small" @click="detail(scope.row.id)">修改</el-button>
            <el-button type="text" size="small" style="color: red" @click="delQ(scope.row.id, -1)">删除</el-button>
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
<el-dialog title="学科" :visible.sync="dialogFormVisible">
      <el-form :model="subject">
        <el-form-item label="名称" label-width="80px">
          <el-input v-model="subject.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="项目空间" label-width="80px">
          <el-select v-model="subject.namespace" placeholder="请选择项目空间">
            <el-option :label="item.name" :value="item.name" v-for="item in namespace"
                  v-bind:key="item.name"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="save()">确 定</el-button>
      </div>
    </el-dialog>
    </el-col>

  </el-row>

</template>

<script>
export default {
  data() {
    return {
      dialogFormVisible:false,
      loading: false,
      currentPage: 1,
      total: 0,
      page_size: 5,
      subject: {},
      namespace: [],
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
    this.get_namespace()
    this.onSubmit()
  },
  methods: {
    // 获取项目空间
    get_namespace: function () {
      var thsi = this;
      this.$.get(DOMAIN_API_SYS + "/s8k/namespace_api/", function (res) {
        thsi.namespace = res.data;
      })
    },
    onSubmit: function (page_id) {
      this.form.page_id = page_id ? page_id : this.currentPage;
      this.form.page_size = this.page_size;
      this.loading = true;
      this.$http.post(DOMAIN_API_SYS + "/tea/subject/index/", this.form).then(res => {
        let r = res.data.data
        this.tableData = r.page_data;
        this.total = r.sum_len
      }).catch((res) => {
        this.$layer_message(res.result)
      }).finally(() => this.loading = false)
    },
    handleSizeChange: function (val) {
      this.page_size = val;
      this.onSubmit()
    },
    handleCurrentChange(val) {
      this.currentPage = val;
      this.onSubmit();
    },
    // 审核详情
    detail(id_) {
      this.dialogFormVisible = true;
      var thsi = this;
      this.$.get(DOMAIN_API_SYS + "/tea/subject/add/?id=" + id_ || '', function (res) {
        console.log(res)
        thsi.subject = res.data;
      })
    },
    save(){
      var thsi = this;
      this.$http.post(DOMAIN_API_SYS + "/tea/subject/add/", thsi.subject).then(res => {
        thsi.dialogFormVisible = false;
        this.onSubmit()
      })
    },
    delQ(id_, status) {
      this.$confirm('确定执行吗, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        lockScroll: false
      }).then(() => {
        this.loading = true;
        this.$http.post(DOMAIN_API_SYS + "/tea/subject/status/", {id: id_, status: status}).then(res => {
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