<template>
  <el-row>
    <el-col :span="12">
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="试卷ID">
          <el-input v-model="form.id" placeholder="输入试卷ID或名称"></el-input>
        </el-form-item>
          <el-form-item label="类型">
          <el-radio-group v-model="form.type">
            <el-radio label="" value="">全部</el-radio>
            <el-radio label="1" value="1">测试平台</el-radio>
            <el-radio label="2" value="2">考试平台</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit(1)">搜索</el-button>
          <el-button type="primary" @click="onAdd(0)">添加试卷</el-button>
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
            prop="sid_name"
            align="center"
            label="学科">
        </el-table-column>
        <el-table-column
            prop="level_name"
            align="center"
            label="级别">
        </el-table-column>
        <el-table-column
            prop="do_time"
            align="center"
            label="做题时间(分)">
        </el-table-column>
        <el-table-column
            prop="add_time"
            width="180"
            align="center"
            label="添加时间">
        </el-table-column>
        <el-table-column
            prop=""
            width="180"
            align="center"
            label="操作">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="onAdd(scope.row)">编辑</el-button>
            <el-button type="text" size="small" @click="question_det(scope.row.id)">试题管理</el-button>
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
    <el-dialog :title="title" :visible.sync="dialogFormVisible">
      <el-form ref="form" :model="paper" label-width="120px">
        <el-form-item label="试卷名称">
          <el-input v-model="paper.name" placeholder="试卷名称"></el-input>
        </el-form-item>
        <el-form-item label="类型">
          <el-radio-group v-model="paper.type">
            <el-radio label="1" value="1">测试平台</el-radio>
            <el-radio label="2" value="2">考试平台</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="科目">
          <el-radio-group v-model="paper.sid">
            <el-radio label="1" value="1">k8s</el-radio>
            <el-radio label="2" value="2">mysql</el-radio>
            <el-radio label="3" value="3">Vue</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="级别">
          <el-radio-group v-model="paper.level">
            <el-radio label="1" value="1">初级</el-radio>
            <el-radio label="2" value="2">中级</el-radio>
            <el-radio label="3" value="3">高级</el-radio>
          </el-radio-group>

        </el-form-item>
        <el-form-item label="做题时长(分)" prop="do_time">
          <el-input v-model.number="paper.do_time"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="savePaper()">确 定</el-button>
      </div>
    </el-dialog>
  </el-row>

</template>

<script>
export default {
  data() {
    return {
      title: "添加试卷",
      dialogFormVisible: false,
      loading: false,
      currentPage: 1,
      total: 0,
      page_size: 5,
      initpaper: {
          id: 0,
          name: '',
          type: '1',
          level: '1',
          sid: '1',
          do_time: 0
      },
      paper: {
          id: 0,
          name: '',
          type: '1',
          level: '1',
          sid: '1',
          do_time: 0
      },
      form: {
        id: '',
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
    savePaper: function () {
      this.loading = true;
      this.$http.post(DOMAIN_API_SYS + "/tea/save_paper/", this.paper).then(res => {
        this.$layer_message("保存成功", 'success')
        this.dialogFormVisible = false;
        this.onSubmit()
      }).catch((res) => {
        this.$layer_message(res.result)
      }).finally(() => this.loading = false)
    },
    onSubmit: function (page_id) {
      this.form.page_id = page_id ? page_id: this.currentPage;
      this.form.page_size = this.page_size;
      this.loading = true;
      this.$http.post(DOMAIN_API_SYS + "/tea/paper/", this.form).then(res => {
        let r = res.data.data
        this.tableData = r.page_data;
        this.total = r.sum_len
      }).catch((res) => {
        this.$layer_message(res.result)
      }).finally(() => this.loading = false)
    },
    onAdd: function (paper) {
      console.log(this.initpaper)
      this.paper = paper ? paper: this.initpaper
      this.dialogFormVisible = true;
    },
    question_det: function (id_){
      this.$router.replace({path: "/paper/add/" + id_});
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
      this.$http.post(DOMAIN_API_SYS + "/tea/del_p/", {id: id_, status: -1}).then(res => {
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