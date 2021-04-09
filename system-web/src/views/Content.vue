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
      node: {
        //传感器识别ID
        id: 1,
        //x,y轴位置，模拟GPS定位数据
        postion_x: 1,
        postion_y: 1,
        //环境数据,后续可以补充
        environment_data: {
          time: "2021-04-09-16-00", //环境数据更新时间
          temperature: 22, //温度，单位℃
          humidity: 30, //湿度，单位%
        },
        //总环境数据，传感器收集到的历史数据
        environment_datas: [],
        //相邻节点,即该节点能够收集到这些节点发送的数据
        neighborhood_nodes: [],
      },
      //总节点
      nodes: [],
    };
  },
  mounted() {
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
};
</script>


