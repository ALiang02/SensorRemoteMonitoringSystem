<template>
  <div class="map">
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
        for (let i = 0; i < this.nodes.length; i++) {
          let [x, y] = this.nodes[i].gps.split(",");
          this.nodes[i].pos_x = parseInt(x);
          this.nodes[i].pos_y = parseInt(y);
          let category = 0;
          if (this.nodes[i].status) {
            if (this.nodes[i].energy <= 20) category = 2;
            else category = 1;
          }
          this.node_datas[i] = {
            name: "传感器" + this.nodes[i].sensor_id + "号",
            sensor_id: this.nodes[i].sensor_id,
            data_types: this.nodes[i].data_types,
            x: parseInt(x),
            y: 9 - parseInt(y),
            category,
          };

          for (let j = 0; j < this.nodes[i].neighborhood_nodes.length; j++) {
            this.node_links.push({
              source: "传感器" + this.nodes[i].neighborhood_nodes[j] + "号",
              target: "传感器" + this.nodes[i].sensor_id + "号",
            });
          }

          this.myDraw();
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
