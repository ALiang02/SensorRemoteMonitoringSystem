import Vue from 'vue'
import VueRouter from 'vue-router'


Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import(/* webpackChunkName: "about" */ '../views/Login.vue')
  },  {
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
  }
]

const router = new VueRouter({
  routes
})

export default router
