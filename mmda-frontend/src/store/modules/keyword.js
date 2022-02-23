import Vue from 'vue'
import Vuex from 'vuex'
import api from '@/api'

Vue.use(Vuex)

const state = {
  // List of all keyword analyses
  userKeyword: null,
  // One single keyword analysis
  keyword: null,
  // List of discoursemes
  discoursemes: [],
  // Keywords of keyword analysis
  keywords: null,
  // Concordances of keyword analysis
  concordances: null,
  concordances_loading : null,
}

const getters = {
  userKeyword (state) {
    return state.userKeyword
  },
  keyword (state) {
    return state.keyword
  },
  discoursemes (state) {
    return state.discoursemes
  },
  keywords (state) {
    return state.keywords
  },
  concordances (state) {
    return state.concordances
  },
  concordances_loading (state) {
    return state.concordances_loading
  }
}

const actions = {
  getUserSingleKeyword ({commit}, data) {
    // Get one keyword analysis
    return new Promise((resolve, reject) => {

      if (!data.username) return reject('No user provided')
      if (!data.keyword_id) return reject('No keyword id provided')

      api.get(`/user/${data.username}/keyword/${data.keyword_id}/`).then(function (response) {
        commit('setKeywordSingle', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getUserKeyword ({commit}, username) {
    // Get all keyword analyses of a user
    return new Promise((resolve, reject) => {

      if (!username) return reject('No user provided')

      api.get(`/user/${username}/keyword/`).then(function (response) {
        commit('setKeyword', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getKeywordDiscoursemes ({commit}, data) {
    // Get list of discoursmes of the analysis
    return new Promise((resolve, reject) => {

      if (!data.username) return reject('No user provided')
      if (!data.keyword_id) return reject('No keyword id provided')

      api.get(`/user/${data.username}/keyword/${data.keyword_id}/discourseme/`).then(function (response) {
        commit('setKeywordDiscoursemes', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  addUserKeyword ({commit}, data) { // eslint-disable-line no-unused-vars
    // Get all users analysis
    return new Promise((resolve, reject) => {

      if (!data.username) return reject('No user provided')

      api.post(`/user/${data.username}/keyword/`, data).then(function () {
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  updateUserKeyword ({commit}, data) { // eslint-disable-line no-unused-vars
    // Update analysis details
    return new Promise((resolve, reject) => {

      if (!data.username)   return reject('No user provided')
      if (!data.keyword_id) return reject('No keyword id provided')

      api.put(`/user/${data.username}/keyword/${data.keyword_id}/`, data).then(function () {
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  deleteUserKeyword ({commit}, data) {
    // Delete an analysis
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.keyword_id)  return reject('No keyword id provided')

      api.delete(`/user/${data.username}/keyword/${data.keyword_id}/`).then(function () {
        commit('setKeywordSingle', null)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  addDiscoursemeToKeyword ({commit, dispatch}, data) { // eslint-disable-line no-unused-vars
    // Add a discourseme to an analysis
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.keyword_id) return reject('No keyword id provided')
      if (!data.discourseme_id) return reject('No discourseme provided')

      api.put(`/user/${data.username}/keyword/${data.keyword_id}/discourseme/${data.discourseme_id}/`).then(function () {
        dispatch('getKeywordDiscoursemes', data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  removeDiscoursemeFromKeyword ({commit, dispatch}, data) { // eslint-disable-line no-unused-vars
    // Remove a discourseme from an analysis
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.keyword_id)  return reject('No keyword provided')
      if (!data.discourseme_id) return reject('No discourseme provided')

      api.delete(`/user/${data.username}/keyword/${data.keyword_id}/discourseme/${data.discourseme_id}/`).then(function () {
        dispatch('getKeywordDiscoursemes', data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getKeywordKeywords ({commit}, data) {
    // Get keywords
    return new Promise((resolve, reject) => {
      
      if (!data.username)    return reject('No user provided')
      if (!data.keyword_id)  return reject('No keyword id provided')

      let params = new URLSearchParams()

      const request = {
        params: params
      }
      api.get(`/user/${data.username}/keyword/${data.keyword_id}/keywords/`, request).then(function (response) {
        commit('setKeywords', response.data);
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getKeywordDiscoursemeKeywords ({commit}, data) {
    // Get keyword analysis
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.keyword_id)  return reject('No keyword provided')
      if (!data.discourseme_items&&!data.discourseme_id&&!data.discourseme_ids) return reject('No discourseme_[items, id or ids]')

      let params = new URLSearchParams()
     
      if(data.discourseme_items) for(var it of data.discourseme_items) params.append("keyword", it);
      if(data.discourseme_id) params.append("discourseme",data.discourseme_id);
      if(data.discourseme_ids) for(var ids of data.discourseme_ids) params.append("discourseme", ids);

      const request = {
        params: params
      }
      //console.log(data);
      api.get(`/user/${data.username}/keyword/${data.keyword_id}/keywords/`, request).then(function (response) {
        commit('setKeywords', response.data);
        //console.log(response.data.t_score);
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getConcordances ({commit}, data ) {
    // Get Concordances
    return new Promise((resolve, reject) => {

      if (!data.username) return reject('No username provided')
      if (data.keyword_id===undefined) return reject('No keyword_id provided')

      let params = new URLSearchParams()

      if(data.items){
        data.items.forEach((item)=>{ params.append("item", item) })
      }

      if(data.discourseme_ids) {
        for(var it of data.discourseme_ids) params.append("discourseme", it);
      }

      const request = {
        params: params
      }

      commit('setConcordancesLoading', data);
      api.get(`/user/${data.username}/keyword/${data.keyword_id}/concordance/`, request).then(function (response) {
        if(data == state.concordances_loading){
          commit('setConcordances', response.data)
          commit('setConcordancesLoading',null)
        }
        resolve()
      }).catch(function (error) {
        commit('setConcordances',null)
        commit('setConcordancesLoading',null)
        reject(error)
      })
    })
  },
  cancelConcordanceRequest({commit}){
    commit('setConcordancesLoading',null);
  },
  resetConcordances({commit}){
    commit('setConcordances',null);
  }
}

const mutations = {
  setKeyword (state, keyword) {
    // List of analysis
    state.userKeyword = keyword
  },
  setKeywordDiscoursemes (state, discoursemes) {
    // List of discoursemes
    state.discoursemes = discoursemes
  },
  setKeywordSingle (state, keyword) {
    // One analysis
    state.keyword = keyword
  },
  setKeywords (state, keywords) {
    // One analysis
    state.keywords = keywords
  },
  setConcordances (state, concordances) {
    state.concordances = concordances
  },
  setConcordancesLoading(state, concordances_loading){
    state.concordances_loading = concordances_loading;
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
