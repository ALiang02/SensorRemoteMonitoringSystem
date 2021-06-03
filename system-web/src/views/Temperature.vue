<template>
  <div class="temperature">
    <!-- <el-select v-model="sensor" placeholder="请选择">
      <el-option
        v-for="sensor in sensors"
        :key="sensor.sensor_id"
        :label="sensor.sensor_id"
        :value="sensor.sensor_id"
      >
      </el-option>
    </el-select> -->
    <div id="temperature" style="width: 80%; height: 900px" />
    <br />
    <div id="temperature_pie" style="width: 100%; height: 900px" />
    <!-- <el-row type="flex">
      <el-col>
        <div id="temperature" style="width: 100%; height: 900px" />
      </el-col>
      <el-col>
        <div id="temperature_pie" style="width: 100%; height: 900px" />
      </el-col>
    </el-row> -->
  </div>
</template>

<script>
import * as echarts from "echarts";
// import { Message, MessageBox } from "element-ui";

export default {
  data() {
    return {
      line_chart: null,
      legend_data: [],
      series_data: [],
      pie_chart: null,
      pie_data: [],
      // sensor: "",
      // sensors: [],

      temperature_data: {
        sensors: [],
        values: [],
      },
    };
  },
  methods: {
    // getSensors() {
    //   this.$axios({
    //     url: "get_sensor_list",
    //     data: {},
    //   }).then(({ data }) => {
    //     this.sensors = data.sensor_list;
    //   });
    // },

    getNodes() {
      // let now = new Date(2021, 1, 1);
      // console.log(
      //   [now.getFullYear(), now.getMonth() + 1, now.getDate()].join("/")
      // );
      return this.$axios({
        url: "/get_temperature",
        data: {},
      }).then(({ data }) => {
        console.log(data.temperature_data);
        this.temperature_data = data.temperature_data;

        this.pie_data = [
          {
            value: 0,
            name: "异常数据",
          },
          {
            value: 0,
            name: "2℃~10℃",
          },
          {
            value: 0,
            name: "10℃~20℃",
          },
          {
            value: 0,
            name: "20℃~30℃",
          },
          {
            value: 0,
            name: "30℃~38℃",
          },
        ];
        console.log(this.temperature_data.values);
        for (let i = 0; i < this.temperature_data.values.length; i++) {
          for (let j = 0; j < this.temperature_data.values[i].length; j++) {
            let value = this.temperature_data.values[i][j][1];
            if (value <= 2) {
              this.pie_data[0].value++;
            } else if (value < 10) {
              this.pie_data[1].value++;
            } else if (value < 20) {
              this.pie_data[2].value++;
            } else if (value < 30) {
              this.pie_data[3].value++;
            } else if (value < 38) {
              this.pie_data[4].value++;
            } else {
              this.pie_data[0].value++;
            }
          }
        }
        console.log(this.pie_data);

        this.legend_data = [];
        this.series_data = [];

        for (let i = 0; i < this.temperature_data.sensors.length; i++) {
          this.legend_data[i] = this.temperature_data.sensors[i] + "号传感器";
          this.series_data[i] = {
            name: this.legend_data[i],
            type: "line",
            smooth: true,
            symbol: "none",
            // areaStyle: {},
            data: this.temperature_data.values[i],
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
      });
    },

    pie_draw() {
      this.pie_chart = echarts.init(document.getElementById("temperature_pie"));

      this.pie_chart.setOption({
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
            data: this.pie_data,
            label: {
              formatter: "{b}({d}%)",
            },
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
      let title = "温度";

      this.line_chart = echarts.init(document.getElementById("temperature"));
      // 绘制图表
      this.line_chart.setOption({
        title: {
          text: title,
        },
        tooltip: {
          trigger: "axis",
        },
        legend: {
          data: this.legend_data,
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
              return value + "%";
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
        series: this.series_data,
      });

      for (let x of this.legend_data) {
        this.line_chart.dispatchAction({
          type: "legendUnSelect",
          // 图例名称
          name: x,
        });
      }
      if (this.$store.state.from_node) {
        this.line_chart.dispatchAction({
          type: "legendSelect",
          // 图例名称
          name: this.$store.state.sensor_id + "号传感器",
        });
      } else {
        this.line_chart.dispatchAction({
          type: "legendAllSelect",
          // 图例名称
          name: this.$store.state.sensor_id + "号传感器",
        });
      }
      this.$store.state.from_node = false;
    },

    chart_update() {
      setInterval(() => {
        this.line_chart.showLoading();
        this.pie_chart.showLoading();

        this.getNodes().then(() => {
          this.line_chart.hideLoading();
          this.pie_chart.hideLoading();
          this.line_chart.setOption({
            legend: {
              data: this.legend_data,
            },
            series: this.series_data,
          });
          this.pie_chart.setOption({
            series: [
              {
                name: "访问来源",
                type: "pie",
                radius: "50%",
                data: this.pie_data,
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
        });
      }, 10 * 1000);
    },
  },

  mounted() {
    this.getNodes().then(() => {
      this.pie_draw();
      this.table_draw();
    });
    this.chart_update();

    // this.getSensors();
  },
};
</script>
