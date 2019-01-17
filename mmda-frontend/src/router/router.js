import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/views/Index.vue'
import store from '@/store/store'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'index',
      component: Index
    },
    {
      path: '/about',
      name: 'about',
      component: () => import(/* webpackChunkName: "about" */ '@/views/About.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import(/* webpackChunkName: "login" */ '@/views/Login.vue')
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import(/* webpackChunkName: "profile" */ '@/views/Profile.vue')
    },
    {
      path: '/admin/users',
      name: 'adminusers',
      component: () => import(/* webpackChunkName: "adminusers" */ '@/views/AdminUsers.vue')
    },
    {
      path: '/admin/objects',
      name: 'adminobjects',
      component: () => import(/* webpackChunkName: "adminobjects" */ '@/views/AdminObjects.vue')
    },
    {
      path: '/analysis',
      name: 'analysis',
      component: () => import(/* webpackChunkName: "analysis" */ '@/views/Analysis.vue')
    },
    {
      path: '/analysis/new',
      name: 'analysisnew',
      component: () => import(/* webpackChunkName: "analysisnew" */ '@/views/AnalysisNew.vue')
    },
    {
      path: '/analysis/:id',
      props: true,
      name: 'analysisshow',
      component: () => import(/* webpackChunkName: "analysisshow" */ '@/views/AnalysisView.vue')
    },
    {
      path: '/analysis/:id/wordcloud',
      props: true,
      name: 'analysiswordcloud',
      component: () => import(/* webpackChunkName: "analysiswordcloud" */ '@/views/Wordcloud.vue')
    },
    {
      path: '/discourseme',
      name: 'discourseme',
      component: () => import(/* webpackChunkName: "discourseme" */ '@/views/Discourseme.vue')
    },
    {
      path: '/discourseme/new',
      name: 'discoursemenew',
      component: () => import(/* webpackChunkName: "discoursemenew" */ '@/views/DiscoursemeNew.vue')
    },
    {
      path: '/discourseme/:id',
      props: true,
      name: 'discoursemeshow',
      component: () => import(/* webpackChunkName: "discoursemeshow" */ '@/views/DiscoursemeView.vue')
    },
    {
      path: '/discursive',
      name: 'discursive',
      component: () => import(/* webpackChunkName: "discursive" */ '@/views/DiscursivePosition.vue')
    },
    {
      path: '/discursive/new',
      name: 'discursivenew',
      component: () => import(/* webpackChunkName: "discursivenew" */ '@/views/DiscursivePositionNew.vue')
    },
    {
      path: '/discursive/:id',
      props: true,
      name: 'discursiveshow',
      component: () => import(/* webpackChunkName: "discursiveshow" */ '@/views/DiscursivePositionView.vue')
    }
  ]
})

// Allow publicPages and redirect unauthenticated visiteres to the login page
router.beforeEach((to, from, next) => {
  const publicPages = ['/', '/login', '/about']
  const privatePages = !publicPages.includes(to.path)

  // If your authenticated and you want to go the login
  if (store.getters['login/isAuthenticated'] && to.path === '/login') {
    next('/profile')
  }

  // Check if you got a JWT, if so validate it
  store.dispatch('login/testJWT').then(()=> {
    next()
  }).catch(()=> {
    // console.debug(error)
    // If not valid and it's not a private page, your good
    if (!privatePages) {
      next()
    }
  })

})

export default router
