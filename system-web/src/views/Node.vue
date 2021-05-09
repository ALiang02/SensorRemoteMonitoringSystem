<template>
  <div class="node">
    <!-- <el-container>
      <el-aside width="400px">Aside</el-aside>
      <el-main></el-main>
    </el-container> -->
    <el-row>
      <el-col :span="8" id="chart" style="width: 1200px; height: 900px">
      </el-col>
      <el-col :span="4">
        <h3>{{ id }}号传感器</h3>
        <h4>位置：({{ GPS_data.postion_x }},{{ GPS_data.postion_y }})</h4>
        <h4>版本：{{ version }}</h4>

        <h4>数据种类：</h4>
        <el-tag
          :key="tag"
          v-for="tag in data_types"
          closable
          :disable-transitions="false"
          @close="handleClose(tag)"
        >
          {{ tag }}
        </el-tag>
        <el-input
          class="input-new-tag"
          v-if="inputVisible"
          v-model="inputValue"
          ref="saveTagInput"
          size="small"
          @keyup.enter.native="handleInputConfirm"
          @blur="handleInputConfirm"
        >
        </el-input>
        <el-button
          v-else
          class="button-new-tag"
          size="small"
          @click="showInput"
        >
          添加数据种类
        </el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from "echarts";
import { Message, MessageBox } from "element-ui";

export default {
  data() {
    return {
      id: 1,
      GPS_data: {
        postion_x: 1,
        postion_y: 1,
      },
      version: "1.012",

      environment_datas: [
        {
          temperature: 22, //温度，单位℃
          humidity: 30, //湿度，单位%
          time: "2021-04-09-16-00",
        },
        {
          temperature: 23, //温度，单位℃
          humidity: 33, //湿度，单位%
          time: "2021-04-09-20-00",
        },
        {
          temperature: 25, //温度，单位℃
          humidity: 36, //湿度，单位%
          time: "2021-04-10-00-00",
        },
        {
          temperature: 24, //温度，单位℃
          humidity: 31, //湿度，单位%
          time: "2021-04-10-04-00",
        },
        {
          temperature: 26, //温度，单位℃
          humidity: 34, //湿度，单位%
          time: "2021-04-10-08-00",
        },
      ],
      data_types: ["temperature", "humidity"],
      inputVisible: false,
      inputValue: "",
    };
  },
  methods: {
    handleClose(tag) {
      MessageBox.confirm("此操作将删除该数据类型, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.data_types.splice(this.data_types.indexOf(tag), 1);
          Message({
            type: "success",
            message: "删除成功!",
          });
        })
        .catch(() => {
          Message({
            type: "info",
            message: "已取消删除",
          });
        });
    },

    showInput() {
      this.inputVisible = true;
      this.$nextTick(() => {
        this.$refs.saveTagInput.$refs.input.focus();
      });
    },

    handleInputConfirm() {
      let inputValue = this.inputValue;
      if (inputValue) {
        this.data_types.push(inputValue);
        Message({
          type: "success",
          message: "添加成功!",
        });
      }
      this.inputVisible = false;
      this.inputValue = "";
    },
  },

  mounted() {
    var myChart = echarts.init(document.getElementById("chart"));
    // 绘制图表
    myChart.setOption({
      title: {
        text: "温度 湿度 数据图",
        left: "center",
      },
      dataset: {
        dimensions: ["time", "humidity", "temperature"],
        source: this.environment_datas,
      },
      tooltip: {},
      grid: [{ bottom: "55%" }, { top: "55%" }],
      legend: {
        data: ["humidity", "temperature"],
        left: "left",
      },
      xAxis: [
        {
          type: "category",
          gridIndex: 0,
        },
        {
          type: "category",
          gridIndex: 1,
        },
      ],
      yAxis: [
        {
          type: "value",
          axisLabel: {
            formatter: "{value} %",
          },
          gridIndex: 0,
        },
        {
          type: "value",
          axisLabel: {
            formatter: "{value} °C",
          },
          gridIndex: 1,
        },
      ],
      series: [
        { type: "line", smooth: true, xAxisIndex: 0, yAxisIndex: 0 },
        { type: "line", smooth: true, xAxisIndex: 1, yAxisIndex: 1 },
      ],
    });
  },
};
</script>
