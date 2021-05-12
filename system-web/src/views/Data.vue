<template>
  <div class="home">
    <el-menu
      class="el-menu-demo"
      default-active="/home/data/humidity"
      mode="horizontal"
      @select="handleSelect"
    >
      <el-menu-item index="/home/data/humidity">湿度</el-menu-item>
      <el-menu-item index="/home/data/temperature">温度</el-menu-item>
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