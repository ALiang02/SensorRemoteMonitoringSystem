<template>
  <div class="test">
    <div
      :span="8"
      id="chart"
      style="width: 1600px; height: 900px"
      @contextmenu.prevent
    ></div>
  </div>
</template>

<script>
import * as echarts from "echarts";

export default {
  data() {
    return {
      nodes: [],
      node_datas: [],
      node_links: [],
    };
  },
  methods: {
    getNodes() {
      this.$axios({
        url: "/get_sensor_list",
      }).then(({ data }) => {
        console.log(data);
        this.nodes = data.sensor_list;
        console.log(this.nodes);
        // this.nodeDraw();
        for (let i = 0; i < this.nodes.length; i++) {
          let [x, y] = this.nodes[i].gps.split(",");
          this.nodes[i].pos_x = parseInt(x);
          this.nodes[i].pos_y = parseInt(y);
          this.node_datas[i] = {
            name: "传感器" + this.nodes[i].sensor_id + "号",
            sensor_id: this.nodes[i].sensor_id,
            x: parseInt(x),
            y: 9 - parseInt(y),
            // itemStyle: { color: "#00ff00" },
          };
          for (let j = 0; j < this.nodes[i].neighborhood_nodes.length; j++) {
            this.node_links.push({
              source: "传感器" + this.nodes[i].neighborhood_nodes[j] + "号",
              target: "传感器" + this.nodes[i].sensor_id + "号",
            });
          }
          this.myDraw();
        }
        // console.log(this.nodes);
        // this.myDraw();
      });
    },
    onContextmenu(event) {
      // console.log(event);
      this.$contextmenu({
        items: [
          {
            label: "查看传感器状态",
            onClick: () => {
              console.log("查看传感器状态");
            },
          },
          {
            label: "查看传感器收集的数据",
            onClick: () => {
              console.log("查看传感器收集的数据");
            },
          },
          // { label: "前进(F)", disabled: true },
          // { label: "重新加载(R)", divided: true, icon: "el-icon-refresh" },
          // { label: "另存为(A)..." },
          // { label: "打印(P)...", icon: "el-icon-printer" },
          // { label: "投射(C)...", divided: true },
          // {
          //   label: "使用网页翻译(T)",
          //   divided: true,
          //   minWidth: 0,
          //   children: [
          //     { label: "翻译成简体中文" },
          //     { label: "翻译成繁体中文" },
          //   ],
          // },
          // {
          //   label: "截取网页(R)",
          //   minWidth: 0,
          //   children: [
          //     {
          //       label: "截取可视化区域",
          //       onClick: () => {
          //         this.message = "截取可视化区域";
          //         console.log("截取可视化区域");
          //       },
          //     },
          //     { label: "截取全屏" },
          //   ],
          // },
          // { label: "查看网页源代码(V)", icon: "el-icon-view" },
          // { label: "检查(N)" },
        ],
        event,
        //x: event.clientX,
        //y: event.clientY,
        customClass: "custom-class",
        zIndex: 3,
        minWidth: 230,
      });
      return false;
    },

    myDraw() {
      var myChart = echarts.init(document.getElementById("chart"));
      // myChart.on("contextmenu", this.onContextmenu);
      // 控制台打印数据的名称
      let that = this;
      myChart.on("contextmenu", function (params) {
        // console.log(params);
        setTimeout(() => {
          that.onContextmenu(params.event.event);
        }, 0);

        // return true;
      });

      myChart.setOption({
        title: {
          text: "无线传感器网络拓扑图",
        },
        tooltip: {},
        animationDurationUpdate: 1500,
        animationEasingUpdate: "quinticInOut",
        series: [
          {
            type: "graph",
            layout: "none",
            symbolSize: 50,
            roam: true,
            label: {
              show: true,
            },
            edgeSymbol: ["circle", "arrow"],
            edgeSymbolSize: [4, 10],
            edgeLabel: {
              fontSize: 20,
            },
            data: this.node_datas,
            links: this.node_links,
            lineStyle: {
              opacity: 0.9,
              width: 2,
              curveness: 0,
            },
          },
        ],
      });
    },
  },
  mounted() {
    this.getNodes();
  },
};
</script>
