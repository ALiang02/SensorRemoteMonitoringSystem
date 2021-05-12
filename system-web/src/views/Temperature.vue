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
      let title =
        this.year + "年" + this.month + "月" + this.date + "日" + "温度";
      for (let i = 0; i < this.temperature_data.sensors.length; i++) {
        legend_data[i] = this.temperature_data.sensors[i] + "号传感器";
        series_data[i] = {
          name: legend_data[i],
          type: "line",
          data: this.temperature_data.values[i],
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
          type: "category",
          boundaryGap: false,
          data: ["0:00", "6:00", "12:00", "18:00"],
        },
        yAxis: {
          type: "value",
          axisLabel: {
            formatter: function (value) {
              return value + "℃";
            },
          },
        },
        series: series_data,
      });
    },
  },

  mounted() {
    this.getNodes();
  },
};
</script>
