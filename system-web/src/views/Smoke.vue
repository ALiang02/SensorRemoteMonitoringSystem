<template>
  <div class="smoke">
    <el-row type="flex">
      <el-col :span="16">
        <div id="smoke" style="width: 100%; height: 900px" />
      </el-col>
      <el-col :span="8">
        <div id="smoke_pie" style="width: 100%; height: 900px" />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from "echarts";
// import { Message, MessageBox } from "element-ui";

export default {
  data() {
    return {
      year: 2021,
      month: 5,
      date: 12,
      smoke_data: {
        sensors: [],
        values: [],
      },
    };
  },
  methods: {
    getNodes() {
      let now = new Date(2021, 1, 1);
      console.log(
        [now.getFullYear(), now.getMonth() + 1, now.getDate()].join("/")
      );
      this.$axios({
        url: "/get_smoke",
        data: {
          year: this.year,
          month: this.month,
          date: this.date,
        },
      }).then(({ data }) => {
        console.log(data.smoke_data);
        this.smoke_data = data.smoke_data;
        this.table_draw();
        this.pie_draw();
      });
    },
    pie_draw() {
      var myChart = echarts.init(document.getElementById("smoke_pie"));
      let pie_data = [
        {
          value: 0,
          name: "异常数据",
        },
        {
          value: 0,
          name: "2ppm~10ppm",
        },
        {
          value: 0,
          name: "10ppm~20ppm",
        },
        {
          value: 0,
          name: "20ppm~30ppm",
        },
        {
          value: 0,
          name: "30ppm~38ppm",
        },
      ];
      console.log(this.smoke_data.values);
      for (let i = 0; i < this.smoke_data.values.length; i++) {
        for (let j = 0; j < this.smoke_data.values[i].length; j++) {
          let value = this.smoke_data.values[i][j][1];
          if (value <= 2) {
            pie_data[0].value++;
          } else if (value < 10) {
            pie_data[1].value++;
          } else if (value < 20) {
            pie_data[2].value++;
          } else if (value < 30) {
            pie_data[3].value++;
          } else if (value < 38) {
            pie_data[4].value++;
          } else {
            pie_data[0].value++;
          }
        }
      }
      console.log(pie_data);

      myChart.setOption({
        title: {
          text: "数据分析",
          left: "left",
        },

        legend: {
          left: "center",
        },
        series: [
          {
            name: "访问来源",
            type: "pie",
            radius: "50%",
            // data: [
            //   { value: 1048, name: "搜索引擎" },
            //   { value: 735, name: "直接访问" },
            //   { value: 580, name: "邮件营销" },
            //   { value: 484, name: "联盟广告" },
            //   { value: 300, name: "视频广告" },
            // ],

            data: pie_data,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      });
    },

    table_draw() {
      let legend_data = [];
      let series_data = [];
      let title = "烟雾浓度";
      for (let i = 0; i < this.smoke_data.sensors.length; i++) {
        legend_data[i] = this.smoke_data.sensors[i] + "号传感器";
        series_data[i] = {
          name: legend_data[i],
          type: "line",
          smooth: true,
          symbol: "none",
          // areaStyle: {},
          data: this.smoke_data.values[i],
          markArea: {
            itemStyle: {
              color: "rgba(255, 173, 177, 0.4)",
            },
            data: [
              [
                {
                  name: "异常数据",
                  yAxis: 38,
                },
                {
                  yAxis: Number.POSITIVE_INFINITY,
                },
              ],
              [
                {
                  name: "异常数据",
                  yAxis: 2,
                },
                {
                  yAxis: Number.NEGATIVE_INFINITY,
                },
              ],
            ],
          },
          markPoint: {
            data: [
              { type: "max", name: "最大值" },
              { type: "min", name: "最小值" },
            ],
          },
          markLine: {
            data: [{ type: "average", name: "平均值" }],
          },
        };
      }
      var myChart = echarts.init(document.getElementById("smoke"));
      // 绘制图表
      myChart.setOption({
        title: {
          text: title,
        },
        tooltip: {
          trigger: "axis",
        },
        legend: {
          data: legend_data,
        },

        xAxis: {
          type: "time",
          boundaryGap: false,
        },
        yAxis: {
          type: "value",
          boundaryGap: [0, "100%"],
          min: 0,
          max: 40,
          axisLabel: {
            formatter: function (value) {
              return value + "ppm";
            },
          },
        },
        dataZoom: [
          {
            type: "inside",
            start: 99,
            end: 100,
          },
          {
            start: 0,
            end: 100,
          },
        ],
        series: series_data,
      });

      for (let x of legend_data) {
        myChart.dispatchAction({
          type: "legendUnSelect",
          // 图例名称
          name: x,
        });
      }
      if (this.$store.state.from_node) {
        myChart.dispatchAction({
          type: "legendSelect",
          // 图例名称
          name: this.$store.state.sensor_id + "号传感器",
        });
      } else {
        myChart.dispatchAction({
          type: "legendAllSelect",
          // 图例名称
          name: this.$store.state.sensor_id + "号传感器",
        });
      }
      this.$store.state.from_node = false;
    },
  },

  mounted() {
    this.getNodes();
  },
};
</script>
