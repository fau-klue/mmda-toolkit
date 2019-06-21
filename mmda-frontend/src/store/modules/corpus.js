import Vue from 'vue'
import Vuex from 'vuex'
import api from '@/api'

Vue.use(Vuex)

const state = {
  // List of all corpora
  corpora: null,
  // One corpus
  corpus: null,
}

const getters = {
  corpora (state) {
    return state.corpora
  },
  corpus (state) {
    return state.corpus
  },
}

const actions = {
  getCorpora ({commit}) {
    // Get all available corpora
    return new Promise((resolve, reject) => {
      api.get(`/corpus/`).then(function (response) {
        commit('setCorpora', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getCorpus ({commit}, corpus) {
    // Get corpus details
    return new Promise((resolve, reject) => {

      if (!corpus) return reject('No corpus provided')

      api.get(`/corpus/${corpus}/`).then(function (response) {
        commit('setCorpus', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
}

const mutations = {
  setCorpora (state, corpora) {
    state.corpora = corpora
  },
  setCorpus (state, corpus) {
    state.corpus = corpus
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
