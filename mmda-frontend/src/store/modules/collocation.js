import Vue from 'vue'
import Vuex from 'vuex'
import api from '@/api'

Vue.use(Vuex)

const state = {
  // List of all collocation analyses
  userCollocation: null,
  // One single collocation analysis
  collocation: null,
  // List of discoursemes
  discoursemes: [],
  // Collocates of collocation analysis
  collocates: null,
  // Concordances of collocation analysis
  concordances: null,
  concordances_loading : null,
  // Frequency breakdown of collocation analysis
  breakdown: null,
  // Meta data distribution of collocation analysis
  meta: null
}

const getters = {
  userCollocation (state) {
    return state.userCollocation
  },
  collocation (state) {
    return state.collocation
  },
  discoursemes (state) {
    return state.discoursemes
  },
  collocates (state) {
    return state.collocates
  },
  concordances (state) {
    return state.concordances
  },
  concordances_loading (state) {
    return state.concordances_loading
  },
  breakdown (state) {
    return state.breakdown
  },
  meta (state) {
    return state.meta
  }
}

const actions = {
  getUserSingleCollocation ({commit}, data) {
    // Get one collocation analysis
    return new Promise((resolve, reject) => {

      if (!data.username) return reject('No user provided')
      if (!data.collocation_id) return reject('No collocation provided')

      api.get(`/user/${data.username}/collocation/${data.collocation_id}/`).then(function (response) {
        commit('setCollocationSingle', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getUserCollocation ({commit}, username) {
    // Get all collocation analyses of a user
    return new Promise((resolve, reject) => {

      if (!username) return  reject('No user provided')

      api.get(`/user/${username}/collocation/`).then(function (response) {
        commit('setCollocation', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getCollocationDiscoursemes ({commit}, data) {
    // Get list of discoursmes of the collocation analysis
    return new Promise((resolve, reject) => {

      if (!data.username) return reject('No user provided')
      if (!data.collocation_id) return reject('No collocation provided')

      api.get(`/user/${data.username}/collocation/${data.collocation_id}/discourseme/`).then(function (response) {
        commit('setCollocationDiscoursemes', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  addUserCollocation ({commit}, data) { // eslint-disable-line no-unused-vars
    // Get all users collocation analyses
    return new Promise((resolve, reject) => {

      if (!data.username) return reject('No user provided')

      api.post(`/user/${data.username}/collocation/`, data).then(function () {
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  updateUserCollocation ({commit}, data) { // eslint-disable-line no-unused-vars
    // Update collocation analysis details
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.collocation_id) return reject('No collocation provided')

      api.put(`/user/${data.username}/collocation/${data.collocation_id}/`, data).then(function () {
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  deleteUserCollocation ({commit}, data) {
    // Delete an collocation
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.collocation_id) return reject('No collocation provided')

      api.delete(`/user/${data.username}/collocation/${data.collocation_id}/`).then(function () {
        commit('setCollocationSingle', null)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  addDiscoursemeToCollocation ({commit, dispatch}, data) { // eslint-disable-line no-unused-vars
    // Add a discourseme to a collocation analysis
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.collocation_id) return reject('No collocation provided')
      if (!data.discourseme_id) return reject('No discourseme provided')

      api.put(`/user/${data.username}/collocation/${data.collocation_id}/discourseme/${data.discourseme_id}/`).then(function () {
        dispatch('getCollocationDiscoursemes', data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  removeDiscoursemeFromCollocation ({commit, dispatch}, data) { // eslint-disable-line no-unused-vars
    // Remove a discourseme from a collocation analysis
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.collocation_id) return reject('No collocation provided')
      if (!data.discourseme_id) return reject('No discourseme provided')

      api.delete(`/user/${data.username}/collocation/${data.collocation_id}/discourseme/${data.discourseme_id}/`).then(function () {
        dispatch('getCollocationDiscoursemes', data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getCollocationCollocates ({commit}, data) {
    // Get collocates of collocation analysis
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.collocation_id) return reject('No collocation provided')
      if (!data.window_size) return reject('No window size provided')

      let params = new URLSearchParams()
      // Append api/?window_size=12
      params.append("window_size", data.window_size)

      const request = {
        params: params
      }
      api.get(`/user/${data.username}/collocation/${data.collocation_id}/collocate/`, request).then(function (response) {
        commit('setCollocates', response.data);
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getCollocationDiscoursemeCollocates ({commit}, data) {
    // Get collocates of collocation analysis
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.collocation_id) return reject('No collocation provided')
      if (!data.window_size) return reject('No window size provided')
      if (!data.discourseme_items&&!data.discourseme_id&&!data.discourseme_ids) return reject('No discourseme_[items, id or ids]')

      let params = new URLSearchParams()
      // Append api/?window_size=12
      params.append("window_size", data.window_size)
     
      if(data.discourseme_items) for(var it of data.discourseme_items) params.append("collocate", it);
      if(data.discourseme_id) params.append("discourseme",data.discourseme_id);
      if(data.discourseme_ids) for(var ids of data.discourseme_ids) params.append("discourseme", ids);

      const request = {
        params: params
      }
      //console.log(data);
      api.get(`/user/${data.username}/collocation/${data.collocation_id}/collocate/`, request).then(function (response) {
        commit('setCollocates', response.data);
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
      // username
      // collocation_id
      // (items)
      // (window_size)

      if (!data.username) return reject('No username provided')
      if (data.collocation_id===undefined) return reject('No collocation_id provided')

      let params = new URLSearchParams()

      if(data.items){
        data.items.forEach((item)=>{ params.append("item", item) })
      }

      if(data.window_size){
         params.append("window_size", data.window_size)
      }

      //Second order concordances
      //if(data.discourseme_items) for(var it of data.discourseme_items) params.append("collocate", it);
      // if(data.discourseme_id) {
      //   params.append("discourseme",data.discourseme_id);
      // }
      if(data.discourseme_ids) {
        for(var it of data.discourseme_ids) params.append("discourseme", it);
      }

      const request = {
        params: params
      }

      commit('setConcordancesLoading', data);
      api.get(`/user/${data.username}/collocation/${data.collocation_id}/concordance/`, request).then(function (response) {
        // only accept the loading, if data is the latest call
        // otherwise another request has happened and this one is invalid
        // TODO:: cancel prevous requests upon a new one (i.e. notify the server to drop the activity)
        if(data == state.concordances_loading){
          // console.log("req fullfilled");
          commit('setConcordances', response.data)
          commit('setConcordancesLoading',null)
        }
        //}else{
        // console.log("req dropped");
        resolve()
      }).catch(function (error) {
        commit('setConcordances',null)
        commit('setConcordancesLoading',null)
        reject(error)
      })
    })
  },
  cancelConcordanceRequest({commit}){
    //console.log("req canceled");
    commit('setConcordancesLoading',null);
  },
  resetConcordances({commit}){
    commit('setConcordances',null);
  },
  resetBreakdown({commit}){
    commit('setBreakdown',null);
  },
  getCollocationBreakdown ({commit}, data){
    // Get frequency breakdown for collocation analysis
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.collocation_id) return reject('No collocation provided')

      let params = new URLSearchParams()
      if (data.p_show) params.append("p_show", data.p_show)
      const request = {
        params: params
      }

      api.get(`/user/${data.username}/collocation/${data.collocation_id}/breakdown/`, request).then(function (response) {
        commit('setBreakdown', response.data);
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getCollocationMeta ({commit}, data){
    // Get meta data for collocation analysis
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.collocation_id) return reject('No collocation provided')

      let params = new URLSearchParams()
      if (data.s_show) params.append("s_show", data.s_show)
      const request = {
        params: params
      }

      api.get(`/user/${data.username}/collocation/${data.collocation_id}/meta/`, request).then(function (response) {
        commit('setMeta', response.data);
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  }

}

const mutations = {
  setCollocation (state, collocation) {
    // List of collocation analyses
    state.userCollocation = collocation
  },
  setCollocationDiscoursemes (state, discoursemes) {
    // List of discoursemes
    state.discoursemes = discoursemes
  },
  setCollocationSingle (state, collocation) {
    // One collocation analysis
    state.collocation = collocation
  },
  setCollocates (state, collocates) {
    // One collocation analysis
    state.collocates = collocates
  },
  setConcordances (state, concordances) {
    state.concordances = concordances
  },
  setConcordancesLoading(state, concordances_loading){
    state.concordances_loading = concordances_loading;
  },
  setBreakdown (state, breakdown) {
    state.breakdown = breakdown
  },
  setMeta (state, meta) {
    state.meta = meta
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
