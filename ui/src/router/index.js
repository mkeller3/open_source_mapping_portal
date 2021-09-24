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
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
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
  },
  {
    path: '/portal_search',
    name: 'Portal Search',
    component: () => import('../views/PortalSearch.vue')
  },
  {
    path: '/project',
    name: 'PProject',
    component: () => import('../views/Project.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
