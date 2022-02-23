// Central Entrypoint for the store
import Vue from 'vue'
import Vuex from 'vuex'
import admin from './modules/admin'
import collocation from './modules/collocation'
import coordinates from './modules/coordinates'
import corpus from './modules/corpus'
import discourseme from './modules/discourseme'
import constellation from './modules/constellation'
import login from './modules/login'
import profile from './modules/profile'
import wordcloud from './modules/wordcloud'
import keyword from './modules/keyword'

Vue.use(Vuex)

// Namespaced central store
const store = new Vuex.Store({
  modules: {
    admin: admin,
    collocation: collocation,
    coordinates: coordinates,
    corpus: corpus,
    discourseme: discourseme,
    constellation: constellation,
    login: login,
    profile: profile,
    wordcloud: wordcloud,
    keyword: keyword
  }
})

export default store
