import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from './views/Dashboard.vue'
import ClientDetail from './views/ClientDetail.vue'

const routes = [
  { path: '/', component: Dashboard },
  { path: '/client/:id', component: ClientDetail }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router