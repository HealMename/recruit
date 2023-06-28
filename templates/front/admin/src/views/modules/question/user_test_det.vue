<template>
  <el-row>
    <el-col :span="24">
      <el-button  @click="go_bank()">返回</el-button>
      <el-empty description="暂无信息" v-if="!tableData.length"></el-empty>

      <el-card class="box-card" v-for="(item,index) in tableData" v-bind:key="index" style="margin-bottom: 10px;">
        <el-descriptions title="题目信息">
          <el-descriptions-item label="ID">{{ item.id }}</el-descriptions-item>
          <el-descriptions-item label="标题">{{ item.title }}</el-descriptions-item>
          <el-descriptions-item label="级别">{{ item.level }}</el-descriptions-item>
          <el-descriptions-item label="规模">{{ item.size }}</el-descriptions-item>
          <el-descriptions-item label="耗时">1分钟</el-descriptions-item>
          <el-descriptions-item label="版本">
            <el-tag size="small">{{ item.version }}</el-tag>
          </el-descriptions-item>

          <el-descriptions-item label="详情">

            <el-button type="text" @click="dialogVisible = true;content=item.content;initTerm();" style="padding-top: 5px;">查看详情</el-button>
            <el-dialog
                title="详情"
                :visible.sync="dialogVisible"
                width="50%">
              <div id="xterm" class="xterm" ></div>
              <span slot="footer" class="dialog-footer">
                  <el-button  @click="dialogVisible = false;">关 闭</el-button>
                </span>
            </el-dialog>
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
    </el-col>
  </el-row>


</template>

<script>
import 'xterm/css/xterm.css'
import { Terminal } from 'xterm'
import { FitAddon } from 'xterm-addon-fit'
export default {

  data() {
    return {
      content: [],
      term: '',
      dialogVisible: false,
      loading: false,
      id: this.$route.params.id,
      tableData: []
    }
  },
  mounted() {


  },
  created() {
    this.onSubmit()
  },
  methods: {
    initTerm() {
        var term = new Terminal({
        fontSize: 14,
        cursorBlink: true,
        rows:24
      });
      this.$nextTick(()=>{
        if (!this.term){
          this.term = term;
          term.open(document.getElementById('xterm'));
        }
        this.content.forEach(el=>{
          term.write(el.msg)
        })

      })
    },
    onSubmit: function () {
      this.loading = true;
      this.$http.post(DOMAIN_API_SYS + "/tea/user/user_test_det/", {id: this.id}).then(res => {
        this.tableData = res.data.data;
      }).catch((res) => {
        this.$layer_message(res.result)
      }).finally(() => this.loading = false)
    },
    go_bank: function () {
      this.$router.replace({path: "/user/test/"});
    },

  }
}
</script>

<style scoped>
  .dia-card{
    height: 400px;
    overflow: scroll;
  }
  .dia-card{
      scrollbar-width: none; /* firefox */
      -ms-overflow-style: none; /* IE 10+ */
  }
  .dia-card::-webkit-scrollbar {
      display: none; /* Chrome Safari */
  }

  .el-dialog__wrapper{
    overflow: hidden;
  }
</style>