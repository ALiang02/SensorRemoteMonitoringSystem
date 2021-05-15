<template>
  <div class="humidity">
    <div :span="8" id="humidity" style="width: 1200px; height: 900px" />
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
      humidity_data: {
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
        url: "/get_humidity",
        data: {
          year: this.year,
          month: this.month,
          date: this.date,
        },
      }).then(({ data }) => {
        console.log(data.humidity_data);
        this.humidity_data = data.humidity_data;
        this.table_draw();
      });
    },

    table_draw() {
      let legend_data = [];
      let series_data = [];
      let title = "湿度";
      for (let i = 0; i < this.humidity_data.sensors.length; i++) {
        legend_data[i] = this.humidity_data.sensors[i] + "号传感器";
        series_data[i] = {
          name: legend_data[i],
          type: "line",
          smooth: true,
          symbol: "none",
          // areaStyle: {},
          data: this.humidity_data.values[i],
        };
      }
      var myChart = echarts.init(document.getElementById("humidity"));
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
        series: series_data,
      });
    },
  },

  mounted() {
    this.getNodes();
  },
};
</script>
