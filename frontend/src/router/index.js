import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import ProductSetView from '@/views/ProductSetView.vue'
import RequestsView from '@/views/RequestsView.vue'
import OfferView from '@/views/OfferView.vue'
import MyCartView from '@/views/MyCartView.vue'
import OrdersView from '@/views/OrdersView.vue'

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
  {
    path: '/offers',
    component: OfferView
  },
  {
    path: '/my-cart',
    component: MyCartView
  },
  {
    path: '/my-orders',
    component: OrdersView
  }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
