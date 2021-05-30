<template>
  <div class="map">
    <div
      :span="8"
      id="chart"
      style="width: 100%; height: 900px"
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
        url: "/get_sensor_list", //向服务器发送http请求获得传感器数据
      }).then(({ data }) => {
        //对data数据进行解析
        console.log(data);
        this.nodes = data.sensor_list;
        console.log(this.nodes);
        for (let i = 0; i < this.nodes.length; i++) {
          //对节点进行遍历
          let [x, y] = this.nodes[i].gps.split(","); //将模拟gps位置提取到x,y中
          this.nodes[i].pos_x = parseInt(x);
          this.nodes[i].pos_y = parseInt(y);
          let category = 0; //对传感器分类，关闭着的传感器分类为0
          if (this.nodes[i].status) {
            if (this.nodes[i].energy <= 20) category = 2;
            //剩余能量少的传感器分类为2
            else category = 1;
            //开启的传感器分类为1
          }

          this.node_datas[i] = {
            //将传感器数据提取到node_data中供echarts加载
            name: "传感器" + this.nodes[i].sensor_id + "号", //节点名称
            sensor_id: this.nodes[i].sensor_id,
            data_types: this.nodes[i].data_types,
            x: parseInt(x), //节点x轴位置
            y: 9 - parseInt(y), //节点y轴位置
            category, //节点分类
          };

          for (let j = 0; j < this.nodes[i].neighborhood_nodes.length; j++) {
            //提取传感器节点间的数据交互到node_links供echarts加载
            this.node_links.push({
              source: "传感器" + this.nodes[i].neighborhood_nodes[j] + "号",
              target: "传感器" + this.nodes[i].sensor_id + "号",
            });
          }

          this.myDraw(); //绘制echarts网络拓扑图
        }
      });
    },
    onContextmenu(event, attr) {
      this.$contextmenu({
        items: [
          {
            label: "查看传感器状态",
            onClick: () => {
              console.log("查看传感器状态");
              console.log(attr);

              this.$router.push({ path: "/home/sensor" });
            },
            divided: true,
          },
          {
            label: "查看湿度",
            onClick: () => {
              console.log("查看湿度");
              console.log(attr);
              this.$router.push({ path: "/home/data/humidity" });
              this.$store.state.from_node = true;
            },
            disabled: !attr.data_types.includes("humidity"),
          },
          {
            label: "查看温度",
            onClick: () => {
              console.log("查看温度");
              console.log(attr);
              this.$router.push({ path: "/home/data/temperature" });
              this.$store.state.from_node = true;
            },
            disabled: !attr.data_types.includes("temperature"),
          },
          {
            label: "查看烟雾浓度",
            onClick: () => {
              console.log("查看烟雾浓度");
              console.log(attr);
              this.$router.push({
                path: "/home/data/combustibleGas",
              });
              this.$store.state.from_node = true;
            },
            disabled: !attr.data_types.includes("combustibleGas"),
          },
          {
            label: "查看可燃气体浓度",
            onClick: () => {
              console.log("查看可燃气体浓度");
              console.log(attr);
              this.$router.push({ path: "/home/data/smoke" });
              this.$store.state.from_node = true;
            },
            disabled: !attr.data_types.includes("smoke"),
          },
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
      let that = this;
      myChart.on("contextmenu", function (params) {
        console.log(params);
        that.$store.state.sensor_id = params.data.sensor_id;
        let attr = params.data;
        setTimeout(() => {
          that.onContextmenu(params.event.event, attr);
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
        legend: [{ data: ["关闭着的", "开启着的", "电源不多"] }],
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
            categories: [
              {
                name: "关闭着的",
              },
              {
                name: "开启着的",
              },
              {
                name: "电源不多",
              },
            ],
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
      myChart.dispatchAction({
        type: "legendUnSelect",
        // 图例名称
        name: "关闭着的",
      });
    },
  },
  mounted() {
    this.getNodes();
  },
};
</script>

<style >
.custom-class {
  height: 180px;
}
</style>