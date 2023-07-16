<template>
  <el-row v-loading="loading">
    <!--面试官-->
    <el-col :span="24" >
      <el-descriptions class="margin-top" title="" :column="3" border>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-user"></i>
            姓名
          </template>
          <p v-text="form.ocr_info_front.name"></p>

        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-mobile-phone"></i>
            手机号
          </template>
          <p v-text="form.phone"></p>
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-tickets"></i>
            身份证号
          </template>
          <p v-text="form.ocr_info_front.number_id"></p>
        </el-descriptions-item>
        <el-descriptions-item span="2">
          <template slot="label">
            <i class="el-icon-office-building"></i>
            联系地址
          </template>
          <p v-text="form.ocr_info_front.address"></p>
        </el-descriptions-item>

        <el-descriptions-item span="3">
          <template slot="label">
            <i class="el-icon-office-building"></i>
            身份证有效期
          </template>
          <span v-text="form.ocr_info_back.start_time"></span> -- <span
            v-text="form.ocr_info_back.end_time"></span>
        </el-descriptions-item>
        <template v-for="(item,i) in school_list">
          <el-descriptions-item span="1" :key="i">
            <template slot="label">
              <i class="el-icon-office-building"></i>
              学校
            </template>
            <p v-text="item.school"></p>

          </el-descriptions-item>
          <el-descriptions-item span="1" :key="i">
            <template slot="label">
              <i class="el-icon-office-building"></i>
              学历
            </template>
            <p v-text="item.education"></p>
          </el-descriptions-item>
          <el-descriptions-item span="2" :key="i">
            <template slot="label">
              <i class="el-icon-office-building"></i>
              专业
            </template>
            <p v-text="item.speciality"></p>
          </el-descriptions-item>
          <el-descriptions-item span="3" :key="i">
            <template slot="label">
              <i class="el-icon-office-building"></i>
              入学毕业时间
            </template>
            <span v-text="handle_time(item.time)"></span>
          </el-descriptions-item>
          <el-descriptions-item span="1" :key="i">
            <template slot="label">
              <i class="el-icon-office-building"></i>
              毕业证
            </template>
            <img v-if="item.diploma" :src="item.diploma" class="avatar">
          </el-descriptions-item>
          <el-descriptions-item span="2" :key="i">
            <template slot="label">
              <i class="el-icon-office-building"></i>
              学位证
            </template>
            <img v-if="item.degree" :src="item.degree" class="avatar">
          </el-descriptions-item>
        </template>
        <template v-for="(item,i) in work_list">
          <el-descriptions-item span="1" :key="i">
            <template slot="label">
              <i class="el-icon-office-building"></i>
              公司名
            </template>
            <p v-text="item.name"></p>
          </el-descriptions-item>
          <el-descriptions-item span="1" :key="i">
            <template slot="label">
              <i class="el-icon-office-building"></i>
              从事行业
            </template>
            <p v-text="item.industry"></p>
          </el-descriptions-item>
          <el-descriptions-item span="1" :key="i">
            <template slot="label">
              <i class="el-icon-office-building"></i>
              岗位
            </template>
            <p v-text="item.post"></p>
          </el-descriptions-item>
          <el-descriptions-item span="1" :key="i">
            <template slot="label">
              <i class="el-icon-office-building"></i>
              技能关键词
            </template>
            <span v-text="item.keyword"></span>
          </el-descriptions-item>
          <el-descriptions-item span="2" :key="i">
            <template slot="label">
              <i class="el-icon-office-building"></i>
              工作时间
            </template>
            <span v-text="handle_time(item.time)"></span>
          </el-descriptions-item>
        </template>
        <el-descriptions-item span="3">
          <template slot="label">
            <i class="el-icon-office-building"></i>
            公司在职证明
          </template>
          <img v-if="prove.work" :src="prove.work" class="avatar">
        </el-descriptions-item>
        <el-descriptions-item span="3">
          <template slot="label">
            <i class="el-icon-office-building"></i>
            社保证明
          </template>
          <img v-if="prove.security" :src="prove.security" class="avatar">
        </el-descriptions-item>
        <el-descriptions-item span="3">
          <template slot="label">
            <i class="el-icon-office-building"></i>
            其他证明
          </template>
          <img v-if="prove.other" :src="prove.other" class="avatar">
        </el-descriptions-item>

        <template v-for="(item,i) in knowledge_list">
          <el-descriptions-item span="1" :key="i">
            <template slot="label">
              <i class="el-icon-office-building"></i>
              技能名称
            </template>
            <p v-text="item.name"></p>
          </el-descriptions-item>
          <el-descriptions-item span="1" :key="i">
            <template slot="label">
              <i class="el-icon-office-building"></i>
              使用时长
            </template>
            <p v-text="item.use_month"></p>
          </el-descriptions-item>
          <el-descriptions-item span="1" :key="i">
            <template slot="label">
              <i class="el-icon-office-building"></i>
              掌握程度
            </template>
            <p v-text="item.level"></p>
          </el-descriptions-item>

        </template>


      </el-descriptions>

      <div style="margin: 20px">
        <el-button type="danger" @click="verify_(1)" v-if="status === 0">拒绝</el-button>
        <el-button type="warning" @click="verify_(2)" v-if="status === 0">通过</el-button>
        <el-button @click="go_bank()">返回</el-button>
      </div>
    </el-col>

  </el-row>

</template>

<script>
export default {
  data() {
    return {
      status: 1,
      id: this.$route.params.id,
      knowledge_list:[],
      // 出题专家
      tea: {

      },
      // 其他证明
      prove: {
        work: '',
        security: "",
        other: ""
      },
      // 学历信息
      school_list: [
        {
          education: "",
          school: "",
          speciality: "",
          time: [],
          diploma: "",
          degree: "",
        }
      ],
      // 工作信息
      work_list: [
        {
          name: "",
          industry: "",
          post: "",
          time: [],
          start_time: "",
          end_time: "",
          keyword: "",
        }
      ],
      loading: false,
      form: {
        name: '',
        code: '',
        phone: '',
        ocr_info_front: {
          name: '',
          number_id: '',
          address: '',

        },
        ocr_info_back: {
          start_time: '',
          end_time: '',
          time: []
        },
        imageUrl1: "",
        imageUrl2: "",
        ocr_front: {},
        ocr_back: {}
      },
    }
  },
  mounted() {

  },
  created() {
    this.init_data()

  },
  methods: {
    init_data: function () {

        this.loading = true;
        this.$http.get(DOMAIN_API_SYS + "/interviewer/save/?cms_user_id=" + this.id).then(res => {
          res = res.data
          if (res.response === 'ok') {
            this.loading = false;
            var data = res.data;
            this.status = data.status
            // 第一步
            this.form.name = data.form.nickname;
            this.form.phone = data.form.phone;
            this.imageUrl1 = data.form.imageUrl1
            this.imageUrl2 = data.form.imageUrl2
            this.form.ocr_info_front.name = data.form.name
            this.form.ocr_info_front.address = data.form.ocr_front.address
            this.form.ocr_info_front.number_id = data.form.number_id
            this.form.ocr_info_back.start_time = data.form.start_time
            this.form.ocr_info_back.end_time = data.form.end_time
            this.form.ocr_info_back.time = [
              new Date(data.form.start_time.substring(0, 4),
                  parseInt(data.form.start_time.substring(4, 6)) - 1,
                  data.form.start_time.substring(6, 8)),
              new Date(data.form.end_time.substring(0, 4),
                  parseInt(data.form.end_time.substring(4, 6)) - 1,
                  data.form.end_time.substring(6, 8))]
            this.ocr_front = data.form.ocr_front
            this.ocr_back = data.form.ocr_back
            if (data.school_list.length){
              data.school_list.forEach(option => {
              option.time = [
                new Date(option.time[0].substring(0, 4),
                    parseInt(option.time[0].substring(4, 6)) - 1,
                    option.time[0].substring(6, 8)),
                new Date(option.time[1].substring(0, 4),
                    parseInt(option.time[1].substring(4, 6)) - 1,
                    option.time[1].substring(6, 8))
              ]
            })
              this.school_list = data.school_list
            }


            if (data.work_list.length){
              data.work_list.forEach(option => {
              option.time = [
                new Date(option.time[0].substring(0, 4),
                    parseInt(option.time[0].substring(4, 6)) - 1,
                    option.time[0].substring(6, 8)),
                new Date(option.time[1].substring(0, 4),
                    parseInt(option.time[1].substring(4, 6)) - 1,
                    option.time[1].substring(6, 8))
              ]
            })


            this.work_list = data.work_list
            }
            this.knowledge_list = data.knowledge_list

            this.prove = data.prove || {}
          }

        })

    },
    go_bank: function () {
      this.$router.replace({path: "/verify/"});
    },
    verify_: function (type) {
      if (type === 1) {
        this.$prompt('反馈内容', '拒绝申请', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
        }).then(({value}) => {
          this.$confirm('确定拒绝吗, 是否继续?', '二次确认', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            this.loading = true;
            this.$http.post(DOMAIN_API_SYS + "/interviewer/verify/status/", {
              id: this.id,
              status: -1,
              feedback: value
            }).then(res => {

            }).catch((res) => {
              this.$layer_message(res.result)
            })

            this.$message({
              type: 'success',
              message: '操作成功!'
            });
            this.status = -1
            this.loading = false;
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消'
            });
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          });
        });
      } else {
        // 通过
        this.$confirm('确定通过吗, 是否继续?', '通过申请', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$confirm('确定通过吗, 是否继续?', '二次确认', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            this.loading = true;
            this.$http.post(DOMAIN_API_SYS + "/interviewer/verify/status/", {id: this.id, status: 1}).then(res => {

            }).catch((res) => {
              this.$layer_message(res.result)
            })

            this.$message({
              type: 'success',
              message: '操作成功!'
            });
            this.loading = false;
            this.status = 1
          })

        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          });
        });
      }

    },
    handle_time(time) {
      if (time.length) {
        var start_time_year = time[0].getFullYear();
        var start_time_moth = time[0].getMonth() + 1;
        var start_time_day = time[0].getDate();
        if (start_time_moth < 10) {
          start_time_moth = '0' + start_time_moth
        }
        if (start_time_day < 10) {
          start_time_day = '0' + start_time_day
        }
        var end_time_year = time[1].getFullYear();
        var end_time_moth = time[1].getMonth() + 1;
        var end_time_day = time[1].getDate();
        if (end_time_moth < 10) {
          end_time_moth = '0' + end_time_moth
        }
        if (end_time_day < 10) {
          end_time_day = '0' + end_time_day
        }
        var start_time = `${start_time_year}${start_time_moth}${start_time_day}`
        var end_time = `${end_time_year}${end_time_moth}${end_time_day}`
        return `${start_time} -- ${end_time}`
      }
    },
  }
}
</script>

<style lang="css">

img {
  width: 200px;
  margin: 0 auto;
}
</style>