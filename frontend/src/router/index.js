import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import ProductSetView from '../views/ProductSetView'
import RequestsView from '../views/RequestsView'

const routes = [
  {
    path: '/',
    component: HomeView
  },
  {
    path: '/login',
    component: LoginView
  },
  {
    path: '/show-products',
    component: ProductSetView
  },
  {
    path: '/requests',
    component: RequestsView
  },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
