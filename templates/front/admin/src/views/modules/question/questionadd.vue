<template>
  <el-row v-loading="loading">

    <el-form ref="form" :model="form" label-width="120px" :rules="rules">
      <div class="base_info">

        <el-form-item label="基本属性" style="width: 77px;">
        </el-form-item>
        <el-form-item label="题目ID：">
          <el-input v-model="form.id" disabled></el-input>
        </el-form-item>
        <el-form-item label="状态：" v-if="open_role.indexOf('1') !== -1">
          <el-radio-group v-model="form.status">
            <el-radio label="0" value="0">未审核</el-radio>
            <el-radio label="1" value="1">已审核</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="科目：">
          <el-radio-group v-model="form.sid">
            <el-radio :label="key.id" :value="key.id" v-for="(key, index) in subjects" v-bind:key="index">{{
                key.name
              }}
            </el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="版本：" prop="version">
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
      </div>

      <div class="base_info">
        <el-form-item label="题目信息" style="width: 77px;">
        </el-form-item>
        <el-form-item label="做题时长(分)：" prop="do_time">
          <el-input v-model.number="form.do_time"></el-input>
        </el-form-item>
        <el-form-item label="考点：" prop="do_points">
          <el-input v-model="form.do_points"></el-input>
        </el-form-item>

        <el-form-item label="题目标题：" prop="title">
          <el-input v-model="form.title"></el-input>
        </el-form-item>
        <el-form-item label="题目描述：" prop="desc">
          <el-input type="textarea" v-model="form.desc"></el-input>
        </el-form-item>
        <el-form-item
            v-for="(domain, index) in form.os_detail"
            :label="'环境' + (index+1) + '：'"
            :key="index"
            :prop="domain.content"
            :rules="{
            required: true, message: '内容不能为空', trigger: 'blur'
          }"
        >
          <el-input v-model="domain.content" style="width: 500px; margin-right: 10px;"></el-input>
          <el-button @click.prevent="removeOsDetail(domain)" v-if="index !== 0" type="warning">删除</el-button>
        </el-form-item>
        <el-form-item>
          <el-button @click="addOsDetail">新增环境</el-button>
        </el-form-item>
      </div>

      <div class="base_info">
        <el-form-item label="解题步骤" style="width: 77px;">
        </el-form-item>
        <el-form-item :label="'步骤'+ (index+1) + ':'" prop="step_det" class="step_det"
                      v-for="(item,index) in form.step_list"
                      v-bind:key="index">
          <template>
            <quillEditor
                ref="text"
                v-model="item.content"
                class="editor"
                :options="editorOption"
                @click.native="handleEditAblequestion"
            >
            </quillEditor>
          </template>
          <el-button type="danger" icon="el-icon-delete" circle v-if="index+1 !== 1"
                     @click="del_step(index)"></el-button>
          <el-button type="primary" icon="el-icon-plus" circle v-if="index+1 === form.step_list.length"
                     @click="add_step()"></el-button>
        </el-form-item>
      </div>

      <div class="base_info">
        <el-form-item label="答题步骤" style="width: 77px;">
        </el-form-item>
        <el-form-item :label="'步骤'+ (index+1) + ':'" prop="step_det" class="step_det"
                      v-for="(item,index) in form.answer_list"
                      v-bind:key="index">
          <template>
            <quillEditor
                ref="text"
                v-model="item.content"
                class="editor"
                :options="editorOption"
                @click.native="handleEditAblequestion"
            >
            </quillEditor>
          </template>
          <el-button type="danger" icon="el-icon-delete" circle v-if="index+1 !== 1"
                     @click="del_answer(index)"></el-button>
          <el-button type="primary" icon="el-icon-plus" circle v-if="index+1 === form.answer_list.length"
                     @click="add_answer_step()"></el-button>
        </el-form-item>
      </div>
      <el-form-item style="margin-top: 80px;">
        <el-button @click="onSubmit('form')" type="success">保存</el-button>
        <el-button @click="go_bank" type="primary">返回</el-button>
      </el-form-item>
    </el-form>
  </el-row>

</template>

<script>
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
import {quillEditor} from 'vue-quill-editor'

export default {
  components: {
    quillEditor
  },
  data() {

    var checkdo_time = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('请输入做题时间'));
      }
      setTimeout(() => {
        console.log(value)
        if (!Number.isInteger(value)) {
          callback(new Error('请输入数字值'));
        } else {
          if (value > 100) {
            callback(new Error('做题时间必须控制在1至100分钟'));
          } else if (value <= 0) {
            callback(new Error('做题时间必须控制在1至100分钟'));
          } else {
            callback();
          }
        }
      }, 1000);
    };
    return {
      editorOption: {
        placeholder: "请在这里输入步骤详情......",
        modules: {
          toolbar: [
            ['bold', 'italic', 'underline', 'strike'],    //加粗，斜体，下划线，删除线
            ['blockquote', 'code-block'],     //引用，代码块
            [{'header': 1}, {'header': 2}],        // 标题，键值对的形式；1、2表示字体大小
            [{'list': 'ordered'}, {'list': 'bullet'}],     //列表
            [{'script': 'sub'}, {'script': 'super'}],   // 上下标
            [{'indent': '-1'}, {'indent': '+1'}],     // 缩进
            [{'direction': 'rtl'}],             // 文本方向
            [{'size': ['small', false, 'large', 'huge']}], // 字体大小
            [{'header': [1, 2, 3, 4, 5, 6, false]}],     //几级标题
            [{'color': []}, {'background': []}],     // 字体颜色，字体背景颜色
            [{'font': []}],     //字体
            [{'align': []}],    //对齐方式
            ['clean'],    //清除字体样式
          ]
        }
      },

      loading: false,
      role: this.$storage.get("role"),
      open_role: this.$storage.get("open_role"),
      subjects: [],
      form: {
        id: this.$route.params.id,
        sid: 1,
        do_time: 0,
        do_points: '',
        version: '',
        level: "1",
        title: "",
        desc: "",
        size: "1",
        status: "0",
        add_user: this.$storage.get("userId"),
        step_list: [{
          content: ''
        }],
        answer_list: [{
          content: ''
        }],
        os_detail: [{content: ''}]
      },
      qillInit: true,//data里面属性
      rules: {
        do_time: [{validator: checkdo_time, trigger: 'blur'}],
        version: [{required: true, message: '请输入版本', trigger: 'blur'},
          {min: 1, max: 5, message: '长度在 1 到 5 个字符', trigger: 'blur'}],
        title: [{required: true, message: '请输入题目标题', trigger: 'blur'},
          {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}],
        do_points: [{required: true, message: '请输入考点', trigger: 'blur'},
          {min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur'}],
        desc: [{required: true, message: '请输入题目描述', trigger: 'blur'},
          {min: 1, max: 200, message: '长度在 1 到 200 个字符', trigger: 'blur'}]
      }
    }
  },
  mounted() {
    this.$refs.text[0].quill.enable(false)
    this.$refs.text[1].quill.enable(false)
  },
  created() {
    this.loading = true;
    if (this.form.id > 0) {
      this.loading = true;
      this.$http.get(DOMAIN_API_SYS + "/tea/question/?id=" + this.form.id).then(res => {
        let r = res.data.data
        this.form = r
        this.form.sid = Number(this.form.sid)
        this.loading = false
      })
    }
    this.$http.post(DOMAIN_API_SYS + "/tea/subject/all/", {}).then(res => {
      this.subjects = res.data.data
      this.loading = false
    })
  },
  methods: {
    // 删除环境
    removeOsDetail(item) {
      var index = this.form.os_detail.indexOf(item)
      if (index !== -1) {
        this.form.os_detail.splice(index, 1)
      }
    },
    // 新增环境
    addOsDetail() {
      if (this.form.os_detail.length >= 20) {
        return this.$layer_message("最多添加20个环境信息！")
      }
      this.form.os_detail.push({content: ''})
    },
    handleEditAblequestion() {
      if (this.qillInit) {
        this.$refs.text[0].quill.enable(true)
        this.$refs.text[0].quill.focus()
        this.$refs.text[1].quill.enable(true)
        this.$refs.text[1].quill.focus()
        this.qillInit = false
      }
    },
    go_bank: function () {
      this.$router.replace({path: "/question/"});
    },
    // 添加步骤
    add_step: function () {
      if (this.form.step_list.length >= 20) {
        this.$layer_message("最多添加20个解题步骤！")
      } else {
        this.form.step_list.push({content: ''})
      }

    },
    add_answer_step: function () {
      if (this.form.answer_list.length >= 20) {
        this.$layer_message("最多添加20个答题步骤！")
      } else {
        this.form.answer_list.push({content: ''})
      }
    },
    // 删除步骤
    del_answer: function (index) {
      this.$confirm(`确定删除此步骤?`, "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        this.form.answer_list.splice(index, 1);
        this.$message({
          message: "删除成功",
          type: "success",
          duration: 1500,
        });
      })

    },
    // 删除步骤
    del_step: function (index) {
      this.$confirm(`确定删除此步骤?`, "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(() => {
        this.form.step_list.splice(index, 1);
        this.$message({
          message: "删除成功",
          type: "success",
          duration: 1500,
        });
      })

    },
    onSubmit: function (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          var step_data = []
          var answer_step = []
          this.form.os_detail.forEach((option, i) => {
            if (!option.content.length) {
              this.$layer_message(`环境${i + 1}不能为空！`)
              valid = false
            }
            if (option.content.length >= 100) {
              this.$layer_message(`环境${i + 1} 字符不能超过100！`)
              valid = false
            }
          })
          if (!valid) {
            return
          }
          this.form.step_list.forEach((option, i) => {
            if (!option.content.length) {
              this.$layer_message(`解题步骤${i + 1}不能为空！`)
              valid = false
              return
            }
            if (option.content.length >= 500) {
              this.$layer_message(`解题步骤${i + 1} 字符不能超过500！`)
              valid = false
              return
            }
            step_data.push({
              sequence: i + 1,
              content: option.content
            })
          })
          if (!valid) {
            return
          }
          this.form.answer_list.forEach((option, i) => {
            if (!option.content.length) {
              this.$layer_message(`答题步骤${i + 1}不能为空！`)
              valid = false
              return
            }
            if (option.content.length >= 500) {
              this.$layer_message(`答题步骤${i + 1} 字符不能超过500！`)
              valid = false
              return
            }
            answer_step.push({
              sequence: i + 1,
              content: option.content
            })
          })

          this.form.os_detail_data = JSON.stringify(this.form.os_detail)
          this.form.step_data = JSON.stringify(step_data)
          this.form.answer_step = JSON.stringify(answer_step)
          if (valid) {
            this.$http.post(DOMAIN_API_SYS + "/tea/question/", this.form).then(res => {
              this.$layer_message('操作成功', 'success')
              this.$router.replace({path: "/question"});
            }).catch((res) => {
              this.$layer_message(res.result)
            }).finally(() => this.loading = false)
          }

        } else {
          return false;
        }
      });
    },

  }
}
</script>

<style lang="css">
.editor {
  height: 200px;
  margin-bottom: 71px;
}

.ql-container {
  height: 200px !important;
}

.ql-editor {
  height: 200px;
}

.el-form {
  padding-bottom: 20px;
  width: 86%;
}

.ql-toolbar.ql-snow .ql-formats {
  margin: 0;

}

.ql-toolbar.ql-snow {
  padding-bottom: 0;
}

.base_info {
  border: 1px solid #CCCCCC;
  padding: 20px;
  margin: 10px 0;
}
</style>