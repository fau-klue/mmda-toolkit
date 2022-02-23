// Configuration the router
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
      path: '/keyword',
      name: 'keywordlist',
      component: () => import(/* webpackChunkName: "keywordlist" */ '@/views/KeywordList.vue')
    },
    {
      path: '/keyword/new',
      name: 'keywordnew',
      component: () => import(/* webpackChunkName: "keywordnew" */ '@/views/KeywordNew.vue')
    },
    {
      path: '/keyword/:id',
      props: true,
      name: 'keywordcontent',
      component: () => import(/* webpackChunkName: "keywordcontent" */ '@/views/KeywordContent.vue')
    },
    {
      path: '/keyword/:id/wordcloud',
      props: true,
      name: 'keywordwordcloud',
      component: () => import(/* webpackChunkName: "keywordwordcloud" */ '@/views/WordcloudKeyword.vue')
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
      path: '/constellation',
      name: 'constellationlist',
      component: () => import(/* webpackChunkName: "constellationlist" */ '@/views/ConstellationList.vue')
    },
    {
      path: '/constellation/new',
      name: 'constellationnew',
      component: () => import(/* webpackChunkName: "constellationnew" */ '@/views/ConstellationNew.vue')
    },
    {
      path: '/constellation/:id',
      props: true,
      name: 'constellationcontent',
      component: () => import(/* webpackChunkName: "constellationcontent" */ '@/views/ConstellationContent.vue')
    },
    {
      path: '/constellation/:id/concordances',
      props: true,
      name: 'constellationconcordances',
      component: () => import(/* webpackChunkName: "constellationconcordances" */ '@/views/ConstellationConcordances.vue')
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
