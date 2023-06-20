<template>
  <div class="container">
    <el-tabs v-model="activeName" @tab-click="haddle">
      <el-tab-pane label="模块列表" name="first">
        <el-table :data="tableData" border v-show="showTable" style="width: 100%">
          <el-table-column prop="mod_code" align="left" label="模块编码" width="80"></el-table-column>
          <el-table-column prop="is_menu" align="left" label="菜单设置">
            <template slot-scope="scope">
              {{ scope.row.is_menu == 1 ? "菜单" : "单页" }}
            </template>
          </el-table-column>
          <el-table-column prop="mod_name" align="center" label="模块名称" width="180">
            <template slot-scope="scope">
              <div style="text-align: left;">
                {{ scope.row.subs ? scope.row.mod_name : "&nbsp &nbsp &nbsp &nbsp" + scope.row.mod_name }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="mod_value" align="left" label="模块值">
          </el-table-column>
          <el-table-column prop="mod_path" align="left" label="模块连接路径">
          </el-table-column>
          <el-table-column prop="mod_order" align="center" label="模块排序" width="75">
          </el-table-column>
          <el-table-column label="操作" fixed="right" align="center" width="150">
            <template slot-scope="scope">
              <el-button type="text" @click="editBtn(scope.row)">编辑</el-button>
              <el-button type="text" @click="delMod(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="添加模块" name="second">
        <el-form :model="form_add" label-width="120px" size="mini">
          <el-form-item label="上级模块：" style="width: 430px;">
            <el-input v-model="form_add.parent_code"></el-input>
          </el-form-item>
          <el-form-item label="模块名称：" style="width: 430px;">
            <el-input v-model="form_add.mod_name"></el-input>
          </el-form-item>
          <el-form-item label="模块编码：" style="width: 430px;">
            <el-input v-model="form_add.mod_code"></el-input>
          </el-form-item>
          <el-form-item label="模块值：" style="width: 430px;">
            <el-input v-model="form_add.mod_value"></el-input>
          </el-form-item>
          <el-form-item label="模块路径：" style="width: 430px;">
            <el-input v-model="form_add.mod_path"></el-input>
          </el-form-item>
          <el-form-item label="模块排序：" style="width: 430px;">
            <el-input v-model="form_add.mod_order"></el-input>
          </el-form-item>
          <el-form-item label="菜单设置：">
            <el-radio-group v-model="form_add.is_menu">
              <el-radio :label="1">是菜单</el-radio>
              <el-radio :label="0">是单页</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="addMod()">添加</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="编辑模块" name="third" v-if="editFlag">
        <el-form :model="form_edit" label-width="120px" size="mini">
          <el-form-item label="上级模块：" style="width: 430px;">
            <el-input v-model="form_edit.parent_code" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="模块名称：" style="width: 430px;">
            <el-input v-model="form_edit.mod_name"></el-input>
          </el-form-item>
          <el-form-item label="模块编码：" style="width: 430px;">
            <el-input v-model="form_edit.mod_code" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="模块值：" style="width: 430px;">
            <el-input v-model="form_edit.mod_value"></el-input>
          </el-form-item>
          <el-form-item label="模块路径：" style="width: 430px;">
            <el-input v-model="form_edit.mod_path"></el-input>
          </el-form-item>
          <el-form-item label="模块排序：" style="width: 430px;">
            <el-input v-model="form_edit.mod_order"></el-input>
          </el-form-item>
          <el-form-item label="菜单设置：">
            <el-radio-group v-model="form_edit.is_menu">
              <el-radio :label="1">是菜单</el-radio>
              <el-radio :label="0">是单页</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="editMod()">编辑</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      activeName: "first",
      tableData: [],// 模块列表
      showTable: false,
      editFlag: false,//编辑tab
      form_add: {//添加模块表单
        parent_code: "",
        mod_name: "",
        mod_code: "",
        mod_value: "",
        mod_path: "",
        mod_order: "",
        is_menu: "",
      },
      form_edit: {//编辑模块表单
        parent_code: "",
        mod_name: "",
        mod_code: "",
        mod_value: "",
        mod_path: "",
        mod_order: "",
        is_menu: "",
      },
    }
  },

  watch: {
    // 分页监听
    table: function () {
    },
  },
  created() {
    this.queryList();
  },
  methods: {
    haddle: function () {
      if (this.activeName !== "third") {
        this.editFlag = false;
      }
    },
    queryList: function () {

      let params = {
        role: this.$storage.get('role'),
      }
      this.$http({
        url: `${DOMAIN_API_SYS}/django7681v/menu_list/?role=${this.$storage.get('role')}`,
        method: "get",
        params: params
      }).then(({r}) => {
        let data = r.data;
        let tableList = [];
        data.forEach(d => {
          tableList.push(d);
          if (d.subs.length) {
            d.subs.forEach(m => {
              tableList.push(m);
            })
          }
        });
        this.tableData = tableList;
        this.showTable = true
      })
    },
    //编辑
    editBtn: function (row) {
      this.editFlag = true;
      this.activeName = "third";
      this.form_edit.mod_order = row.mod_order;
      this.form_edit.parent_code = row.parent_code;
      this.form_edit.mod_name = row.mod_name;
      this.form_edit.mod_code = row.mod_code;
      this.form_edit.mod_value = row.mod_value;
      this.form_edit.mod_path = row.mod_path;
      this.form_edit.is_menu = row.is_menu;
    },
    //删除
    delMod: function (row) {
      this.$confirm('确认要删除该模块吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        let params = {
          "parent_code": row.parent_code,
          "mod_name": row.mod_name,
          "mod_code": row.mod_code,
          "mod_value": row.mod_value,
          "mod_path": row.mod_path,
          "mod_order": row.mod_order,
        };
        this.baseFun().axiosDelete(this.baseUrl().system.module, params, (resp) => {
          let r = resp.data;
          if (r.response === 'ok') {
            this.msgOk("删除成功");
            this.activeName = "first";
            this.queryList();
          } else {
            this.msgErr(r.message)
          }
        })
      }).catch(() => {
      });
    },
    //添加模块
    addMod: function () {
      let params = {
        "parent_code": this.form_add.parent_code,
        "mod_name": this.form_add.mod_name,
        "mod_code": this.form_add.mod_code,
        "mod_value": this.form_add.mod_value,
        "mod_path": this.form_add.mod_path,
        "mod_order": this.form_add.mod_order,
      }
      if (!this.form_add.parent_code || !this.form_add.mod_name || !this.form_add.mod_code || !this.form_add.mod_value || !this.form_add.mod_path || !this.form_add.mod_order) {
        this.msgWarn("请填写完整表单");
        return
      }
      this.baseFun().axiosPut(this.baseUrl().system.module, params, (resp) => {
        let r = resp.data;
        if (r.response === 'ok') {
          this.msgOk(r.message);
          this.activeName = "first";
          this.queryList();
          this.form_add = {};
        } else {
          this.msgErr('操作失败!' + r.message)
        }
      })
    },
    //编辑模块
    editMod: function () {
      let params = {
        "parent_code": this.form_edit.parent_code,
        "mod_name": this.form_edit.mod_name,
        "mod_code": this.form_edit.mod_code,
        "mod_value": this.form_edit.mod_value,
        "mod_path": this.form_edit.mod_path,
        "mod_order": this.form_edit.mod_order,
      };
      if (!this.form_edit.parent_code || !this.form_edit.mod_name || !this.form_edit.mod_code || !this.form_edit.mod_value || !this.form_edit.mod_path || !this.form_edit.mod_order) {
        this.msgWarn("请填写完整表单");
        return
      }
      this.baseFun().axiosPatch(this.baseUrl().system.module, params, (resp) => {
        let r = resp.data;
        if (r.response === 'ok') {
          let data = r.data;
          this.msgOk("编辑成功");
          this.editFlag = false;
          this.activeName = "first";
          this.queryList();
        } else {
          this.msgErr('操作失败!')
        }
      })
    },
    msgOk: function (msg) {
      this.$message({
        message: msg,
        type: 'success',
      })
    },

    msgWarn: function (msg) {
      this.$message({
        message: msg,
        type: 'warning',
      })
    },

    msgErr: function (msg) {
      this.$message.error(msg)
    },
  }
}
</script>

<style scoped>

</style>