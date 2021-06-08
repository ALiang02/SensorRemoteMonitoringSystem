<template>
  <div>
    <el-row class="header">
      <el-col :span="16">
        <el-row type="flex" justify="start">
          <el-menu
            default-active="/home/map"
            class="el-menu-vertical-demo menu"
            mode="horizontal"
            @select="handleSelect"
          >
            <el-menu-item index="/home/map">
              <i class="el-icon-s-home"></i>
              <span slot="title">网络拓扑图</span>
            </el-menu-item>
            <el-menu-item index="/home/sensor">
              <!-- <i class="el-icon-school"></i> -->
              <i class="el-icon-s-order"></i>
              <span slot="title">传感器管理</span>
            </el-menu-item>
            <el-menu-item index="/home/data">
              <i class="el-icon-s-data"></i>
              <span slot="title">数据一览</span>
            </el-menu-item>
          </el-menu>
        </el-row>
      </el-col>
      <el-col :span="6" class="search">
        <el-input
          type="text"
          placeholder="请输入内容"
          v-model="searchInput"
          @keyup.enter.native="searchEvent"
        >
          <el-button
            slot="append"
            icon="el-icon-search"
            @click="searchEvent"
            title="搜索"
          ></el-button>
        </el-input>
      </el-col>

      <el-col :span="2">
        <el-row type="flex" justify="end">
          <div class="quit" @click="quitSystem">退出</div>
        </el-row></el-col
      >
    </el-row>
    <br />
    <hr />

    <router-view> </router-view>
  </div>
</template>

<script>
import { Message, MessageBox } from "element-ui";
export default {
  data() {
    return {
      searchInput: "",
    };
  },
  methods: {
    searchEvent() {
      console.log(321);
      console.log(this.searchInput);
      // this.$refs.mainContent.searchEvent(this.searchInput);
      if (
        this.searchInput.includes("温") ||
        this.searchInput.includes("temperature")
      ) {
        this.$router.push({ path: "/home/data/temperature" });
      } else if (
        this.searchInput.includes("湿") ||
        this.searchInput.includes("humidity")
      ) {
        this.$router.push({ path: "/home/data/humidity" });
      } else if (
        this.searchInput.includes("可燃") ||
        this.searchInput.includes("combustibleGas")
      ) {
        this.$router.push({ path: "/home/data/combustibleGas" });
      } else if (
        this.searchInput.includes("烟") ||
        this.searchInput.includes("雾") ||
        this.searchInput.includes("smoke")
      ) {
        this.$router.push({ path: "/home/data/smoke" });
      } else if (
        this.searchInput.includes("传感器") ||
        this.searchInput.includes("节点") ||
        this.searchInput.includes("sensor")
      ) {
        this.$router.push({ path: "/home/sensor" });
      } else if (
        this.searchInput.includes("网络") ||
        this.searchInput.includes("拓扑") ||
        this.searchInput.includes("图") ||
        this.searchInput.includes("map")
      ) {
        this.$router.push({ path: "/home/map" });
      } else {
        Message.info("无效关键字");
      }
    },

    handleSelect(index) {
      console.log(index);

      this.$router.push({ path: index });
    },
    quitSystem() {
      console.log(123);
      MessageBox.confirm("确定退出系统, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.$store.commit("verificationGet", "jl");
          sessionStorage.setItem("verification", "jl");
          this.$router.push({ path: "/login" });
        })
        .catch(() => {
          console.log("取消退出");
        });
    },
  },
};
</script>

<style>
.header {
  height: 60px;
  /* background-color: #c0c0c0; */
}

.title {
  width: auto;
  cursor: pointer;
  line-height: 60px;
  font-size: 32px;
  padding-left: 20px;
  padding-right: 20px;
}

.menu {
  height: 60px;
}

.quit {
  width: auto;
  cursor: pointer;
  line-height: 60px;
  font-size: 24px;
  padding-right: 20px;
  text-decoration: underline;
  color: #0080ff;
}

.search {
  line-height: 60px;
}
</style>
