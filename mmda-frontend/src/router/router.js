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
      name: 'adminuserlist',
      component: () => import(/* webpackChunkName: "adminuserlist" */ '@/views/AdminUserList.vue')
    },
    {
      path: '/admin/users/new',
      name: 'adminusersnew',
      component: () => import(/* webpackChunkName: "adminusersnew" */ '@/views/AdminUsersNew.vue')
    },
    {
      path: '/admin/objects',
      name: 'adminobjects',
      component: () => import(/* webpackChunkName: "adminobjects" */ '@/views/AdminObjects.vue')
    },
    {
      path: '/analysis',
      name: 'analysislist',
      component: () => import(/* webpackChunkName: "analysislist" */ '@/views/AnalysisList.vue')
    },
    {
      path: '/analysis/new',
      name: 'analysisnew',
      component: () => import(/* webpackChunkName: "analysisnew" */ '@/views/AnalysisNew.vue')
    },
    {
      path: '/analysis/:id',
      props: true,
      name: 'analysiscontent',
      component: () => import(/* webpackChunkName: "analysiscontent" */ '@/views/AnalysisContent.vue')
    },
    {
      path: '/analysis/:id/wordcloud',
      props: true,
      name: 'analysiswordcloud',
      component: () => import(/* webpackChunkName: "analysiswordcloud" */ '@/views/Wordcloud.vue')
    },
    {
      path: '/discourseme',
      name: 'discoursemelist',
      component: () => import(/* webpackChunkName: "discoursemelist" */ '@/views/DiscoursemeList.vue')
    },
    {
      path: '/discourseme/new',
      name: 'discoursemenew',
      component: () => import(/* webpackChunkName: "discoursemenew" */ '@/views/DiscoursemeNew.vue')
    },
    {
      path: '/discourseme/:id',
      props: true,
      name: 'discoursemecontent',
      component: () => import(/* webpackChunkName: "discoursemecontent" */ '@/views/DiscoursemeContent.vue')
    },
    {
      path: '/discursive',
      name: 'discursivelist',
      component: () => import(/* webpackChunkName: "discursivelist" */ '@/views/DiscursivePositionList.vue')
    },
    {
      path: '/discursive/new',
      name: 'discursivenew',
      component: () => import(/* webpackChunkName: "discursivenew" */ '@/views/DiscursivePositionNew.vue')
    },
    {
      path: '/discursive/:id',
      props: true,
      name: 'discursivecontent',
      component: () => import(/* webpackChunkName: "discursivecontent" */ '@/views/DiscursivePositionContent.vue')
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
