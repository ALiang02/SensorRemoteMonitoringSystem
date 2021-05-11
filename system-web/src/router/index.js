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
      path: 'data',
      name: 'Data',
      component: () => import(/* webpackChunkName: "about" */ '../views/Data.vue')
    },   {
      path: 'sensor',
      name: 'Sensor',
      component: () => import(/* webpackChunkName: "about" */ '../views/Sensor.vue')
    },  ]
    
  },{
    path: '/content',
    name: 'Content',
    component: () => import(/* webpackChunkName: "about" */ '../views/Content.vue')
  },  {
    path: '/node',
    name: 'Node',
    component: () => import(/* webpackChunkName: "about" */ '../views/Node.vue')
  },  {
    path: '/test',
    name: 'Test',
    component: () => import(/* webpackChunkName: "about" */ '../views/Test.vue')
  }, 
]

const router = new VueRouter({
  routes
})

export default router
