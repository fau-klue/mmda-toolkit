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
  concordances: null,
  // Current concordance request object  // for immediate feedback to the user, if loading concordances takes too long
  concordances_loading : null,
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
  },
  concordances_loading (state) {
    return state.concordances_loading
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

      if (!corpus) return reject('No corpus provided')

      api.get(`/corpus/${corpus}/`).then(function (response) {
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
      // Concat item parameter. api/?item=foo&item=bar
      data.topic_items.forEach((item)=>{ params.append("item", item) })

      if(data.collocate_items){
        // Concat item parameter. api/?collocate=foo&collocate=bar
        data.collocate_items.forEach((item)=>{ params.append("collocate", item) })
      }

      if(data.window_size){
         // Append api/?window_size=12
         params.append("window_size", data.window_size)
      }

      const request = {
        params: params
      }
      //console.log("req called");
      commit('setConcordancesLoading', data);
      api.get(`/corpus/${data.corpus}/concordances/`, request).then(function (response) {
        // only accept the loading, if data is the latest call
        // otherwise another request has happened and this one is invalid
        //  TODO:: cancel prevous requests upon a new one (i.e. notify the server to drop the activity)
        if(data == state.concordances_loading){
          //console.log("req fullfilled");
          commit('setConcordances', response.data)
          commit('setConcordancesLoading',null)
        //}else{
        //  console.log("req dropped");
        }
        resolve()
      }).catch(function (error) {
        commit('setConcordancesLoading',null)
        reject(error)
      })
    })
  },
  cancelConcordanceRequest({commit}){
    //console.log("req canceled");
    commit('setConcordancesLoading',null);
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
  },
  setConcordancesLoading(state,concordances_loading){
    state.concordances_loading = concordances_loading;
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
