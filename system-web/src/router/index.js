import Vue from 'vue'
import VueRouter from 'vue-router'


Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import(/* webpackChunkName: "about" */ '../views/Login.vue')
  }, {
    path: '/home',
    name: 'Home',
    component: () => import(/* webpackChunkName: "about" */ '../views/Home.vue'),
    children:[ {
      path: 'map',
      name: 'Map',
      component: () => import(/* webpackChunkName: "about" */ '../views/Map.vue')
    },   {
      path: 'sensor',
      name: 'Sensor',
      component: () => import(/* webpackChunkName: "about" */ '../views/Sensor.vue')
    },  {
      path: 'data',
      name: 'Data',
      component: () => import(/* webpackChunkName: "about" */ '../views/Data.vue'),
      children:[ {
        path: 'temperature',
        name: 'Temperature',
        component: () => import(/* webpackChunkName: "about" */ '../views/Temperature.vue')
      },   {
        path: 'humidity',
        name: 'Humidity',
        component: () => import(/* webpackChunkName: "about" */ '../views/Humidity.vue')
      },    ]
      

    },   ]
    
  }
]

const router = new VueRouter({
  routes
})

const VueRouterPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(to){
  return VueRouterPush.call(this,to).catch(err => err)
}


export default router
