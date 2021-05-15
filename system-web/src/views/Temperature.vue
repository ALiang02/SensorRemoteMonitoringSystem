<template>
  <div class="temperature">
    <div :span="8" id="temperature" style="width: 1200px; height: 900px" />
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
      temperature_data: {
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
        url: "/get_temperature",
        data: {
          year: this.year,
          month: this.month,
          date: this.date,
        },
      }).then(({ data }) => {
        console.log(data.temperature_data);
        this.temperature_data = data.temperature_data;
        this.table_draw();
      });
    },

    table_draw() {
      let legend_data = [];
      let series_data = [];
      let title = "温度";
      for (let i = 0; i < this.temperature_data.sensors.length; i++) {
        legend_data[i] = this.temperature_data.sensors[i] + "号传感器";
        series_data[i] = {
          name: legend_data[i],
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
        };
      }
      var myChart = echarts.init(document.getElementById("temperature"));
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
              return value + "℃";
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
