<template>
  <div class="sensor">
    <h2>传感器状态</h2>
    <el-table
      id="sensor_table"
      :data="nodes"
      border
      highlight-current-row
      @row-click="getRow"
    >
      <el-table-column fixed prop="sensor_id" label="编号"> </el-table-column>
      <el-table-column prop="ip" label="ip地址"> </el-table-column>
      <el-table-column prop="gps" label="gps位置"> </el-table-column>
      <el-table-column prop="energy" label="剩余能量">
        <template slot-scope="scope">
          <font v-if="scope.row.energy >= 20" color="success">{{
            scope.row.energy + "%"
          }}</font>
          <font v-else color="error">{{ scope.row.energy + "%" }}</font>
        </template>
      </el-table-column>
      <el-table-column prop="data_types" label="环境数据">
        <template slot-scope="scope">
          <el-link
            v-for="data_type in scope.row.data_types"
            :key="data_type"
            style="float: left; margin: 0px 5px; cursor: pointer"
            @click="data_href(data_type, scope.row.sensor_id)"
          >
            {{ data_type }}
          </el-link>
          <!-- <el-tag
            v-for="data_type in scope.row.data_types"
            :key="data_type"
            type="primary"
            style="float: left; margin: 0px 5px"
          >
            {{ data_type }}
          </el-tag> -->
        </template>
      </el-table-column>
      <el-table-column prop="status" label="开关">
        <template slot-scope="scope">
          <font v-if="scope.row.status === true" color="success">开启</font>
          <font v-else color="error">关闭</font>
        </template>
      </el-table-column>
    </el-table>

    <el-card class="box-card" v-show="card_show">
      <div slot="header" class="clearfix">
        <span>{{ sensor.sensor_id }}号传感器</span>
        <el-button
          style="float: right; padding: 3px 5px"
          type="text"
          @click="sensor_reset"
        >
          重置
        </el-button>
        <el-button
          style="float: right; padding: 3px 5px"
          type="text"
          @click="sensor_update"
        >
          保存修改
        </el-button>
      </div>
      <!-- <div v-for="o in 4" :key="o" class="text item">
        {{ "列表内容 " + o }}
      </div> -->
      <el-form label-width="90px">
        <el-form-item label="传感器编号">
          <el-input v-model="sensor.sensor_id" disabled></el-input>
        </el-form-item>
        <el-form-item label="ip地址">
          <el-input v-model="sensor.ip" disabled></el-input>
        </el-form-item>
        <el-form-item label="gps地址">
          <el-input v-model="sensor.gps" disabled></el-input>
        </el-form-item>
        <el-form-item label="剩余能量">
          <el-input v-model="sensor.energy" disabled></el-input>
        </el-form-item>
        <el-form-item label="数据类型">
          <el-checkbox-group v-model="sensor.data_types">
            <el-checkbox label="humidity" name="data_types"></el-checkbox>
            <el-checkbox label="temperature" name="data_types"></el-checkbox>
            <el-checkbox label="combustibleGas" name="data_types"></el-checkbox>
            <el-checkbox label="smoke" name="data_types"></el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <el-form-item label="传感器开关">
          <el-switch v-model="sensor.status"></el-switch>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { Message, MessageBox } from "element-ui";

export default {
  data() {
    return {
      nodes: [],
      card_show: true,
      sensor: {
        sensor_id: "1",
        ip: "192.168.0.111",
        gps: "1,1",
        energy: 50,
        neighborhood_nodes: "3,4",
        data_types: ["temperature", "combustibleGas"],
        status: true,
      },
      raw_sensor: {
        sensor_id: "1",
        ip: "192.168.0.111",
        gps: "1,1",
        energy: 50,
        neighborhood_nodes: "3,4",
        data_types: ["temperature", "combustibleGas"],
        status: true,
      },
    };
  },
  methods: {
    data_href(target, sensor_id) {
      // console.log(e);
      this.$store.state.sensor_id = sensor_id;
      this.$store.state.from_node = true;

      this.$router.push({ path: "/home/data/" + target });
    },
    sensor_update() {
      console.log(this.sensor);
      MessageBox.confirm("此操作将永久删除该文件, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.$axios({
            url: "/update_sensor",
            data: {
              sensor_id: this.sensor.sensor_id,
              ip: this.sensor.ip,
              gps: this.sensor.gps,
              energy: this.sensor.energy,
              neighborhood_nodes: this.sensor.neighborhood_nodes,
              data_types: this.sensor.data_types.join(","),
              status: this.sensor.status === true ? 1 : 0,
            },
          }).then(({ data }) => {
            console.log(data);
            if (data.flag) {
              Message.success(data.message);
              this.getNodes();
            } else {
              Message.error(data.message);
            }
          });
        })
        .catch(() => {
          Message({
            type: "info",
            message: "已取消删除",
          });
        });
    },
    sensor_reset() {
      this.sensor = this.raw_sensor;
    },
    getRow(row, c) {
      console.log(row);
      console.log(c);
      this.sensor = { ...row };
      this.raw_sensor = { ...row };
      this.$store.state.sensor_id = this.sensor.sensor_id;
    },
    getNodes() {
      this.$axios({
        url: "/get_sensor_list",
      }).then(({ data }) => {
        console.log(data);
        this.nodes = data.sensor_list;
        this.nodes.forEach(function (value) {
          value.data_types = value.data_types.split(",");
          value.status = value.status ? true : false;
        });
        console.log(this.nodes);

        this.sensor = { ...this.nodes[this.$store.state.sensor_id - 1] };
      });
    },
  },
  mounted() {
    console.log(this.sensor_id);
    this.getNodes();
  },
};
</script>

<style>
.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}
.clearfix:after {
  clear: both;
}

/* .box-card {
  width: 480px;
} */
</style>
