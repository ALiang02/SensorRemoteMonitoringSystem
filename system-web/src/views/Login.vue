<template>
  <div class="login">
    <div class="login_input">
      <div class="title">
        <p>管理员登录</p>
      </div>
      <el-input
        class="myInput"
        v-model="account"
        clearable
        placeholder="用户名"
      ></el-input>
      <el-input
        class="myInput"
        v-model="password"
        clearable
        show-password
        placeholder="密码"
      ></el-input>

      <div class="login_button">
        <el-button type="primary" @click="submit">登录</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { Message } from "element-ui";
export default {
  mounted() {
    let x = document.querySelector(".login");
    let y = document.createElement("script");
    y.setAttribute("src", "/external/ribbon.js");
    x.appendChild(y);
    console.log(x);
  },

  destroyed() {
    document.body.removeChild(document.querySelector("#bgCanvas"));
    location.reload();
  },
  data() {
    return {
      account: "",
      password: "",
    };
  },

  methods: {
    submit() {
      console.log("发送");
      this.$axios({
        url: "/login",
        data: {
          account: this.account,
          password: this.password,
        },
      }).then(({ data }) => {
        console.log(data);
        if (data.flag) {
          Message.success(data.message);
          sessionStorage.setItem("verification", data.verification);
          this.$router.push({ path: "/home/map" });
        } else {
          Message.error(data.message);
        }
      });
    },
  },
};
</script>


<style>
@charset "utf-8";
* {
  padding: 0;
  margin: 0;
}

.login {
  width: 500px;
  height: 400px;
  box-sizing: border-box;
  padding: 0 50px;
  border-radius: 5px;
  box-shadow: 0px 2px 12px 0px rgba(105, 105, 105, 0.07);
  background: rgba(255, 255, 255, 0.5);
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: mymove 1s ease-in-out alternate;
  overflow: hidden;
  transition: 1.5s;
}

@keyframes mymove {
  0% {
    width: 0px;
    height: 5px;
  }

  10% {
    width: 50px;
    height: 5px;
  }

  15% {
    width: 100px;
    height: 5px;
  }

  20% {
    width: 150px;
    height: 5px;
  }

  25% {
    width: 200px;
    height: 5px;
  }

  30% {
    width: 250px;
    height: 5px;
  }

  35% {
    width: 300px;
    height: 5px;
  }

  40% {
    width: 350px;
    height: 5px;
  }

  45% {
    width: 450px;
    height: 5px;
  }

  50% {
    width: 500px;
    height: 5px;
  }

  55% {
    height: 30px;
  }

  60% {
    height: 60px;
  }

  65% {
    height: 90px;
  }

  70% {
    height: 120px;
  }

  75% {
    height: 150px;
  }

  80% {
    height: 180px;
  }

  85% {
    height: 210px;
  }

  90% {
    height: 240px;
  }

  95% {
    height: 240px;
  }

  100% {
    height: 300px;
  }
}

.login_input {
  width: 300px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.login_button {
  margin-top: 10px;
}

.myInput {
  margin-bottom: 25px;
}

.title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 30px;
  font-weight: bold;
  color: #606266;
}

.el-button--primary {
  width: 100%;
}
</style>

