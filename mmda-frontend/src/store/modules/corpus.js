import Vue from 'vue'
import Vuex from 'vuex'
import api from '@/api'

Vue.use(Vuex)

const state = {
  // List of all corpora
  corpora: null,
  // One corpus
  corpus: null,
  // Currently selected concordances
  concordances: null
}

const getters = {
  corpora (state) {
    return state.corpora
  },
  corpus (state) {
    return state.corpus
  },
  concordances (state) {
    return state.concordances
  }
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
      api.get(`/corpus/${corpus}`).then(function (response) {
        commit('setCorpus', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getConcordances ({commit}, data ) {
    // Get Concordances
    return new Promise((resolve, reject) => {
      
      if (!data.corpus) return reject('No corpus provided')
      if (!data.topic_items) return reject('No topic items provided')

      let params = new URLSearchParams()
      // Concat item parameter
      data.topic_items.forEach((item)=>{ params.append("item", item) })
      if(data.collocation_items){
        data.collocation_items.forEach((item)=>{ params.append("collocate", item) })
      }
      if(data.window_size){
         params.append("window_size",data.window_size)
      }
      const request = {
        params: params
      };
      api.get(`/corpus/${data.corpus}/concordances/`, request).then(function (response) {
        commit('setConcordances', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  }
}

const mutations = {
  setCorpora (state, corpora) {
    state.corpora = corpora
  },
  setCorpus (state, corpus) {
    state.corpus = corpus
  },
  setConcordances (state, concordances) {
    state.concordances = concordances
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
