<template>
  <div class="content">
    <canvas id="map" width="1600" height="900"></canvas>
  </div>
</template>

<script>
export default {
  data() {
    return {
      //传感器节点
      nodeData: {
        //传感器识别ID
        node_id: 1,
        //x,y轴位置，模拟GPS定位数据
        GPS_data: {
          x: 1,
          y: 1,
        },
        //环境数据,后续可以补充
        environment_data: {
          temperature: 22, //温度，单位℃
          humidity: 30, //湿度，单位%
        },

        time: "2021-04-09-16-00", //数据更新时间
      },
      //总节点
      nodeDatas: [],
      nodes: [],
    };
  },
  mounted() {
    this.mapDraw();
    this.getTestData();

    // this.nodeDraw();
  },

  methods: {
    mapDraw() {
      var map = document.getElementById("map");
      var node_map = map.getContext("2d");
      node_map.lineWidth = 1;
      node_map.strokeStyle = "black";
      // node_map.fillStyle = "#E6A23C";
      // node_map.fillRect(0, 0, 1600, 900);
      node_map.setLineDash([1, 4]); // [实线长度, 间隙长度]
      node_map.lineDashOffset = -0;
      // node_map.font = "16px sans-serif";
      for (let i = 1; i < 16; i++) {
        node_map.moveTo(i * 100, 0);
        node_map.lineTo(i * 100, 900);

        node_map.fillText(i, i * 100, 900);
      }
      for (let j = 1; j < 9; j++) {
        node_map.moveTo(0, j * 100);
        node_map.lineTo(1600, j * 100);
        node_map.fillText(9 - j, 0, j * 100);
      }

      node_map.stroke();
    },
    getTestData() {
      this.$axios({
        url: "/get_sensor_list",
      }).then(({ data }) => {
        console.log(data);
        this.nodes = data.sensor_list;
        console.log(this.nodes);
        this.nodeDraw();
      });
    },
    drawArrow(ctx, fromX, fromY, toX, toY, color, theta, headlen, width) {
      //       ctx：Canvas绘图环境
      // fromX, fromY：起点坐标（也可以换成p1，只不过它是一个数组）
      // toX, toY：终点坐标 (也可以换成p2，只不过它是一个数组)
      // theta：三角斜边一直线夹角
      // headlen：三角斜边长度
      // width：箭头线宽度
      // color：箭头颜色
      color = "#000000";
      theta = 30;
      headlen = 20;
      width = 1;

      // 计算各角度和对应的P2,P3坐标
      var angle = (Math.atan2(fromY - toY, fromX - toX) * 180) / Math.PI,
        angle1 = ((angle + theta) * Math.PI) / 180,
        angle2 = ((angle - theta) * Math.PI) / 180,
        topX = headlen * Math.cos(angle1),
        topY = headlen * Math.sin(angle1),
        botX = headlen * Math.cos(angle2),
        botY = headlen * Math.sin(angle2);

      ctx.save();
      ctx.beginPath();

      var arrowX = fromX - topX,
        arrowY = fromY - topY;
      var x = (fromX - toX) / 2;
      var y = (fromY - toY) / 2;
      // ctx.setLineDash([10, 10]); // [实线长度, 间隙长度]
      ctx.moveTo(arrowX, arrowY);
      ctx.moveTo(fromX, fromY);
      ctx.lineTo(toX, toY);
      // ctx.stroke();
      arrowX = toX + topX;
      arrowY = toY + topY;
      // ctx.setLineDash([1, 0]); // [实线长度, 间隙长度]

      ctx.moveTo(arrowX + x, arrowY + y);
      ctx.lineTo(toX + x, toY + y);
      arrowX = toX + botX;
      arrowY = toY + botY;
      ctx.lineTo(arrowX + x, arrowY + y);
      ctx.strokeStyle = color;

      ctx.lineWidth = width;
      ctx.stroke();
      ctx.restore();
    },
    nodeDraw() {
      console.log(this.nodes);
      console.log("123");
      var map = document.getElementById("map");
      var node_map = map.getContext("2d");

      for (let node of this.nodes) {
        node_map.setLineDash([1, 0]); // [实线长度, 间隙长度]
        node_map.beginPath();

        let [x1, y1] = node.gps.split(",");

        node_map.arc(x1 * 100, (9 - y1) * 100, 30, 0, Math.PI * 2, false);

        // node_map.fillStyle = `rgba(${parseInt(
        //   node.color.substring(1, 3),
        //   16
        // )},${parseInt(node.color.substring(1, 3), 16)},${parseInt(
        //   node.color.substring(1, 3),
        //   16
        // )},1)`;
        // node_map.strokeStyle = node.color;
        node_map.stroke();
        for (let node_id of node.neighborhood_nodes) {
          for (let { sensor_id, gps } of this.nodes) {
            if (node_id == sensor_id) {
              let [x2, y2] = gps.split(",");
              this.drawArrow(
                node_map,

                x2 * 100,
                (9 - y2) * 100,
                x1 * 100,
                (9 - y1) * 100
              );
            }
          }
        }
      }
      // this.drawArrow(node_map, 200, 300, 400, 500);
    },

    randomInt(from, to) {
      return parseInt(Math.random() * (to - from + 1) + from);
    },
  },
};
</script>


