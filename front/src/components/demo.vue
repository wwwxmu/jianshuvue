<template>
  <div class="main_content">
    <avatar :image="image_url" size="128"></avatar>
    <h2><a :href="j_url">{{name}}</a></h2>
    <h3>新增字数: {{new_word}} &nbsp;&nbsp; 新增喜欢: {{new_like}} &nbsp;&nbsp; 新增文章: {{new_article}} &nbsp;&nbsp; 新增粉丝: {{new_follows}}</h3>
    <div id="baseInfo"></div>
    <v-table id="aTable"
            :columns="columns"
            :table-data="article_table"
            :show-vertical-border="false"
            :multiple-sort="multipleSort"
            @sort-change="sortChange"
            row-hover-color="#eee"
            row-click-color="#edf7ff"
    ></v-table>
  </div>
</template>
<script>
import echarts from 'echarts'
import axios from 'axios'
import Avatar from 'vue-avatar-component'
// import bTable from 'bootstrap-vue/es/components/table/table'
import 'vue-easytable/libs/themes-base/index.css'
// 导入 table 和 分页组件
import {VTable, VPagination} from 'vue-easytable'
export default {
  components: {Avatar, VTable, VPagination},
  data () {
    return {
      multipleSort: false,
      pageSize: 20,
      chart: null,
      name: null,
      article_table: [],
      image_url: null,
      new_word: 0,
      new_like: 0,
      new_article: 0,
      new_follows: 0,
      j_url: 'https://www.jianshu.com/u/' + this.$route.params.id,
      columns: [
        {
          field: 'title',
          title: '标题',
          width: 400,
          titleAlign: 'center',
          columnAlign: 'center',
          isResize: true
        },
        {
          field: 'link',
          title: '链接',
          width: 350,
          titleAlign: 'center',
          columnAlign: 'center',
          isResize: true
        },
        {
          field: 'comment_num',
          title: '评论数',
          width: 100,
          titleAlign: 'center',
          columnAlign: 'center',
          orderBy: 'asc',
          isResize: true
        },
        {
          field: 'heart_num',
          title: '点赞数',
          width: 100,
          titleAlign: 'center',
          columnAlign: 'center',
          orderBy: 'asc',
          isResize: true
        },
        {
          field: 'read_num',
          title: '阅读量',
          width: 100,
          titleAlign: 'center',
          columnAlign: 'center',
          orderBy: 'asc',
          isResize: true
        }
      ]
    }
  },
  methods: {
    baseInfo (id) {
      this.baseInfoChart = echarts.init(document.getElementById(id))
      var option = {
        title: {
          text: '简书作者基本数据概览',
          left: 'center',
          top: 5,
          textStyle: {
            fontSize: 16,
            fontFamily: 'Helvetica',
            fontWeight: 200
          }
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['关注', '粉丝', '文章', '收获喜欢', '字数'],
          left: 'center',
          top: 30
        },
        grid: {
          left: '15%',
          right: '15%'
        //  bottom: '15%',
        // containLabel: true
        },
        toolbox: {
          feature: {
            dataZoom: {
              yAxisIndex: 'none'
            },
            restore: {},
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          // boundaryGap: false,
          data: []
        },
        yAxis: [{
          type: 'value'
        }, {
          type: 'value'
          // splitLine : {show : false}
        }],
        dataZoom: [{
          start: 0,
          end: 100
        }, {
          type: 'inside'
        }],
        series: [{
          name: '关注',
          type: 'line',
          itemStyle: {
            borderWidth: 5,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
            shadowBlur: 10
          },
          lineStyle: {
            width: 5,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
            shadowBlur: 10
          },
          stack: '总量',
          data: []
        },
        {
          name: '粉丝',
          type: 'line',
          itemStyle: {
            borderWidth: 5,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
            shadowBlur: 10
          },
          lineStyle: {
            width: 5,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
            shadowBlur: 10
          },
          stack: '总量',
          data: []
        },
        {
          name: '文章',
          type: 'line',
          itemStyle: {
            borderWidth: 5,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
            shadowBlur: 10
          },
          lineStyle: {
            width: 5,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
            shadowBlur: 10
          },
          stack: '总量',
          data: []
        },
        {
          name: '收获喜欢',
          type: 'line',
          itemStyle: {
            borderWidth: 5,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
            shadowBlur: 10
          },
          lineStyle: {
            width: 5,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
            shadowBlur: 10
          },
          stack: '总量',
          data: []
        },
        {
          name: '字数',
          type: 'bar',
          itemStyle: {
            color: '#0984e3',
            barBorderRadius: [10, 10, 0, 0],
            shadowColor: 'rgba(0, 0, 0, 0.5)',
            shadowBlur: 10
          },
          yAxisIndex: 1,
          stack: '总量',
          data: []
        }]
      }
      this.baseInfoChart.setOption(option)
      const path = `http://39.108.51.6:8080/api/base/` + this.$route.params.id
      axios.get(path).then(response => {
        this.image_url = response.data.img
        this.name = response.data.name
        this.new_word = response.data.new_word
        this.new_like = response.data.new_like
        this.new_article = response.data.new_article
        this.new_follows = response.data.new_follows
        this.baseInfoChart.setOption({
          xAxis: {
            data: response.data.date
          },
          series: [
            {
              name: '关注',
              data: response.data.following
            },
            {
              name: '粉丝',
              data: response.data.follows
            },
            {
              name: '文章',
              data: response.data.article_nums
            },
            {
              name: '字数',
              data: response.data.word_nums
            },
            {
              name: '收获喜欢',
              data: response.data.like_nums
            }]
        })
      }).catch(error => {
        console.log(error)
      })
      window.addEventListener('resize', function () {
        this.vipSetOption.baseInfoChart.resize()
      })
    },
    sortChange (params) {
      if (params.comment_num) {
        this.article_table.sort(function (a, b) {
          if (params.comment_num === 'asc') {
            return a.comment_num - b.comment_num
          } else if (params.comment_num === 'desc') {
            return b.comment_num - a.comment_num
          } else {
            return 0
          }
        })
      }
      if (params.heart_num) {
        this.article_table.sort(function (a, b) {
          if (params.heart_num === 'asc') {
            return a.heart_num - b.heart_num
          } else if (params.heart_num === 'desc') {
            return b.heart_num - a.heart_num
          } else {
            return 0
          }
        })
      }
      if (params.read_num) {
        this.article_table.sort(function (a, b) {
          if (params.read_num === 'asc') {
            return a.read_num - b.read_num
          } else if (params.read_num === 'desc') {
            return b.read_num - a.read_num
          } else {
            return 0
          }
        })
      }
    }
  },
  mounted () {
    this.$nextTick(function () {
      this.baseInfo('baseInfo')
    })
  },
  created: function () {
    axios.get('http://39.108.51.6:8080/api/article/' + this.$route.params.id).then(response => {
      this.article_table = response.data.article
    }).catch(error => {
      console.log(error)
    })
  }
}
</script>
<style scoped>
#baseInfo {
  position: relative;
  margin: auto auto;
  width: 100%;
  height: 300px;
}
a, a:hover {
    text-decoration: none;
    color: #74b9ff;
}
#aTable {
  position: relative;
  margin: auto auto;
}
</style>
