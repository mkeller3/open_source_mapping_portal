import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue')
  },
  {
    path: '/map_builder',
    name: 'Map Builder',
    component: () => import('../views/MapBuilder.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
