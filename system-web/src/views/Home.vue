<template>
  <div class="home">
    <el-menu
      :default-active="activeIndex2"
      class="el-menu-demo"
      mode="horizontal"
      @select="handleSelect"
    >
      <el-menu-item index="/home/map">网络拓扑图</el-menu-item>
      <el-menu-item index="/home/sensor">传感器编辑</el-menu-item>
      <el-menu-item index="/home/data">数据一览</el-menu-item>
    </el-menu>
    <router-view />
  </div>
</template>

<script>
export default {
  methods: {
    handleSelect(index) {
      console.log(index);
      this.$router.push({ path: index });
    },
  },
};
</script>