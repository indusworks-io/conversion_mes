import { createRouter, createWebHistory } from 'vue-router'
import { session } from './data/session'
import { userResource } from '@/data/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    redirect: {
      name: 'Workstations',
    }
  },
  {
    path: '/workstations',
    name: 'Workstations',
    component: () => import('@/pages/WorkstationList.vue'),
  },
  {
    path: '/workstation/:id',
    name: 'WorkstationDetails',
    component: () => import('@/pages/WorkstationDetails.vue'),
  },
  {
    path: '/workstation/:id/order/:orderid',
    name: 'OrderDetails',
    component: () => import('@/pages/OrderDetails.vue'),
  }
]

let router = createRouter({
  history: createWebHistory('/frontend'),
  routes,
})


let defaultWorkstation = localStorage.getItem('defaultWorkstation');

router.beforeEach(async (to, from, next) => {
  let isLoggedIn = session.isLoggedIn
  try {
    await userResource.promise
  } catch (error) {
    isLoggedIn = false
  }

  if (to.name === 'Login' && isLoggedIn) {
    next({ name: 'Home' })
  } else if (to.name !== 'Login' && !isLoggedIn) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router
