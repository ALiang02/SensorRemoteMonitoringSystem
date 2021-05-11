<template>
  <div class="sensor">
    <h2>传感器状态</h2>
    <el-table :data="nodes" border highlight-current-row>
      <el-table-column fixed prop="sensor_id" label="编号"> </el-table-column>
      <el-table-column prop="ip" label="ip地址"> </el-table-column>
      <el-table-column prop="gps" label="gps位置"> </el-table-column>
      <el-table-column prop="energy" label="剩余能量"> </el-table-column>
      <el-table-column prop="data_types" label="正在收集的环境数据">
      </el-table-column>
      <el-table-column fixed="right" label="操作">
        <template slot-scope="scope">
          <el-button @click="handleClick(scope.row)" type="text" size="small"
            >查看</el-button
          >
          <el-button type="text" size="small">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      nodes: [],
    };
  },
  methods: {
    getNodes() {
      this.$axios({
        url: "/get_sensor_list",
      }).then(({ data }) => {
        this.nodes = data.sensor_list;
      });
    },
  },
  mounted() {
    this.getNodes();
  },
};
</script>
